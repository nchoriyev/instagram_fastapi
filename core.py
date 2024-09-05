from fastapi import FastAPI, Depends, status

from database import Session, ENGINE
from routers.auth import auth_router
from routers.post import router_post
from routers.comment import router_comment
from routers.like import router_likes
from fastapi_jwt_auth import AuthJWT
from schemas1.auth import Settings
from fastapi.exceptions import HTTPException
from models import User

apps = FastAPI()
apps.include_router(auth_router)
apps.include_router(router_post)
apps.include_router(router_comment)
apps.include_router(router_likes)

session = Session(bind=ENGINE)


@AuthJWT.load_config
def get_config():
    return Settings()


def get_current_user(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_id = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user


@apps.get("/")
async def home():
    return {"message": "Assalomu aleykum asosiy sahifaga xush kelibsiz!!"}
