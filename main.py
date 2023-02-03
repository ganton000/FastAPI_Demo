from typing import Optional, List, Dict
import random
import string

from fastapi import FastAPI
from bcrypt import checkpw, hashpw, gensalt
from uuid import UUID

from shared.models.User import User
from shared.models.UserProfile import UserProfile

app = FastAPI()

# env variables/database data
valid_users = [ "Harry", "Emily" ]
pending_users = {}
valid_profiles = {}
discussion_posts = {}


''' REST APIs '''
@app.get("/")
def index():
	return { "message": "FastAPI part 1"}

@app.get("/login/")
def login(username: str, password: str):
	user = valid_users.get(username)
	if user is None:
		return { "message": "user does not exist" }

	if checkpw(password.encode(), user.passphrase.encode()):
		return user
	else:
		return { "message": "invalid credentials!" }

@app.post("/login/signup")
def signup(username: str, password: str):
	if (username is None and password is None):
		return { "message" : "invalid user" }
	elif not valid_users.get(username) == None:
		return { "message" : "user exists!" }
	else:
		user = User(username, password)
		pending_users[username] = user
		return user

@app.delete("/login/password/change")
def change_password(username: str, old_pass: str="", new_pass: str=""):
	password_len = 8
	user = valid_users.get(username)

	if user is None:
		return { "message": "user does not exist!" }

	if old_pass == "" or new_pass == "":
		characters = string.ascii_lowercase
		temp_pass = "".join(random.choice(characters) for i in range(password_len))

		user.password = temp_pass
		user.passphrase = hashpw(temp_pass.encode(), gensalt())

		return user

	if user.password == old_pass:
		user.password = new_pass
		user.passphrase = hashpw(new_pass.encode(), gensalt())
		return user
	else:
		return { "message" : "invalid credentials" }

@app.post("/login/password/unlock")
def unlock_password(username: Optional[str]=None, id: Optional[UUID]=None):
	if username is None:
		return { "message" : "a username is required" }

	user = valid_users.get(username)

	if user is None:
		return { "message": "user does not exist!" }

	if id is None:
		return { "message": "token needed" }

	if user.id != id:
		return { "message": "invalid token" }
	else:
		return { "password": user.password }

@app.delete("/login/remove/all")
def delete_users(usernames: List[str]):
	for user in usernames:
		del valid_users[user]

	return { "message" : "deleted users" }

@app.post("/login/username/unlock")
def unlock_username(id: Optional[UUID]=None):
	if id is None:
		return { "message": "token needed" }

	for key, val in valid_users.items():
		if val.id == id:
			return { "username": val.username }

		return { "message": "user does not exist!" }

# dynamic pathing declared after fixed pathings of same base dirs
@app.get("/login/{username}/{password}")
def login_with_token(username: str, password: str, id: UUID):
	user = valid_users.get(username)

	if user is None:
		return { "message": "user does not exist" }

	if user.id != id or not checkpw(password.encode(), user.passphrase):
		return { "message": "invalid credentials" }

	return user

@app.patch("/account/profile/update/names/{username}")
def update_profile_names(id: UUID, username: str="", new_names: Optional[Dict[str,str]]=None):
	user = valid_users.get(username)

	if user is None or user.id != id:
		return { "message": "user does not exist" }

	if new_names is None:
		return { "message": "New nmes are required" }

	profile = valid_profiles[username]
	profile.firstname = new_names["firstname"]
	profile.lastname = new_names["lastname"]
	profile.middle_initial = new_names["mi"]

	valid_profiles[username] = profile

	return { "message": "successfuly updated information" }

# override existing profile
@app.put("/account/profile/update/{username}")
def update_profile(username: str, id: UUID, new_profile: UserProfile):
	user = valid_users.get(username)

	if user is None or user.id != id:
		return { "messasge": "User does not exist!" }
	else:
		valid_profiles[username] = new_profile
		return { "message": "Successfully updated profile!" }

@app.delete("/discussion/posts/remove/{username}")
def delete_discussion(username: str, id: UUID):
	user = valid_users.get(username)

	if user is None:
		return { "message": "user does not exist!" }

	if discussion_posts.get(id) is None:
		return { "message": "post does not exist!" }

	del discussion_posts[id]

	return { "message": "post was successfully deleted!" }

@app.delete("/delete/users/pending")
def delete_pending_users(accounts: List[str]=[]):
	for user in accounts:
		del pending_users[user]

	return { "message": "deleted pending users" }