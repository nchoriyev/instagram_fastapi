from docutils.nodes import status
from fastapi import APIRouter
from models import Follow
from database import Session, ENGINE
from schemas import FollowerModel, FollowCreateModel
from fastapi.exceptions import HTTPException

session = Session(bind=ENGINE)

router_follow = APIRouter(prefix="/follow", tags=["Follow"])


@router_follow.get("/")
async def main_page_follow():
    return {"message": "Followerlar va Followinglar bosh qismiga xush kelibsiz!"}


@router_follow.get("/follows")
async def all_follows():
    follows = session.query(Follow).all()
    return follows


@router_follow.post("/to_follow")
async def follow_user(follow: FollowCreateModel):
    check = session(Follow).filter(Follow.id == follow.id).first()
    if check is not None:
        session.delete(follow)
        session.commit()
        return {"message": "Follow remowed succesfully!"}
    new_follow = Follow(
        follower_id=follow.follower_id,
        following_id=follow.following_id,
    )
    session.add(new_follow)
    session.commit()
    return HTTPException(status_code=201, detail="Followed succesfully!")
