from docutils.nodes import status
from fastapi import APIRouter, Depends
from models import Like, Post
from database import Session, ENGINE
from routers.auth import session
from schemas import LikeCreateModel, LikeModel
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi_pagination import Page, paginate, add_pagination

router_likes = APIRouter(prefix="/likes", tags=["likes"])


@router_likes.get("/")
async def like_home():
    return {"message": "Like qismining Bosh sahifasiga xush kelibsiz!"}


@router_likes.get("/likes", response_model=Page[dict])
async def likes():
    likes = Session.query(Like).all()
    return paginate(likes)

add_pagination(router_likes)


@router_likes.post("/likes")
async def like(like: LikeCreateModel):
    """
    Bu funksiya shunday ishlaydiki qachinki biz instagram posttga layk bosganimizda likening ustiga bosib
    uni yaratmoqchi bo'lsak u layk olib tashlanadi agar bo'lmas, aksincha bo'lsa esa yaratiladi!
    CRUD qismining delete qismi ham umumiy ishlatilgan
    :param like:
    :return: like
    """
    check = session(Like).filter(Like.id == like.id)
    if check is not None:
        session.delete(like)
        session.commit()
        return {"message": "Like remowed!"}
    new_like = Like(
        status=like.status,
        post_id=like.post_id,
        user_id=like.user_id,
    )
    session.add(new_like)
    session.commit()
    return {"message": "Like done!"}


@router_likes.post("/like/{post_id}")
async def like_auth(post_id: int,Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()

    post = session.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    existing_like = session.query(Like).filter(Like.user_id == user_id, Like.post_id == post_id).first()

    if existing_like:
        session.delete(existing_like)
        session.commit()
        return {"detail": "Like removed"}

    new_like = Like(user_id=user_id, post_id=post_id)
    session.add(new_like)
    session.commit()
    return {"detail": "Post liked"}



