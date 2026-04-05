from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, schemas, auth, database
import uuid

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/signup", response_model=schemas.Token)
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(username=user.username, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = auth.create_access_token(data={"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer", "couple_id": None, "has_partner": False}

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    has_partner = False
    if user.couple_id:
        couple = db.query(models.User).filter(models.User.couple_id == user.couple_id).all()
        if len(couple) == 2:
            has_partner = True
    
    return {"access_token": access_token, "token_type": "bearer", "couple_id": user.couple_id, "has_partner": has_partner}

@router.post("/create-couple")
def create_couple(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    if current_user.couple_id:
        raise HTTPException(status_code=400, detail="Already in a couple")
    
    couple_id = str(uuid.uuid4())[:12] # somewhat short ID
    new_couple = models.Couple(id=couple_id)
    db.add(new_couple)
    db.commit()
    
    current_user.couple_id = couple_id
    db.commit()
    return {"couple_id": couple_id}

@router.post("/join-couple")
def join_couple(couple_data: schemas.CoupleJoin, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    if current_user.couple_id:
        raise HTTPException(status_code=400, detail="Already in a couple")
    
    couple = db.query(models.Couple).filter(models.Couple.id == couple_data.couple_id).first()
    if not couple:
        raise HTTPException(status_code=404, detail="Couple ID not found")
    
    users_in_couple = db.query(models.User).filter(models.User.couple_id == couple_data.couple_id).all()
    if len(users_in_couple) >= 2:
        raise HTTPException(status_code=400, detail="Couple already complete")
        
    current_user.couple_id = couple_data.couple_id
    db.commit()
    return {"message": "Joined successfully", "couple_id": couple_data.couple_id}

@router.get("/me")
def get_me(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Calculate has_partner dynamic
    has_partner = False
    if current_user.couple_id:
        users = db.query(models.User).filter(models.User.couple_id == current_user.couple_id).all()
        if len(users) == 2:
            has_partner = True
            partner = [u for u in users if u.id != current_user.id][0]
    return {
        "username": current_user.username,
        "couple_id": current_user.couple_id,
        "has_partner": has_partner,
        "partner_name": partner.username if has_partner else None
    }
