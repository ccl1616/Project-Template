from sqlalchemy import select
from sqlalchemy.orm import Session
from researcher.models import ResearchProfile
from fastapi_pagination.ext.sqlalchemy import paginate
def get_research_profile_by_id(db: Session, researcher_id: int):
    return db.query(ResearchProfile).filter(ResearchProfile.id == researcher_id).first()


def get_all_research_profiles(db: Session, skip:int=0, limit:int=100):
    return paginate(db, select(ResearchProfile).order_by(ResearchProfile.id))


def create_research_profile(db: Session, research_profile: ResearchProfile):
    new_research_profile = ResearchProfile(
       google_scholar_link = research_profile.google_scholar_link,
       personal_website_link = research_profile.personal_website_link,
       organization = research_profile.organization,
       title = research_profile.title,
       age = research_profile.age,
       sex = research_profile.sex
    )
    db.add(new_research_profile)
    db.commit()
    db.refresh(new_research_profile)
    return new_research_profile

def delete_research_profile_by_id(db: Session, researcher_id: int):
    db.query(ResearchProfile).filter(ResearchProfile.id == researcher_id).delete()
    db.commit()
    return

