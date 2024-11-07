from fastapi import APIRouter, Depends, status, HTTPException
from app.backend.db_depends import get_db
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session
from typing import Annotated
from app.models import Task, User
from app.schemas import CreateTask, UpdateTask, CreateUser

router = APIRouter(prefix='/task', tags=['task'])


@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks


@router.get('/task_id')
async def task_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    task = db.scalar(select(Task).where(Task.id == user_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )


@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CreateTask, user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    db.execute(insert(Task).values(title=create_task.title,
                                   content=create_task.content,
                                   priority=create_task.priority,
                                   user_id=user_id
                                   ))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)], update_user: UpdateTask, user_id: int):
    user = db.scalar(select(Task).where(Task.user_id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    db.execute(update(Task).where(Task.user_id == user_id).values(
        title=update_user.firstname,
        content=update_user.lastname,
        priority=update_user.age
    ))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task update is successful'
    }


@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], id: int):
    user = db.scalar(select(Task).where(Task.id == id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )
    db.execute(delete(Task).where(Task.id == id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task delete is successful'
    }
