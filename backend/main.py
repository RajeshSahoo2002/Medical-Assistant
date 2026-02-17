from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from middlewares.exception_handler import catch_exception_middleware
from routes.upload_pdf import router as upload_router
from routes.user_questions import router as user_router

app=FastAPI(title="AI Medical Assistant", description="API for RAG Powered AI Chatbot")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Middle ware exception handlers
app.middleware("http")(catch_exception_middleware)

# Routers

#1. router to upload pdf documents
app.include_router(upload_router)
#2. router to ask query by the user
app.include_router(user_router)