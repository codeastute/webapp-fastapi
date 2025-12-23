import os 
from datetime import datetime, timezone, timedelta
from typing import Annotated, Optional
from dotenv import load_dotenv
from pydantic import BaseModel
from jose import jwt
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from api.models import User
from api.deps import db_dependency, user_dependency, bcrypt_context


load_dotenv()
SECRET_KEY = os.getenv('AUTH_SECRET_KEY')
ALGORITHM = os.getenv('AUTH_ALGORITHM')


router = APIRouter(
    prefix = '/auth',
    tags = ['auth']
)


class UserResponse(BaseModel):
    id:int
    username:str
    name:Optional[str]

class UserCreateRequest(BaseModel):
    username:str
    name:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str


def authenticate_user(db:db_dependency, username:str, password:str):
    user:User = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username:str, user_id:int, name:str, expires_delta:timedelta):
    encode = {'sub':username, 'id':user_id, 'name':name}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post('/register', status_code=status.HTTP_201_CREATED) 
async def create_user(db:db_dependency, create_user_request:UserCreateRequest):
    create_user_model = User(
        username = create_user_request.username,
        name = create_user_request.name,
        hashed_password = bcrypt_context.hash(create_user_request.password) 
    )
    db.add(create_user_model)
    db.commit()

@router.post('/token', response_model=Token)
async def login_for_access_token(db:db_dependency, form_data:Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    token = create_access_token(user.username, user.id, user.name, timedelta(minutes=20))
    return {'access_token':token, 'token_type':'bearer'}

@router.get('/me', response_model=UserResponse) 
async def get_user_me(user:user_dependency):
    """
    Returns the currently authenticated user's information
    """
    return {
        'id': user['id'],
        'username': user['username'],
        'name': user.get('name', None)
    }