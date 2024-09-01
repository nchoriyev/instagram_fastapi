from docutils.nodes import status
from fastapi import APIRouter
from models import Like
from database import Session, ENGINE
from routers.auth import session
from schemas import LikeCreateModel, LikeModel
from fastapi.exceptions import HTTPException

router_likes = APIRouter(prefix="/likes", tags=["likes"])


@router_likes.get("/")
async def like_home():
    return {"message": "Like qismining Bosh sahifasiga xush kelibsiz!"}


@router_likes.get("/likes")
async def likes():
    likes = Session.query(Like).all()
    return likes


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


