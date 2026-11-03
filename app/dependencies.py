from app.core.database import get_session

from typing import Annotated
from sqlmodel import Session
from fastapi import Depends


SessionDep = Annotated[Session, Depends(get_session)]