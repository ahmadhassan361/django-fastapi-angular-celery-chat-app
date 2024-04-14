import os
import django
from django.core.asgi import get_asgi_application
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Initialize Django application
django_application = get_asgi_application()

from app.model import UserSchema, UserLoginSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

app = FastAPI()

# Configure CORS settings
origins = ["http://localhost:4200"]  # Update this with your Angular app's URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)



@app.post("/user/signup", tags=["user"])
def create_user(user: UserSchema = Body(...)):
    _sers = User.objects.all()
    print(_sers)
    user_instance, created = User.objects.get_or_create(
        username=user.email,
        email=user.email
    )
    user_instance.set_password(user.password)
    user_instance.save()

    # Return response based on whether user was created or retrieved
    if created:
        return signJWT(user.email)
    else:
        return {"message": "User already exists"}
    

from django.contrib.auth import authenticate

@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(...)):
    user__ =  authenticate(username=user.email, password=user.password)
    print(user__)
    user_ = User.objects.get(username=user.email)
    print(user.password)
    if user_.check_password(user.password):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }
