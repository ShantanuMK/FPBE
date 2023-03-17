from sqlalchemy import Column, String, DateTime
from database import Base


class VideoData(Base):
    __tablename__ = "video_data"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    publishedat = Column(DateTime, index=True)
    thumbnailsdefault = Column(String)
    channeltitle = Column(String)
    publishtime = Column(DateTime)
