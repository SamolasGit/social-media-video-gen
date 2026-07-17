from fastapi import FastAPI
from pydantic import BaseModel
from celery import Celery


app = FastAPI()


# -----------------------------
# Celery connection
# -----------------------------

celery = Celery(
    "api",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",   # <-- add this line
)


# -----------------------------
# Request model
# -----------------------------

class VideoRequest(BaseModel):

    theme: str
    guide: str = ""

    prompt: str = "reddit_story"
    instruction: str = "tiktok"

    voice: str = "alloy"

    subtitle_style: str = "tiktok"

    background_video: str = "assets/videos/minecraft.mp4"


# -----------------------------
# Health check
# -----------------------------

@app.get("/")
def home():

    return {
        "status": "API running"
    }


# -----------------------------
# Generate video
# -----------------------------

@app.post("/generate")
def generate_video(request: VideoRequest):

    data = request.model_dump()


    job = celery.send_task(
        "generate_video",
        args=[data]
    )


    return {
        "job_id": job.id,
        "status": "queued"
    }


# -----------------------------
# Job status
# -----------------------------

@app.get("/status/{job_id}")
def status(job_id: str):

    result = celery.AsyncResult(job_id)


    return {
        "job_id": job_id,
        "status": result.status,
    }