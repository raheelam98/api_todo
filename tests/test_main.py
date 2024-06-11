from fastapi.testclient import TestClient
from sqlmodel import Session
import pytest

from todo_backend.main import app
from todo_backend.db_connector import test_create_db_tables, test_engine, get_session 

#####   pip install pytest


#### ==================== fixture ==================== #####

# https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/?h=test

@pytest.fixture(name="session")
def session_fixture():
    test_create_db_tables()
    with Session(test_engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):   
    def get_session_override():
        return session  
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


#### ==================== read main file ==================== #####
    

#### function to read main file
    
def test_read_main():
    #create TestClind for the fastapi app
    clinet = TestClient(app=app)
    response = clinet.get('/')
    assert response.status_code == 200
    assert response.json() == {'Fast API' : 'Todo Api'}

#### ==================== Get Data From Test Database ==================== #####


#### get todo from test-db
    
def test_get_todo(client : TestClient):
    response = client.get('/api_get_todos')
    assert response.status_code == 200   
     

#### ==================== Add Data Into Test Database ==================== #####

#### add todo into test-db

def test_add_in_db(client: TestClient):
    add_new_todo: str = "Operational Research"
    is_complete: bool = True
    
    # Ensure the response is assigned before accessing it
    response = client.post("/api_todos_test/", json={"todo_name": add_new_todo, "is_complete": is_complete})
    
    # Check that the status code is 200
    assert response.status_code == 200
    
    # Extract the JSON data from the response
    data = response.json()
    
    # Validate the data returned from the response
    assert data["todo_name"] == add_new_todo
    assert data["is_complete"] == True


#### ==================== Update Data From Test Database  ==================== ##### 

def test_update_todo_new(client : TestClient):
   
    id = 13  # todo id for testing
    test_name = "Discrete Mathematics"  # update todo name

    # Make the PUT request
    response = client.put(f'/api_update_todo_test?todo_id={id}', json=test_name)

    # Check the response
    assert response.status_code == 200  


#### ==================== Delete Data From Test Database (hero) ==================== ##### 

def test_delete_todo(client : TestClient):

        todo_id = 16
        response = client.delete(f'/api_delete_todo_hero/{todo_id}')
        assert response.status_code == 200

        for ids in response.json():
            assert  ids
            print(ids)

#### https://sqlmodel.tiangolo.com/tutorial/delete/
####  https://sqlmodel.tiangolo.com/tutorial/fastapi/delete/?h=dele   

 #### ==================== not working Add Data Into Test Database ==================== #####

#### add todo into test-db

# def test_add_in_db2(client: TestClient):
#     add_new_todo: str = "Python Expert"
   
#     # Ensure the response is assigned before accessing it
#     response = client.post("/api_add_todo_test2/", json={"todo_name": add_new_todo})
    
#     # Check that the status code is 200
#     assert response.status_code == 200
    
#     # Extract the JSON data from the response
#     data = response.json()
    
#     # Validate the data returned from the response
#     assert data["todo_name"] == add_new_todo


#### ====================  Test Route NOT Working  ==================== ##### 
#### ====================  Test Route NOT Working  ==================== #####     
#### ====================  Test Route NOT Working  ==================== #####     

#### ==================== Add Data Into Test Database ==================== #####

# def test_add_in_db(client: TestClient):
#     add_new_todo: str = "Numerical Analysis"
    
#     # Ensure the response is assigned before accessing it
#     response = client.post("/api_add_todo/", json={"todo_name": add_new_todo})
    
#     # Check that the status code is 200
#     assert response.status_code == 200
    
#     # Extract the JSON data from the response
#     data = response.json()
  
#     # Validate the data returned from the response
#     assert data["todo_name"] == add_new_todo

#### ==================== Update Data From Test Database  ==================== ##### 

# def test_update_todo_new(client : TestClient):
   
#     id = 8 # todo id for testing
#     test_name = "Modren Python"  # update todo name

#     # Make the PUT request
#     response = client.put(f'/api_update_todo?todo_id={id}', json=test_name)

#     # Check the response
#     assert response.status_code == 200  
    
#### ==================== Delete Data From Test Database (hero) ==================== ##### 

# def test_delete_todo(client : TestClient):

#         todo_id = 7
#         response = client.delete(f'/api_delete_todo/{todo_id}')
#         assert response.status_code == 200

#         for ids in response.json():
#             assert  ids
#             print(ids)

