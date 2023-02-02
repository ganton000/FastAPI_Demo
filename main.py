from fastapi import FastAPI
from bcrypt import checkpw

from shared.models.User import User

app = FastAPI()

# env variables/database data
valid_users = [ "Harry", "Emily" ]



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