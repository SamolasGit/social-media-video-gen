from celery import Celery

from video_generator import generate_video


app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)


@app.task(name="generate_video", bind=True)
def generate_video_task(self, data):

    result = generate_video(data, job_id=self.request.id)

    return {
        "video": str(result)
    }