from fastapi import FastAPI
from services.authenticate.routes import auth_router

app = FastAPI(title='Test App')
app.include_router(auth_router)
