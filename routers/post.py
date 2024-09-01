from urllib.request import Request

from fastapi import APIRouter

from models import Post, User
from database import Session, ENGINE
from schemas import CreatePostModel, PostModel
from fastapi.exceptions import HTTPException

session = Session(bind=ENGINE)

router_post = APIRouter(prefix="/post", tags=["post"])


@router_post.get("/")
async def home():
    return {"message": "Post Sahifasiga xush kelibsiz!!"}


@router_post.post("/posts", response_model=PostModel)
async def posts():
    posts = session.query(Post).all()
    return posts


@router_post.post("/posts")
async def create_post(post: CreatePostModel):
    check_post_id = session(Post).filter(Post.id == post.id).first()
    if check_post_id is not None:
        return HTTPException(status_code=400, detail="Post already exists")
    new_post = Post(
        user_id=post.user_id,
        image_url=post.image_url,
        caption=post.caption,
    )

    session.add(new_post)
    session.commit()
    return HTTPException(status_code=201, detail="Post created successfully!")


@router_post.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    check_post_id = session(Post).filter(Post.id == post_id).first()
    if check_post_id is None:
        return HTTPException(status_code=404, detail="Post not found")
    session.delete(check_post_id)
    session.commit()
    return HTTPException(status_code=204, detail="Post deleted successfully!")
