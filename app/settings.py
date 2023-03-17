from pydantic import BaseSettings

class _Settings(BaseSettings):

    HOST: str = "0.0.0.0"
    PORT: int = 8080

    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    YOUTUBE_SEARCH_QUERY = "dogecoin"
    YOUTUBE_SEARCH_TYPE = "video"
    YOUTUBE_SEARCH_PART = "snippet"
    YOUTUBE_SEARCH_ORDER = "date"
    YOUTUBE_MAX_RESULTS = 5

    ACCESS_KEYS_NUM = 4
    ACCESS_KEY_0 = "AIzaSyCnbJyckXIKcCEbu0fJscO9H2MSBCmkWgY"
    ACCESS_KEY_1 = "AIzaSyCVaki2rKNX5jxMWZCU5cj1hptC4cRU8bI"
    ACCESS_KEY_2 = "AIzaSyDm4BRBFqg2v5fNS5WIwfQpM7bRQGK4lQ0"
    ACCESS_KEY_3 = "AIzaSyBy32xl_iFDsZjOHPCSoc3SsYebiHo3Ubs"

    YOUTUBE_RUNNER_INTERVAL_SECS = 60
    YOUTUBE_SEARCH_TIME_DELTA_MINS = 1


settings = _Settings()
