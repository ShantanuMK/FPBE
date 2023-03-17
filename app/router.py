from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine
from internal import get_videos_, search_videos_

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/getVideos")
def get_videos(page_num: int | None = 1, page_size: int | None = 5, db: Session = Depends(get_db)):
    """
    It gets the videos from the database.
    
    :param page_num: int | None = 1, defaults to 1
    :type page_num: int | None (optional)
    :param page_size: The number of videos to return per page, defaults to 5
    :type page_size: int | None (optional)
    :param db: Session = Depends(get_db)
    :type db: Session
    :return: A json with list of videos and pagination details
    """
    try:
        return get_videos_(page_num, page_size, db)
    except Exception as e:
        raise HTTPException(str(e))


@router.get("/searchVideos")
def search_videos(search_term: str, db: Session = Depends(get_db)):
    """
    It searches for videos in the database and returns the results
    
    :param search_term: str - This is the search term that the user will enter
    :type search_term: str
    :param db: Session = Depends(get_db)
    :type db: Session
    :return: A list of videos
    """
    try:
        return search_videos_(search_term, db)
    except Exception as e:
        raise HTTPException(str(e))
