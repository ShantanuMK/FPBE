# FPBE
# FP-BE

## Basic Requirements:

- Server should call the YouTube API continuously in background (async) with some interval (say 10 seconds) for fetching the latest videos for a predefined search query and should store the data of videos (specifically these fields - Video title, description, publishing datetime, thumbnails URLs and any other fields you require) in a database with proper indexes.
- A GET API which returns the stored video data in a paginated response sorted in descending order of published datetime.
- A basic search API to search the stored videos using their title and description.
- Dockerize the project.
- It should be scalable and optimised.


## Bonus Points:

- Add support for supplying multiple API keys so that if quota is exhausted on one, it automatically uses the next available key.
- Optimise search api, so that it's able to search videos containing partial match for the search query in either video title or description.
    - Ex 1: A video with title *`How to make tea?`* should match for the search query `tea how`


## Instructions to run server.
- Clone the repository.
- change working dir: `cd app`
- Install the requirements: `pip install -r requirements.txt`
- Start the server: `python main.py`

Server will be started on http://0.0.0.0:8080 port.
On 8080/docs, Swagger will be present to view and interact with the APIs.
<br/><br/>


## /getVideos
-  This API takes optional query parameters `page_num` and `page_size` and return paginated response in descending order of published time.
<br/>

![Alt text](/Screenshot%202022-11-05%20at%201.58.30%20PM.png?raw=true "")
<br/>
<br/>

url: `http://0.0.0.0:8080/getVideos?page_num=1&page_size=2`
<br/>

response:
```
{
  "data": [
    {
      "publishedat": "2022-11-05T08:03:17",
      "id": "jWGAkI7mKp8",
      "channeltitle": "Crypto King India",
      "thumbnailsdefault": "https://i.ytimg.com/vi/jWGAkI7mKp8/default.jpg",
      "title": "Dogecoin Big urgent update Bitcoin Will pump/Dump? Ethereum latest update. crypto News today.",
      "description": "Big Crypto Dump | Bitcoin Update | Top Altcoin To Buy Now | Crypto News Today | Crypto News VIP CHANNEL ...",
      "publishtime": "2022-11-05T08:03:17"
    },
    {
      "publishedat": "2022-11-05T08:00:57",
      "id": "JJhX4_Ykfbs",
      "channeltitle": "Cat & Dog lover",
      "thumbnailsdefault": "https://i.ytimg.com/vi/JJhX4_Ykfbs/default.jpg",
      "title": "Happy Halloween🐕 #dog #dogs #doglover #doglovers #dogecoin #dogtraining #dogvideos #halloween",
      "description": "",
      "publishtime": "2022-11-05T08:00:57"
    }
  ],
  "total": 5,
  "count": 2,
  "pagination": {
    "previous": null,
    "next": "/getVideos?page_num=2&page_size=2"
  }
}
```
<br/><br/>

## /searchVideos
- This API shows the videos with title or description matching the `search_term` query param.
This is also able to search videos containing partial match for the search query in either video title or description. <br/>
Ex: when searched for `bombshell dropped`, it will also show the video whose title/description is "DOGECOIN TO $1! ELON MUSK DROPPED A BOMBSHELL ON TWITTER!" 

<br/><br/>
- ![Alt text](Screenshot%202022-11-05%20at%202.06.57%20PM.png?raw=true "")
<br/>

url: 
`
http://0.0.0.0:8080/searchVideos?search_term=bombshell%20dropped
`

<br/>

response:
```
[
  {
    "description": "DOGECOIN TO $1! ELON MUSK DROPPED A BOMBSHELL ON TWITTER! WIN $600 IN CRYPTO AND BURN LUNA CLASSIC ...",
    "thumbnailsdefault": "https://i.ytimg.com/vi/AzgLBONqgZE/default.jpg",
    "title": "DOGECOIN TO $1! ELON MUSK DROPPED A BOMBSHELL ON TWITTER!",
    "publishtime": "2022-11-03T13:00:05",
    "id": "287c0755-d1d9-41f0-bd69-50ebc5b7dceb",
    "publishedat": "2022-11-03T13:00:05",
    "channeltitle": "Crypto King"
  }
]
```

## Docker method for running the server:
- clone the repository
- `docker build -t fpbeapp .`
- `docker run --name fpbeapp -d -p 8080:8080 fpbeapp:latest`

