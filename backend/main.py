from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import *

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

v1_router = APIRouter(prefix="/v1") #API versioning

@v1_router.get("/health")
async def health_check():
    return {"status": "ok"}

# adding user routes to the v1 router
v1_router.include_router(user_router)
# adding menu routes to the v1 router
v1_router.include_router(menu_router)
# adding cart routes to the v1 router
v1_router.include_router(cart_router)
# adding order routes to the v1 router
v1_router.include_router(order_router)

# adding v1 router to the main app
app.include_router(v1_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}