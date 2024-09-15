from database import ENGINE, Base
from models import User, Post, Comment, Stories, Like, Tags, PostTags, Message, Follow

def migrate():
    Base.metadata.create_all(ENGINE)
