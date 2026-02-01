from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from middlewares.exception_handler import catch_exception_middleware

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
#2. router to ask query by the user