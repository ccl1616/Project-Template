from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi_pagination import Page
from fastapi_pagination.customization import CustomizedPage, UseName, UseOptionalParams, UseAdditionalFields
from src.researcher.schemas import ResearchProfile
from sqlalchemy.orm import Session
from . import service
from src.database import get_db
import time

router = APIRouter()

@router.get("/researchers", response_model=CustomizedPage[
    Page[ResearchProfile],
    UseAdditionalFields(
        link=str,
    ),
])
async def get_all_researchers(db: Session = Depends(get_db)):
    
    profiles = service.get_all_research_profiles(db)
    
    link_header = []
    page = profiles.page
    size = profiles.size
    pages = profiles.pages

    # Previous link: Check if there is a previous page
    if page > 1:
        prev_page = page - 1
        link_header.append(
            f'<{router.url_path_for("get_all_researchers")}?page={prev_page}&size={size}>; rel="prev"'
        )

    # Next link: Check if there is a next page
    if page < pages:
        next_page = page + 1
        link_header.append(
            f'<{router.url_path_for("get_all_researchers")}?page={next_page}&size={size}>; rel="next"'
        )

    # Add Link header to the response if any links were created
    if link_header:
        profiles.link = ", ".join(link_header)

    return profiles


@router.get("/researcher/{researcher_id}")
async def get_researcher_by_id(
    researcher_id: int,
    db: Session = Depends(get_db)
):
    return service.get_research_profile_by_id(db, researcher_id)


@router.delete("/researcher/{researcher_id}")
async def delete_researcher_by_id(
    researcher_id: int,
    db: Session = Depends(get_db)
):
    return service.delete_research_profile_by_id(db, researcher_id)


@router.post("/researcher", status_code=201)
async def creat_new_researcher(research_profile: ResearchProfile,
                               db: Session = Depends(get_db)):
    
    response = service.create_research_profile(db, research_profile)

    return {'link': f"{router.url_path_for('get_researcher_by_id', researcher_id = response.id)}; rel='self'"}

@router.post("/background_add_researcher", status_code=202)
async def background_add_new_researcher(research_profile: ResearchProfile, background_tasks: BackgroundTasks,
                               db: Session = Depends(get_db)):
    
    background_tasks.add_task(time.sleep, 30)
    background_tasks.add_task(service.create_research_profile, db, research_profile)

    return {'message': 'Research profile creation in progress.'}

