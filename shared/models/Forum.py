from typing import Optional, List
from datetime import datetime

from uuid import UUID
from pydantic import BaseModel

from .User import UserProfile
from .Post import PostType


class ForumPost(BaseModel):
	id: UUID
	topic: Optional[str] = None
	message: str
	post_type: PostType
	date_posted: datetime
	username: str

class ForumDiscussion(BaseModel):
	id: UUID
	main_post: ForumPost
	replies: Optional[List[ForumPost]] = None
	author: UserProfile