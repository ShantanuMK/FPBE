import os
import uuid
import asyncio
from datetime import datetime, timedelta
import googleapiclient.discovery
import googleapiclient.errors
from sqlalchemy.orm import Session

from models import VideoData
from settings import settings
from log_handler import logger


class YoutubeDataRunner:
    def __init__(self, db: Session):
        self.db = db
        self.access_key_num = settings.ACCESS_KEYS_NUM
        self.access_keys = [getattr(settings, f"ACCESS_KEY_{str(i)}") for i in range(self.access_key_num)]
        self.access_keys_idx = 0
        self.api_service_name = settings.API_SERVICE_NAME
        self.api_version = settings.API_VERSION
    
    async def video_data(self):
        """
        It fetches the latest videos from YouTube and adds them to the database.
        If a ACCESS_KEY's quota is expired, automatically from next time new key is used.
        No duplicate videos will be added in the database.
        """
        while True:
            await asyncio.sleep(settings.YOUTUBE_RUNNER_INTERVAL_SECS)
            logger.info(f"Starting getting YouTube Videos with ACCESS_KEY_{str(self.access_keys_idx)}")
            youtube = googleapiclient.discovery.build(
                                                    self.api_service_name,
                                                    self.api_version, 
                                                    developerKey=self.access_keys[self.access_keys_idx],
                                                    cache_discovery=False)
            
            utc_before_delta = datetime.utcnow() - timedelta(minutes=settings.YOUTUBE_SEARCH_TIME_DELTA_MINS)
            after_ts = (utc_before_delta).isoformat() + "Z"
            # get video from the youtube api, if qouta exhausted, switch to next key
            try:
                request = youtube.search().list(
                    type=settings.YOUTUBE_SEARCH_TYPE,
                    q=settings.YOUTUBE_SEARCH_QUERY,
                    part=settings.YOUTUBE_SEARCH_PART,
                    maxResults=settings.YOUTUBE_MAX_RESULTS,
                    order=settings.YOUTUBE_SEARCH_ORDER,
                    publishedAfter=after_ts
                )
                response = request.execute()
                # print(response)
                # if response.status_code != 200: raise Exception
            except Exception as e:
                logger.error(str(e))
                logger.error("Switching to next Access Key.")
                self.access_keys_idx += 1
                self.access_keys_idx %= self.access_key_num
                response = {}

            video_data_objects = []
            for video in response.get("items", []):
                obj = VideoData(
                    id=video["id"]["videoId"],
                    title=video["snippet"]["title"],
                    description=video["snippet"]["description"],
                    publishedat=datetime.strptime(video["snippet"]["publishedAt"], '%Y-%m-%dT%H:%M:%SZ'),
                    thumbnailsdefault=video["snippet"]["thumbnails"]["default"]["url"],
                    channeltitle=video["snippet"]["channelTitle"],
                    publishtime=datetime.strptime(video["snippet"]["publishTime"], '%Y-%m-%dT%H:%M:%SZ')
                )
                video_data_objects.append(obj)
            logger.info(f"Videos Fetched: {str(len(video_data_objects))}")
            if video_data_objects:
                try:
                    video_ids_present = [video_db_obj.id for video_db_obj in self.db.query(VideoData).filter(VideoData.publishedat >= utc_before_delta).all()]

                    videos_to_add = []
                    for video in video_data_objects:
                        if video.id not in video_ids_present:
                            videos_to_add.append(video)

                    self.db.bulk_save_objects(videos_to_add)
                    self.db.commit()
                    logger.info(f"Added {len(videos_to_add)} into database.")
                except Exception as e:
                    logger.error("Failed to add videos in database.")
