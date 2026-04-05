from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, auth, database, ai

router = APIRouter(prefix="/api/analysis", tags=["analysis"])

@router.get("/bond-score")
def get_bond_score(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    if not current_user.couple_id:
        return {"error": "Not part of a couple yet"}
        
    users = db.query(models.User).filter(models.User.couple_id == current_user.couple_id).all()
    user_ids = [u.id for u in users]
    
    memories = db.query(models.Memory).filter(models.Memory.user_id.in_(user_ids)).all()
    conflicts = db.query(models.Conflict).filter(models.Conflict.user_id.in_(user_ids)).all()
    checks = db.query(models.WeeklyCheck).filter(models.WeeklyCheck.user_id.in_(user_ids)).all()
    
    m_data = [{"title": m.title, "emotion": m.emotion} for m in memories[-10:]] # Only feed last 10 to standard prompt length
    c_data = [{"reason": c.reason, "severity": c.severity, "resolved": c.resolved} for c in conflicts[-5:]]
    w_data = [{"mood": w.mood, "conflict_status": w.conflict_status} for w in checks[-5:]]
    
    analysis = ai.analyze_relationship(m_data, c_data, w_data)
    return analysis
