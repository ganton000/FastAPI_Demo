from typing import Optional, List, Dict

from fastapi import FastAPI
from bcrypt import checkpw
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

@app.delete("/login/remove/all")
def delete_users(usernames: List[str]):
	for user in usernames:
		del valid_users[user]

	return { "message" : "deleted users" }

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
def update_profile_names(username: str, id: UUID, new_names: Dict[str,str]):
	user = valid_users.get(username)

	if user is None or user.id != id:
		return { "message": "user does not exist" }

	if new_names is None:
		return { "message": "No parameters to update" }

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
