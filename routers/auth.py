from fastapi import APIRouter, status
from database import Session, ENGINE
from models import User
from schemas import UserRegisterModel, UserLoginModel
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash

session = Session(bind=ENGINE)
router_auth = APIRouter(prefix="/auth", tags=["auth"])


@router_auth.get("/")
async def auth_page():
    return {"message": "Auth page"}


@router_auth.post("/login")
async def login(user: UserLoginModel):
    db_user = session.query(User).filter(User.username == user.username).first()
    if db_user is not None:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username mavjud / Username is exist !")

    if not check_password_hash(user.password, db_user.password):
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password !")
    session.close()
    return {'username': db_user.username, "message": "Login Successful!!!!!!"}


@router_auth.get("/register")
async def register_page():
    return {"message": "Register page"}


@router_auth.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserRegisterModel):
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )
    session.add(new_user)
    session.commit()
    return new_user


@router_auth.get("/users")
async def get_users():
    users = session.query(User).all()
    return users

