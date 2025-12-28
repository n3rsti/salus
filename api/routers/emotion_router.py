from fastapi import APIRouter, HTTPException
from sqlmodel import select
from typing import List

from api.database import SessionDep
from api.models.emotion_models import Emotion, EmotionRead, EmotionCreate, EmotionUpdate
from api.models.daily_log_models import DailyLog
from api.models.daily_log_emotions_link import DailyLogEmotionLink

# This file contains API endpoints related to Emotions

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
    emotion = session.get(Emotion, emotion_id)

    if not emotion:
        raise HTTPException(status_code=404, detail="Emotion not found")

    update_data = emotion_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(emotion, key, value)

    session.add(emotion)
    session.commit()
    session.refresh(emotion)
    return emotion


@router.delete("/{emotion_id}")
def delete_emotion(session: SessionDep, emotion_id: int):
    emotion = session.get(Emotion, emotion_id)
    if not emotion:
        raise HTTPException(status_code=404, detail="Emotion not found")
    
    session.delete(emotion)
    session.commit()
    return {"ok": True}


@router.post("/{emotion_id}/daily-logs/{log_id}")
def link_emotion_to_daily_log(emotion_id: int, log_id: int, session: SessionDep):
    emotion = session.get(Emotion, emotion_id)
    daily_log = session.get(DailyLog, log_id)

    if not emotion or not daily_log:
        raise HTTPException(status_code=404, detail="Emotion or DailyLog not found")

    # Sprawdzenie, czy link już istnieje, aby uniknąć duplikatów
    link = DailyLogEmotionLink(daily_log_id=log_id, emotion_id=emotion_id)
    session.add(link)
    session.commit()
    
    return {
        "ok": True, 
        "message": f"Emotion {emotion_id} linked to DailyLog {log_id}"
    }