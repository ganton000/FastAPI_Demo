from typing import Optional
from enum import Enum

from pydantic import BaseModel
from datetime import date
from uuid import UUID


class User(BaseModel):
	username: str
	password: str

class UserType(Enum):
	admin = "admin"
	teacher = "teacher"
	alumni = "alumni"
	student = "student"

class UserProfile(BaseModel):
	firstname: str
	lastname: str
	middle_initial: str
	age: Optional[int] = 0
	salary: Optional[int] = 0
	birthday: date
	user_type: UserType

class ValidUser(BaseModel):
	id: UUID
	username: str
	password: str
	passphrase: str
