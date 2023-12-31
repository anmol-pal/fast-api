from fastapi import FastAPI, Depends, Response, status, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

@app.post('/blog', status_code=201)
def create(request: schemas.Blog, db:Session = Depends(get_db)):
    __tablename__ = 'blogs'
    new_blog = models.Blog(title = request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog', response_model=List[schemas.ShowBlog])
def get_all_blogs(db:Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', response_model=schemas.ShowBlog)
def get_blog_by_id(id,response:Response ,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f'{id} not available'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} not available')
    else: 
        return blog
    

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, response:Response, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id ==   id )
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with id {id} not found')
    blog.delete(synchronize_session=False)    
    db.commit() 
    return {"Done"}

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id:int, request:schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Blog with id {id} not found")
    blog.update(request.dict())
    db.commit()
    return 'updated'


@app.post('/user')
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    __tablename__ = 'users'
    new_user = models.User(request.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user