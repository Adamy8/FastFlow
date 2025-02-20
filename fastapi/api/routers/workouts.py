from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, status, HTTPException

from api.models import Workout
from api.deps import db_dependency, user_dependency

router = APIRouter(
    prefix="/workouts",
    tags=["workouts"],
    # dependencies=[user_dependency]
)

class WorkoutBase(BaseModel):
    name: str
    description: Optional[str] = None

class WorkoutCreate(WorkoutBase):
    pass

@router.get("/")
def get_workout(db:db_dependency, user: user_dependency, workout_id: int):
    return db.query(Workout).filter(Workout.id == workout_id).first()   # , Workout.user_id == user["id"]    you can see others workouts

@router.get("/workouts")
def get_workouts(db:db_dependency, user: user_dependency):
    return db.query(Workout).all()      # .filter(Workout.user_id == user["id"])      you can see others workouts

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_workout(db:db_dependency, user: user_dependency, workout: WorkoutCreate):
    new_workout = Workout(**workout.model_dump(), user_id=user.get("id"))
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)
    return new_workout

@router.delete("/")
def delete_workout(db: db_dependency, user: user_dependency, workout_id: int):
    workout = db.query(Workout).filter(Workout.user_id == user["id"], Workout.id == workout_id).first()    # can only delete your own workouts
    if workout:
        db.delete(workout)
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workout with id {workout_id} not found or does not belong to you."
        )
    return workout