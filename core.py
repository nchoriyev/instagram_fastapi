from fastapi import FastAPI
from routers.auth import router_auth
from routers.post import router_post
from routers.comment import router_comment
from routers.like import router_likes

apps = FastAPI()
apps.include_router(router_auth)
apps.include_router(router_post)
apps.include_router(router_comment)
apps.include_router(router_likes)


@apps.get("/")
async def home():
    return {"message": "Assalomu aleykum asosiy sahifaga xush kelibsiz!!"}
