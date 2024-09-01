from fastapi import APIRouter
from models import Comment
from database import Session, ENGINE
from schemas import CommentCreateModel, CommentModel
from fastapi.exceptions import HTTPException

session = Session(bind=ENGINE)
router_comment = APIRouter(prefix="/comments", tags=["comments"])


@router_comment.get("/")
async def main():
    return {"message": "Comments Asosiy sahifasiga xush kelibsiz!!"}


@router_comment.get("/comments")
async def get_comments():
    comments = session.query(CommentModel).all()
    return comments


@router_comment.post("/comments")
async def create_comment(comment: CommentCreateModel):
    check_id = session(Comment).filter(Comment.id == comment.id).first()
    if check_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    new_comment = Comment(
        post_id=comment.post_id,
        user_id=comment.user_id,
        comment_text=comment.comment_text,
    )
    session.add(new_comment)
    session.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED, detail="Comment created successfully")


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
