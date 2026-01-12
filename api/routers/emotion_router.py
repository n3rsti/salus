from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import delete, select, update

from api.database import SessionDep
from api.models.daily_log_emotions_link import DailyLogEmotionLink
from api.models.emotion_models import Emotion, EmotionCreate, EmotionRead, EmotionUpdate
from api.security.auth import JwtPayload, get_current_user

router = APIRouter(prefix="/api/emotions", tags=["Emotions"])


@router.get("", response_model=List[EmotionRead])
def get_emotions(session: SessionDep):
    emotions = session.exec(select(Emotion)).all()

    if emotions:
        return emotions
    else:
        return []


@router.post("", response_model=EmotionRead)
def create_emotion(emotion_in: EmotionCreate, session: SessionDep):
    emotion = Emotion.model_validate(emotion_in)

    session.add(emotion)
    session.commit()
    session.refresh(emotion)
    return emotion


@router.put("/{emotion_id}", response_model=EmotionRead)
def update_emotion(session: SessionDep, emotion_id: int, emotion_update: EmotionUpdate):
    update_data = emotion_update.model_dump(exclude_unset=True)
    statement = update(Emotion).where(Emotion.id == emotion_id).values(**update_data)
    result = session.exec(statement)
    session.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Emotion not found")

    emotion = session.get(Emotion, emotion_id)
    return emotion


@router.delete("/{emotion_id}")
def delete_emotion(session: SessionDep, emotion_id: int):
    statement = delete(Emotion).where(Emotion.id == emotion_id)
    result = session.exec(statement)
    session.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Emotion not found")

    return {"ok": True}


@router.post("/{emotion_id}/daily-logs/{log_id}")
def link_emotion_to_daily_log(
    emotion_id: int,
    log_id: int,
    session: SessionDep,
    current_user: JwtPayload = Depends(get_current_user),
):
    link = DailyLogEmotionLink(daily_log_id=log_id, emotion_id=emotion_id)
    session.add(link)
    session.commit()
    return {"ok": True, "message": f"Emotion {emotion_id} linked to DailyLog {log_id}"}
