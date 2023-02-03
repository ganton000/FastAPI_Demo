from typing import Optional
from enum import Enum

from pydantic import BaseModel
from datetime import datetime


class Post(BaseModel):
	topic: Optional[str]=None
	message: str
	date_posted: datetime

class PostType(Enum):
	information = "information"
	inquiry = "inquiry"
	quote = "quote"
	twit = "twit"