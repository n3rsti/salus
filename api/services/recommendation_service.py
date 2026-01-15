from typing import Literal
from datetime import date, timedelta

from sqlmodel import select
from sqlalchemy import func, text

from api.models.program_models import Program
from api.models.activity_models import Activity
from api.models.user_preference_models import UserPreference
from api.models.user_activity_models import UserActivity
from api.models.daily_log_models import DailyLog
from api.models.enums import Tag

class RecommendationService:
    def __init__(self, session):
        self.session = session

    def get(self, user_id: int, content_type: str, limit: int, explain: bool):
        user_prefs = self._get_user_preferences(user_id)
        if user_prefs is None:
            user_prefs = self._default_user_preferences(user_id)

        recent_logs = self._get_recent_daily_logs(user_id)
        rows = self._query_scored_items_sql(user_id, limit * 2)

        results = []
        for row in rows:
            if row.item_type != content_type:
                continue

            reasons = (
                self._build_reasons(row, user_prefs, recent_logs)
                if explain else None
            )

            results.append({
                "id": row.id,
                "name": row.name,
                "score": float(row.score),
                "reasons": reasons
            })

            if len(results) >= limit:
                break

        return {
            "user_id": user_id,
            "type": content_type,
            "recommendations": results,
        }

    def _query_scored_items_sql(self, user_id: int, limit: int):
        sql = text("""
            WITH
            recent AS (
            SELECT
                user_id,
                AVG(mood)              AS avg_mood,
                AVG(sleep_score)       AS avg_sleep,
                AVG(stress)            AS avg_stress,
                AVG(focus)             AS avg_focus,
                AVG(physical_activity) AS avg_pa
            FROM dailylog
            WHERE user_id = :user_id
                AND date >= CURRENT_DATE - INTERVAL '7 days'
            GROUP BY user_id
            ),
            prefs AS (
            SELECT
                user_id,
                mood,
                sleep,
                stress,
                focus,
                physical_activity
            FROM userpreference
            WHERE user_id = :user_id
            ),
            need AS (
            SELECT
                p.user_id,
                GREATEST(COALESCE(r.avg_stress, 0)-p.stress            , 0) AS w_stress,
                GREATEST(p.sleep       - COALESCE(r.avg_sleep, 0), 0)  AS w_sleep,
                GREATEST(p.focus             - COALESCE(r.avg_focus, 0), 0)  AS w_focus,
                GREATEST(p.physical_activity - COALESCE(r.avg_pa, 0), 0)     AS w_workout,
                GREATEST(p.mood              - COALESCE(r.avg_mood, 0), 0)   AS w_mental
            FROM prefs p
            LEFT JOIN recent r USING (user_id)
            ),
            tag_weights AS (
            SELECT 1 AS tag, w_stress  AS w FROM need
            UNION ALL SELECT 2, w_workout FROM need
            UNION ALL SELECT 3, w_sleep   FROM need
            UNION ALL SELECT 4, w_focus   FROM need
            UNION ALL SELECT 5, w_mental  FROM need
            ),
            items AS (
            SELECT 'activity' AS item_type, id, name, tags FROM activity
            UNION ALL
            SELECT 'program', id, name, tags FROM program
            ),
            scored AS (
            SELECT
                i.item_type,
                i.id,
                i.name,
                jsonb_agg(DISTINCT itag.tag) AS tags,

                SUM(tw.w) AS raw_score,

                SUM(tw.w)
                / NULLIF(
                    SQRT(jsonb_array_length(jsonb_agg(DISTINCT itag.tag))),
                    0
                    ) AS score

            FROM items i
            CROSS JOIN LATERAL jsonb_array_elements(i.tags::jsonb) AS itag(tag)
            JOIN tag_weights tw
                ON tw.tag = (itag.tag)::int

            GROUP BY
                i.item_type,
                i.id,
                i.name
            )
            SELECT
            item_type,
            id,
            name,
            tags,
            raw_score,
            score
            FROM scored
            ORDER BY score DESC
            LIMIT :limit;
        """).bindparams(
            user_id=user_id,
            limit=limit
        )

        return self.session.exec(sql).all()

    def _build_reasons(self, row, user_prefs, recent_logs):
        reasons = []

        TAG_MAP = {
            "stress": (Tag.STRESS, "You nedd to reduce your stress level"),
            "sleep": (Tag.SLEEP, "You nedd to reduce your sleep quality"),
            "focus": (Tag.FOCUS, "You nedd to improve your focus"),
            "physical_activity": (Tag.WORKOUT, "Matches your desired activity level"),
            "mood": (Tag.MENTAL_HEALTH, "You need to improve your well-being"),
        }

        for attr, (tag, text) in TAG_MAP.items():
            if attr == "stress":
                need = max(recent_logs[attr] - getattr(user_prefs, attr), 0)
            else:
                need = max(getattr(user_prefs, attr) - recent_logs[attr], 0)
            if need > 0 and tag in row.tags:
                reasons.append(text)

        return reasons

    def _get_user_preferences(self, user_id):
        prefs = self.session.exec(
            select(UserPreference).where(UserPreference.user_id == user_id)
        ).first()

        if not prefs:
            return None

        return prefs

    def _get_user_program_ids(self, user_id):
        rows = self.session.exec(
            select(UserActivity.program_id)
            .where(UserActivity.user_id == user_id)
            .where(UserActivity.program_id.is_not(None))
        ).all()

        return set(rows)

    def _get_user_activity_ids(self, user_id):
        rows = self.session.exec(
            select(UserActivity.activity_id)
            .where(UserActivity.user_id == user_id)
            .where(UserActivity.activity_id.is_not(None))
        ).all()

        return set(rows)

    def _get_recent_daily_logs(self, user_id):
        since = date.today() - timedelta(days=7)

        row = self.session.exec(
            select(
                func.avg(DailyLog.stress),
                func.avg(DailyLog.sleep_score),
                func.avg(DailyLog.focus),
                func.avg(DailyLog.mood),
                func.avg(DailyLog.physical_activity)
            )
            .where(DailyLog.user_id == user_id)
            .where(DailyLog.date >= since)
        ).one()

        return {
            "stress": int(row[0] or 5),
            "sleep": int(row[1] or 5),
            "focus": int(row[2] or 5),
            "mood": int(row[3] or 5),
            "physical_activity": int(row[4] or 5),
        }
    
    def _default_user_preferences(self, user_id: int) -> UserPreference:
        return UserPreference(
            user_id=user_id,
            mood=5,
            sleep=5,
            stress=5,
            focus=5,
            physical_activity=3
        )
