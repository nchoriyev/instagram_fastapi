from fastapi import APIRouter, status, Depends
from models import Comment, Post
from database import Session, ENGINE
from schemas import CommentCreateModel, CommentModel
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT

session = Session(bind=ENGINE)
router_comment = APIRouter(prefix="/comments", tags=["comments"])


@router_comment.get("/")
async def main():
    return {"message": "Comments Asosiy sahifasiga xush kelibsiz!!"}


@router_comment.get("/comments")
async def get_comments():
    comments = session.query(CommentModel).all()
    return comments


@router_comment.post("/comment/{post_id}")
async def comment(post_id: int, comment: CommentCreateModel, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()

    post = session.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = Comment(
        user_id=user_id,
        post_id=post_id,
        comment_text=comment.comment_text,
    )
    session.add(new_comment)
    session.commit()
    return {"detail": "Comment added"}


@router_comment.put("/comments/{id}")
async def update_comment(id: int, comment: CommentModel):
    check_id = session(Comment).filter(Comment.id == comment.id).first()
    if check_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    check_id.comment_text = comment.comment_text
    session.commit()
    session.refresh(check_id)
    return HTTPException(status_code=status.HTTP_200_OK, detail="Comment updated successfully")


@router_comment.delete("/comments/{comment_id}")
async def delete_comment(comment_id: int):
    comment = session.query(CommentModel).filter(Comment.id == comment_id).first()
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    session.delete(comment)
    session.commit()
    return {"message": "Comment deleted successfully"}
