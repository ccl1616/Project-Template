# composite/service.py
from sqlalchemy.orm import Session
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime

from ..researcher.service import get_research_profile_by_id
from ..researcher.schemas import ResearchProfile, ResearchPaper
from .schemas import ResearcherComposite, Citation, ResearchMetrics

class ResearcherCompositeService:
    def __init__(self, db: Session):
        self.db = db

    # Task 3. Synchronous implementation
    def get_researcher_composite_sync(
        self,
        researcher_id: int,
        include_papers: bool = True,
        include_metrics: bool = True
    ) -> ResearcherComposite:
        """
        Get researcher data synchronously with sub-resources
        """
        # Get base profile using existing service
        profile = get_research_profile_by_id(self.db, researcher_id)
        
        papers = None
        metrics = None
        citations = None
        
        if include_papers:
            papers = self._get_papers_sync(researcher_id)
            citations = self._get_citations_sync(researcher_id)
        
        if include_metrics:
            metrics = self._get_metrics_sync(researcher_id)
            
        return ResearcherComposite(
            profile=profile,
            papers=papers,
            metrics=metrics,
            citations=citations
        )

    # Task 4. Asynchronous implementation
    async def get_researcher_composite_async(
        self,
        researcher_id: int,
        include_papers: bool = True,
        include_metrics: bool = True
    ) -> ResearcherComposite:
        """
        Get researcher data asynchronously with sub-resources
        """
        # Get base profile
        profile = get_research_profile_by_id(self.db, researcher_id)
        
        tasks = []
        if include_papers:
            tasks.extend([
                self._get_papers_async(researcher_id),
                self._get_citations_async(researcher_id)
            ])
        
        if include_metrics:
            tasks.append(self._get_metrics_async(researcher_id))
        
        # Execute all tasks in parallel if any exist
        results = await asyncio.gather(*tasks) if tasks else []
        
        # Map results based on included data
        papers = results[0] if include_papers else None
        citations = results[1] if include_papers else None
        metrics = results[-1] if include_metrics else None
        
        return ResearcherComposite(
            profile=profile,
            papers=papers,
            metrics=metrics,
            citations=citations
        )