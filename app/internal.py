from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from models import VideoData

def get_videos_(page_num: int, page_size: int, db: Session):
    """
    > This function takes in a page number and page size and returns a list of videos from the database
    
    :param page_num: The page number you want to get
    :type page_num: int
    :param page_size: The number of videos to return per page
    :type page_size: int
    :param db: Session = Depends(get_db)
    :type db: Session
    :return: A dictionary with the following keys:
        - data: A list of VideoData objects
        - total: The total number of videos in the database
        - count: The number of videos returned
        - pagination: A dictionary with the following keys:
            - next: The url to the next page of videos
            - previous: The url to the previous page of videos
    """
    start = (page_num - 1) * page_size
    end = start + page_size
    
    query = db.query(VideoData).order_by(VideoData.publishedat.desc())
    data = query.offset(start).limit(page_size).all()
    total_videos = db.query(VideoData).count()
    response = {
        "data": data,
        "total": total_videos,
        "page_size": page_size,
        "pagination": {}
    }

    if end >= total_videos:
        response["pagination"]["next"] = None
        response["pagination"]["previous"] = f"/getVideos?page_num={page_num-1}&page_size={page_size}" if page_num > 1 else None
    else:
        response["pagination"]["previous"] = f"/getVideos?page_num={page_num-1}&page_size={page_size}" if page_num > 1 else None
        response["pagination"]["next"] = f"/getVideos?page_num={page_num+1}&page_size={page_size}"

    return response


def search_videos_(search_term: str, db: Session):
    """
    It searches for videos that have a title or description that matches the search term
    
    :param search_term: str
    :type search_term: str
    :param db: Session - this is the database session that we created in the previous step
    :type db: Session
    :return: A list of VideoData objects
    """
    terms = [term.lower() for term in search_term.split()]
    query = db.query(VideoData).filter(or_(
        func.lower(VideoData.title).op('regexp')('|'.join(terms)),
        func.lower(VideoData.description).op('regexp')('|'.join(terms))))
    return query.all()
