from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, auth, database

router = APIRouter(prefix="/api/data", tags=["data"])

@router.post("/add-memory", response_model=schemas.MemoryResponse)
def add_memory(memory: schemas.MemoryCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    new_memory = models.Memory(**memory.dict(), user_id=current_user.id)
    db.add(new_memory)
    db.commit()
    db.refresh(new_memory)
    return new_memory

@router.get("/memories", response_model=list[schemas.MemoryResponse])
def get_memories(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    if not current_user.couple_id:
        return db.query(models.Memory).filter(models.Memory.user_id == current_user.id).order_by(models.Memory.date.desc()).all()
        
    users = db.query(models.User).filter(models.User.couple_id == current_user.couple_id).all()
    user_ids = [u.id for u in users]
    memories = db.query(models.Memory).filter(models.Memory.user_id.in_(user_ids)).order_by(models.Memory.date.desc()).all()
    return memories

@router.post("/add-conflict", response_model=schemas.ConflictResponse)
def add_conflict(conflict: schemas.ConflictCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    new_conflict = models.Conflict(**conflict.dict(), user_id=current_user.id)
    db.add(new_conflict)
    db.commit()
    db.refresh(new_conflict)
    return new_conflict

@router.get("/conflicts", response_model=list[schemas.ConflictResponse])
def get_conflicts(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    if not current_user.couple_id:
        return db.query(models.Conflict).filter(models.Conflict.user_id == current_user.id).order_by(models.Conflict.date.desc()).all()
        
    users = db.query(models.User).filter(models.User.couple_id == current_user.couple_id).all()
    user_ids = [u.id for u in users]
    conflicts = db.query(models.Conflict).filter(models.Conflict.user_id.in_(user_ids)).order_by(models.Conflict.date.desc()).all()
    return conflicts

@router.post("/add-weekly-check", response_model=schemas.WeeklyCheckResponse)
def add_weekly_check(check: schemas.WeeklyCheckCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    new_check = models.WeeklyCheck(**check.dict(), user_id=current_user.id)
    db.add(new_check)
    db.commit()
    db.refresh(new_check)
    return new_check

@router.get("/weekly-checks", response_model=list[schemas.WeeklyCheckResponse])
def get_weekly_checks(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    if not current_user.couple_id:
        return db.query(models.WeeklyCheck).filter(models.WeeklyCheck.user_id == current_user.id).order_by(models.WeeklyCheck.date.desc()).all()
        
    users = db.query(models.User).filter(models.User.couple_id == current_user.couple_id).all()
    user_ids = [u.id for u in users]
    checks = db.query(models.WeeklyCheck).filter(models.WeeklyCheck.user_id.in_(user_ids)).order_by(models.WeeklyCheck.date.desc()).all()
    return checks
