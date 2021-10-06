
from typing import Optional

from fastapi import FastAPI, Form, Request
from pydantic import BaseModel
import requests
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse


news_searching_api_url = 'http://tools.kinds.or.kr:8888/search/news'
keyword_api_url = 'http://tools.kinds.or.kr:8888/keyword'

news_searching_api = {
    "access_key": "9af2f705-2974-4340-8b55-d69040b944ab",
    "argument": {
        "query": "",
        "published_at": {
            "from": "",
            "until": ""
        },
        "provider": [""],
        "category": [""],
        "category_incident": [""],
        "byline": "",
        "provider_subject": [""],
        "subject_info": [""],
        "subject_info1": [""],
        "subject_info2": [""],
        "subject_info3": [""],
        "subject_info4": [""],
        "sort": {"date": "asc"},
        "hilight": 200,
        "return_from": 0,
        "return_size": 5,
        "fields": [
            "byline",
            "category",
            "category_incident",
            "provider_news_id",
            "hilight",
        ]
    }
}

keyword_api = {
    "access_key": "9af2f705-2974-4340-8b55-d69040b944ab",
    "argument": {
        "title": ""
    }
}

class Item(BaseModel):
    article_url: str
    title: str
    time: str

app = FastAPI()
app.mount("/static/", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

favicon_path = 'favicon.ico'


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

# @app.get("/")
# async def root():
# 	return { "message" : "Hello World" }

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("main_page.html", {"request": request, "id": None})

@app.get("/timeline/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("timeline_"+id+".html", {"request": request, "id": id})

@app.post("/items/")
async def create_item(item: Item):
    
    data = dict(item)
    
    keyword_api["argument"]["title"] = data['title']
    response = requests.post(keyword_api_url, data=json.dumps(keyword_api)).json()
    use_keyword = " AND ".join(response["return_object"]["result"]["title"].split())
    day_time = datetime.strptime('-'.join(data['time'][:10].split('.')),"%Y-%m-%d")
        
        
    news_searching_api["argument"]["query"] = data['title']
    news_searching_api["argument"]["published_at"]["from"] = str(day_time - relativedelta(days=1))[:10]
    news_searching_api["argument"]["published_at"]["until"] = str(day_time + relativedelta(days=1))[:10]


    response = requests.post(news_searching_api_url, data=json.dumps(news_searching_api))
    print(response.json())
    return response.json()



# @app.post("/items/")
# async def create_item(request: Request):
#     form_data = await request.form()
#     print(await request.form())
#     data=dict(form_data)
#     if data == {}:
#         return data
#     keyword_api["argument"]["title"] = data['title']
#     response = requests.post(keyword_api_url, data=json.dumps(keyword_api)).json()
#     use_keyword = " AND ".join(response["return_object"]["result"]["title"].split())
#     day_time = datetime.strptime('-'.join(data['time'][:10].split('.')),"%Y-%m-%d")
        
        
#     news_searching_api["argument"]["query"] = data['title']
#     news_searching_api["argument"]["published_at"]["from"] = str(day_time - relativedelta(days=1))[:10]
#     news_searching_api["argument"]["published_at"]["until"] = str(day_time + relativedelta(days=1))[:10]


#     response = requests.post(news_searching_api_url, data=json.dumps(news_searching_api))
#     print(response.json())
#     return data


