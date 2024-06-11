from fastapi import FastAPI, HTTPException, Depends, Body
from sqlmodel import  Session, select
from typing import Annotated
from contextlib import asynccontextmanager

from todo_backend.db_connector import create_db_and_tables, engine, get_session
from todo_backend.todo_models import Todo


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Crate table.... ")
    create_db_and_tables()
    yield

app = FastAPI(lifespan=life_span, title='Fast API')

@app.get('/')
def get_route_route():
    return {'Fast API' : 'Todo Api'}

## get todo from database
def get_db_todo():
    with Session(engine) as session:
        get_todos = select(Todo)
        todo_list = session.exec(get_todos).all()
        if not todo_list:
            raise HTTPException(status_code=404, detail="Todo Not Found In DB")
        else:
            return todo_list
        
@app.get('/api_get_todos', response_model=list[Todo])
def read_todos(session: Annotated[Session, Depends(get_session)]):
    todo_list = get_db_todo()
    if not todo_list:
        raise HTTPException(status_code=404, detail="Todo Not Found ...")
    else:
        return todo_list
 
## insert data into Todo
def create_db_todo(todo : str):
    with Session(engine) as session:
        select_todo = Todo(todo_name=todo)
        session.add(select_todo)
        session.commit()
        session.refresh(select_todo)
        return select_todo
       
@app.post('/api_add_todo/', response_model=Todo) 
def add_todo_route(user_todo :Annotated[str, Body()], session: Annotated[Session,Depends(get_session) ]):
    if not user_todo:
        raise HTTPException(status_code=404, detail="Todo Not Found...")
    else:
        added_todo = create_db_todo(user_todo)
        return added_todo    


## update data of Todo
def update_db_todo(user_id:int, todo_name:str, session):
    selected_todo = select(Todo).where(Todo.id == user_id)
    update_todo = session.exec(selected_todo).first()
    if not update_todo:
        raise HTTPException(status_code=404, detail=(f"Todo Id: {user_id} Not Found In DB"))
    else:
        update_todo.todo_name = todo_name
        session.add(update_todo)
        session.commit()
        session.refresh(update_todo)
        return update_todo 

@app.put('/api_update_todo', response_model=Todo)   
async def update_todo_route(id: int, todo_name: Annotated[str, Body()], session: Annotated[Session, Depends(get_session)] ):
    updated_todo = update_db_todo(id, todo_name, session)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo Not Found ....")
    return updated_todo    


## delete data from Todo    
def delete_db_todo(todo_id : int):
    with Session(engine) as session:
        db_todo = session.get(Todo, todo_id)
        if not db_todo:
            raise HTTPException(status_code=404, detail=(f"Todo Id: {todo_id} Not Found In DB"))
        session.delete(db_todo)
        session.commit()
        return db_todo
        todo_list = session.exec(select(Todo)).all()

@app.delete('/api_delete_todo/{todo_id}', response_model=Todo)
async def delete_todo_route(todo_id: int , session : Annotated[Session,Depends(get_session)]):
    delete_todo = delete_db_todo(todo_id)
    if not delete_todo:
        raise HTTPException(status_code=404, detail="Todo Not Found...")
    return delete_todo
    todo_list = session.exec(select(Todo)).all()

#### ====================  Test Route Working  ==================== ##### 
#### ====================  Test Route Working  ==================== ##### 
#### ====================  Test Route Working  ==================== #####         

@app.post("/api_todos_test/", response_model=Todo)
def create_todo(todo: Todo, session: Annotated[Session, Depends(get_session)]):
    if not todo:
        raise HTTPException(status_code=405, detail=f'Todo detail {todo} not found')
    else:
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

@app.put("/api_update_todo_test", response_model=Todo)
async def update_todo(todo_id : int, todo_name :Annotated[str, Body()], session: Annotated[Session, Depends(get_session)]):
     get_id : Todo = select(Todo).where(Todo.id == todo_id)
     update_todo = session.exec(get_id).first()
     if not update_todo:
        raise HTTPException(status_code=404, detail=(f"Todo Id: {todo_id} Not Found In DB"))
     else:
        update_todo.todo_name = todo_name
        session.add(update_todo)
        session.commit()
        session.refresh(update_todo)
        return  update_todo

@app.delete("/api_delete_todo_hero/{todo_id}/")
def delete_todo(todo_id: int, session: Annotated[Session, Depends(get_session)]):   
    todo_sel = session.get(Todo, todo_id)
    if not todo_sel:
        raise HTTPException(status_code=404, detail=(f'Todo ID {todo_id} Not Found In DB'))
    session.delete(todo_sel)
    session.commit()
    return todo_sel

### test is not working       
@app.post('/api_add_todo_test2/', response_model=Todo) 
def add_todo_route(user_todo :Annotated[str, Body()], session: Annotated[Session,Depends(get_session) ]):
    select_user_todo = Todo(todo_name=user_todo)
    session.add(select_user_todo)
    session.commit()
    session.refresh(select_user_todo)
    return select_user_todo

    # if not user_todo:
    #     raise HTTPException(status_code=404, detail="Todo Not Found...")
    # else:
        # session.add(select_user_todo)
        # session.commit()
        # session.refresh(select_user_todo)
        # return select_user_todo

        
           