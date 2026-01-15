from typing import Literal
from datetime import date, timedelta

from sqlmodel import select
from sqlalchemy import func

# from api.models.program_models import Program, ProgramTags
# from api.models.activity_models import Activity
# from api.models.tag_models import Tag
# from api.models.user_models import UserPreferences
# from api.models.log_models import DailyLogs
# from api.models.user_activity_models import UserActivities

from api.models.program_models import Program
from api.models.activity_models import Activity
from api.models.tag_models import Tag
from api.models.user_preference_models import UserPreference
from api.models.user_activity_models import UserActivity
from api.models.daily_log_models import DailyLog
from api.models.programs_tags_link import ProgramTagLink

class RecommendationService:
    def __init__(self, session):
        self.session = session

    # ==========================================================
    # PUBLIC API
    # ==========================================================

    def get(
        self,
        user_id: int,
        content_type: Literal["program", "activity"],
        limit: int,
        explain: bool,
    ):
        user_prefs = self._get_user_preferences(user_id)

        if user_prefs is None:
            return {
                "user_id": user_id,
                "type": content_type,
                "recommendations": [],
            }

        # if content_type == "program":
        #     recommendations = self._recommend_programs(user_id, user_prefs, explain)
        # else:
        #     recommendations = self._recommend_activities(user_id, user_prefs, explain)

        recommendations = self._recommend_programs(user_id, user_prefs, explain)

        recommendations.sort(key=lambda r: r["score"], reverse=True)

        return {
            "user_id": user_id,
            "type": content_type,
            "recommendations": recommendations[:limit],
        }

    # ==========================================================
    # PROGRAM RECOMMENDATIONS
    # ==========================================================

    def _recommend_programs(self, user_id, user_prefs, explain):
        programs = self.session.exec(select(Program)).all()
        user_program_ids = self._get_user_program_ids(user_id)
        recent_logs = self._get_recent_daily_logs(user_id)

        results = []

        for program in programs:
            if program.id in user_program_ids:
                continue

            score = 0
            reasons = []

            tags = self._get_program_tags(program.id)

            #scoring based off recent mood level
            if ("stress" in tags) or ("mental health" in tags) or ("focus" in tags):
                if recent_logs["mood"] <= 5:
                    score += 8
                    reasons.append("bad mood lately")

            #scoring based off prefered stress reduction
            if user_prefs.stress >= 6 and (("stress" in tags) or ("mental health" in tags)):
                score += 4
                reasons.append("reducing stress level preference")

            #scoring based off recent stress level
            if recent_logs["stress"] >= 7 and "stress" in tags:
                score += 8
                reasons.append("high stress level lately")

            #scoring based off prefered physical activity
            if "workout" in tags:
                if user_prefs.physical_activity <= 3:
                    score += 2
                    reasons.append("low physical intensity preference")
                elif 4 <= user_prefs.physical_activity <= 7:
                    score += 3
                    reasons.append("moderate physical intensity preference")
                elif user_prefs.physical_activity >= 8:
                    score += 5
                    reasons.append("high physical intensity preference")
                
                if recent_logs["physical_activity"] <= 6 and user_prefs.physical_activity >= 7:
                    score += 8
                    reasons.append("low physical activity lately")

                if recent_logs["physical_activity"] <= 3:
                    score += 8
                    reasons.append("very low physical activity lately")

            #scoring based off prefered focus increasing
            if "focus" in tags:
                if user_prefs.focus >= 5:
                    score += 5
                    reasons.append("increasing focus preference")

                if recent_logs["focus"] <= 5:
                    score += 5
                    reasons.append("low focus lately")
                elif recent_logs["focus"] <= 2:
                    score += 8
                    reasons.append("very low focus lately")

            #scoring based off prefered sleep improvement
            if "sleep" in tags:
                if user_prefs.sleep >= 7:
                    score += 5
                if 4 <= user_prefs.sleep < 7:
                    score += 2
                reasons.append("improving sleep preference")

                if recent_logs["sleep"] <= 70:
                    score += 5
                    reasons.append("low quality of sleep lately")
                elif recent_logs["sleep"] <= 50:
                    score += 8
                    reasons.append("very low quality of sleep lately")

            if score > 0:
                results.append({
                    "id": program.id,
                    "name": program.name,
                    "score": score,
                    "reasons": reasons if explain else None,
                })

        return results

    # ==========================================================
    # ACTIVITY RECOMMENDATIONS
    # ==========================================================

    def _recommend_activities(self, user_id, user_prefs, explain):
        activities = self.session.exec(select(Activity)).all()
        user_activity_ids = self._get_user_activity_ids(user_id)
        recent_logs = self._get_recent_daily_logs(user_id)

        results = []

        for activity in activities:
            if activity.id in user_activity_ids:
                continue

            score = 0
            reasons = []

            if activity.difficulty <= user_prefs.physical_activity:
                score += 3
                reasons.append("difficulty matches physical condition")

            if recent_logs["stress"] >= 6 and activity.difficulty <= 2:
                score += 4
                reasons.append("helps reduce stress")

            if score > 0:
                results.append({
                    "id": activity.id,
                    "name": activity.name,
                    "score": score,
                    "reasons": reasons if explain else None,
                })

        return results

    # ==========================================================
    # DATA ACCESS
    # ==========================================================

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

    def _get_program_tags(self, program_id):
        rows = self.session.exec(
            select(Tag.name)
            .join(ProgramTagLink, ProgramTagLink.tag_id == Tag.id)
            .where(ProgramTagLink.program_id == program_id)
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
            "stress": int(row[0] or 0),
            "sleep": int(row[1] or 0),
            "focus": int(row[2] or 0),
            "mood": int(row[3] or 0),
            "physical_activity": int(row[4] or 0),
        }

    # ==========================================================
    # HELPERS
    # ==========================================================

    def _shares_tags_with_previous_programs(self, current_tags, previous_program_ids):
        if not previous_program_ids or not current_tags:
            return False
        return True  # MVP – do rozbudowy
