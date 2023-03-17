import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from log_handler import logger
from settings import settings
from youtube_runner import YoutubeDataRunner
from database import SessionLocal
from router import router

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(router, dependencies=[])

runner = YoutubeDataRunner(db = SessionLocal())

@app.on_event('startup')
async def app_startup():
    """
    It creates a task that runs the asynchronous video_data() function in the YoutubeDataRunner class
    that continously fetches data from the youtube.
    """
    logger.info("Starting Youtube Background Service.")
    asyncio.create_task(runner.video_data())
    logger.info("Successfully started Youtube Background Service!")


@app.get("/")
async def root():
    return {"message": "Welcome to FamPay BE Assignment App. Pls go to localhost:8080/docs "}

if __name__ == "__main__":
    try:
        logger.info("Starting Server")
        uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
    except Exception as e:
        logger.exception(str(e))
