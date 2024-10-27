# composite/router.py
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from src.database import get_db # HTTP request
from ..researcher.schemas import ResearchProfile, ResearchPaper
from .service import ResearcherCompositeService
from .schemas import ResearcherComposite
import requests

router = APIRouter(
    prefix="/researcher-composite",
    tags=["researcher-composite"]
)

# by HTTP requests
@router.get("/researcher/{researcher_id}")
async def get_researcher_composite(
    researcher_id: int,
    include_papers: bool = Query(
        True, 
        description="Include research papers"
    ),
    include_scholar_metrics: bool = Query(
        True, 
        description="Include Google Scholar metrics"
    ),
    db: Session = Depends(get_db)
):
    """
    GET endpoint that fetches:
    - Base researcher profile
    - Research papers (optional)
    - Google Scholar metrics (optional)
    """
    service = ResearcherCompositeService(db)
    
    # Use httpx for async HTTP requests instead of requests
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f'http://localhost:8000/researcher/{researcher_id}')
            response.raise_for_status()  # Raise an exception for error status codes
            researcher_data = response.json()
            
            return await service.get_researcher_composite(
                researcher_id=researcher_id,
                base_profile=researcher_data,
                include_papers=include_papers,
                include_scholar_metrics=include_scholar_metrics
            )
            
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error fetching researcher data: {str(e)}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Service unavailable: {str(e)}"
            )

# 1. GET, PUT and POST for resources with sub-resources operations

@router.get("/researcher/{researcher_id}")
async def get_researcher_composite(
    researcher_id: int,
    include_papers: bool = Query(
        True, 
        description="Include research papers"
    ),
    include_scholar_metrics: bool = Query(
        True, 
        description="Include Google Scholar metrics"
    ),
    db: Session = Depends(get_db)
):
    """
    GET endpoint that fetches:
    - Base researcher profile
    - Research papers (optional)
    - Google Scholar metrics (optional)
    """
    service = ResearcherCompositeService(db)  
    return await service.get_researcher_composite(
        researcher_id,
        include_papers,
        include_scholar_metrics
    )

@router.put("/researcher/{researcher_id}")
async def update_researcher_composite(
    researcher_id: int,
    profile: ResearcherComposite,
    db: Session = Depends(get_db)
):
    """
    PUT endpoint that updates:
    - Researcher profile information
    - Associated research papers
    - Scholar metrics data
    """
    service = ResearcherCompositeService(db)
    return await service.update_researcher_composite(
        researcher_id, 
        profile
    )

@router.post("/researcher")
async def create_researcher_composite(
    profile: ResearcherComposite,
    db: Session = Depends(get_db)
):
    """
    POST endpoint that creates:
    - New researcher profile
    - Associated research papers
    - Initial scholar metrics
    """
    service = ResearcherCompositeService(db)
    return await service.create_researcher_composite(profile)

# 2. Navigation paths with query parameters

@router.get("/researcher/{researcher_id}/papers")
async def get_researcher_papers(
    researcher_id: int,
    title_contains: Optional[str] = Query(None, description="Filter papers by title"),
    has_demo: Optional[bool] = Query(None, description="Filter papers with demo videos"),
    has_website: Optional[bool] = Query(None, description="Filter papers with project websites"),
    db: Session = Depends(get_db)
):
    """
    Get researcher's papers with filters
    Example: /researcher/123/papers?title_contains=AI&has_demo=true
    """
    service = ResearcherCompositeService(db)
    return await service.get_researcher_papers(
        researcher_id,
        title_contains,
        has_demo,
        has_website
    )

@router.get("/researcher/{researcher_id}/website-links")
async def get_researcher_websites(
    researcher_id: int,
    include_scholar: bool = Query(True, description="Include Google Scholar link"),
    include_personal: bool = Query(True, description="Include personal website link"),
    db: Session = Depends(get_db)
):
    """
    Get researcher's website links
    Example: /researcher/123/website-links?include_scholar=true&include_personal=true
    """
    service = ResearcherCompositeService(db)
    return await service.get_researcher_websites(
        researcher_id,
        include_scholar,
        include_personal
    )

@router.get("/researchers/search")
async def search_researchers(
    organization: Optional[str] = Query(None, description="Filter by organization"),
    title: Optional[str] = Query(None, description="Filter by title"),
    min_age: Optional[int] = Query(None, description="Minimum age"),
    max_age: Optional[int] = Query(None, description="Maximum age"),
    sex: Optional[str] = Query(None, description="Filter by sex"),
    has_scholar_profile: Optional[bool] = Query(None, description="Has Google Scholar profile"),
    has_website: Optional[bool] = Query(None, description="Has personal website"),
    db: Session = Depends(get_db)
):
    """
    Search researchers with multiple filters
    Example: /researchers/search?organization=Stanford&title=Professor
    """
    service = ResearcherCompositeService(db)
    return await service.search_researchers(
        organization=organization,
        title=title,
        min_age=min_age,
        max_age=max_age,
        sex=sex,
        has_scholar_profile=has_scholar_profile,
        has_website=has_website
    )