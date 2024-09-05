from pydantic import BaseModel
from typing import Optional, List

from sqlalchemy import Boolean


class UserRegister(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    bio: str
    profile_image: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            "id": 2,
            "username": "Nodirbek",
            "email": "example@gmail.com",
            "password": "1234ab",
            "bio": "Nothing",
            "profile_image": "url",
            "is_staff": False,
            "is_active": True,
        }


class UserLogin(BaseModel):
    username: Optional[str]
    password: Optional[str]


class UserPasswordReset(BaseModel):
    password: str


class CreatePostModel(BaseModel):
    user_id: Optional[int]
    image_url: Optional[str]
    caption: Optional[str]


class PostModel(BaseModel):
    user_id: Optional[int]
    image_url: Optional[str]
    caption: Optional[str]


class CommentCreateModel(BaseModel):
    post_id: Optional[int]
    user_id: Optional[int]
    comment_text: Optional[str]


class CommentModel(BaseModel):
    id: int
    post_id: Optional[int]
    user_id: Optional[int]
    comment_text: Optional[str]


class LikeModel(BaseModel):
    status: Optional[bool]
    user_id: Optional[int]
    post_id: Optional[int]


class LikeCreateModel(BaseModel):
    status: Optional[bool]
    user_id: Optional[int]
    post_id: Optional[int]


class FollowerModel(BaseModel):
    follower_id: Optional[int]
    following_id: Optional[int]


class FollowCreateModel(BaseModel):
    follower_id: Optional[int]
    following_id: Optional[int]


class TagsModel(BaseModel):
    pass


class TagsCreateModel(BaseModel):
    pass


class PostTagsModel(BaseModel):
    pass


class StoriesModel(BaseModel):
    pass


class StoriesCreateModel(BaseModel):
    pass
