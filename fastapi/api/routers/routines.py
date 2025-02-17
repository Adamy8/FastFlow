from pydantic import BaseModel
from typing import List, Optional
from fastapi import APIRouter
from sqlalchemy.orm import joinedload
from api.models import Workout, Routine
from api.deps import db_dependency, user_dependency

router = APIRouter(
    prefix="/routines",
    tags=["routines"],
    # dependencies=[user_dependency]
)

class RoutineBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoutineCreate(RoutineBase):
    workouts: List[int] = []

@router.get("/")    # get all
def get_routines(db: db_dependency, user: user_dependency):
    return db.query(Routine).options(joinedload(Routine.workouts)).filter(Routine.user_id == user.get('id')).all()  # only get your own routines

@router.post("/")
def create_routine(db: db_dependency, user: user_dependency, routine: RoutineCreate):
    new_routine = Routine(name=routine.name, description=routine.description, user_id=user.get('id'))
    for workout_id in routine.workouts:
        workout = db.query(Workout).filter(Workout.id == workout_id).first()
        if workout:
            new_routine.workouts.append(workout)
    db.add(new_routine)
    db.commit()
    db.refresh(new_routine)
    new_routine = db.query(Routine).options(joinedload(Routine.workouts)).filter(Routine.id == new_routine.id).first()
    return new_routine

@router.delete("/")
def delete_routine(db: db_dependency, user: user_dependency, routine_id: int):
    routine = db.query(Routine).filter(Routine.id == routine_id, Routine.user_id == user.get('id')).first()   # can only delete your own routines
    if routine:
        db.delete(routine)
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Routine with id {routine_id} not found or does not belong to you."
        )
    return routine
