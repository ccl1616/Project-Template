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
    

@router.get("/researcher/{researcher_id}")
async def get_researcher_by_id(researcher_id:int, db: Session = Depends(get_db)):
    return service.get_research_profile_by_id(db, researcher_id)

@router.delete("/researcher/{researcher_id}")
async def delete_researcher_by_id(researcher_id: int, db: Session = Depends(get_db)):
    return service.delete_research_profile_by_id(db, researcher_id)

@router.post("/researcher", status_code=201)
async def creat_new_researcher(research_profile: ResearchProfile, db: Session = Depends(get_db)):
    return service.create_research_profile(db, research_profile)

# Todo: put API with 202 Accepted status code
# Todo: HATEOS links in response