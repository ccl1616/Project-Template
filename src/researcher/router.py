from fastapi import APIRouter, Depends
from researcher.schemas import ResearchProfile
from sqlalchemy.orm import Session
from typing import List
from . import service
from database import get_db

router = APIRouter()

@router.get("/researchers", response_model=List[ResearchProfile])
async def get_all_researchers(db: Session = Depends(get_db)):
    return service.get_all_research_profiles(db)
    

@router.post("/researcher")
async def create_new_researcher(db: Session = Depends(get_db)):
    raise NotImplementError

@router.delete("/researcher")
async def delete_researcher_by_id(db: Session = Depends(get_db)):
    raise NotImplementError

@router.put("/researcher")
async def update_researcher_by_id(db: Session = Depends(get_db)):
    raise NotImplementError

