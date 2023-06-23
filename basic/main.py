from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn
app = FastAPI()

@app.get('/')
def index():
    return {'data': {'name':'Anmol'}}

@app.get('/about')
def about():
    return {'data':'About Page'}

@app.get('/blog/{id}')
def getBlog(id:str):
    return {'data':id}

@app.get('/blog/{id}/comments')
def getBlogComments(id: int):
    return {'data':id}

# Query Parameter
@app.get('/getblog')
def getBlogByLimit(limit=10, publish:bool=True, sort: Optional[str]=None):

    return {'data': f'{limit} blogs from db'}


#Blog data model
class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

    
@app.post('/blog')
def createBlog(request: Blog):
    return {'data': "Blog model created with title {blog.title}"}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1",port=9000)