"""
Authentication service for JWT token generation and password hashing
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..config import get_settings
from ..database import get_db
from ..models import Clinician
from ..schemas import TokenData

settings = get_settings()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def get_clinician_by_email(db: Session, email: str) -> Optional[Clinician]:
    """Get clinician by email"""
    return db.query(Clinician).filter(Clinician.email == email).first()


def authenticate_clinician(db: Session, email: str, password: str) -> Optional[Clinician]:
    """Authenticate a clinician"""
    clinician = get_clinician_by_email(db, email)
    if not clinician:
        return None
    if not verify_password(password, clinician.password_hash):
        return None
    return clinician


async def get_current_clinician(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Clinician:
    """Get current authenticated clinician from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    clinician = get_clinician_by_email(db, email=token_data.email)
    if clinician is None:
        raise credentials_exception
    
    return clinician
