from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from datetime import datetime
import logging
from core.generator import VideoGenerator
import uuid
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Video Generator API",
    description="""
    Generate AI videos with web search capabilities.
    
    This API now uses OpenAI Swarm to perform web searches and create more up-to-date
    and factual content for your videos. The system will search the web for the latest
    information about your topic before generating the essay.
    """
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://0.0.0.0:3000",
        "http://localhost:3030",
        "http://0.0.0.0:3030",
        "http://dev.gazzaruso.com:3000",
        "https://dev.gazzaruso.com:3000",
        "http://dev.gazzaruso.com:3030",
        "https://dev.gazzaruso.com:3030"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store task status
tasks = {}

class VideoRequest(BaseModel):
    topic: str
    num_images: int = 5
    language: str = "en"
    text_model: int = 0
    image_model: int = 1
    video_length: int = 1
    openai_key: Optional[str] = None
    use_web_search: bool = True  # Nuovo parametro per abilitare/disabilitare la ricerca web

    class Config:
        use_enum_values = True
        schema_extra = {
            "example": {
                "topic": "The impact of artificial intelligence on modern society",
                "num_images": 5,
                "language": "en",
                "text_model": 0,  # 0: GPT-4, 1: GPT-3.5
                "image_model": 1,  # 0: DALL-E 2, 1: DALL-E 3
                "video_length": 1,  # 0: 30s, 1: 1min, 2: 4min
                "use_web_search": True  # Abilita la ricerca web per contenuti aggiornati
            }
        }

class TaskStatus(BaseModel):
    status: str
    current_step: str = ""
    progress: float = 0
    error: Optional[str] = None

async def generate_video_task(task_id: str, request: VideoRequest):
    try:
        # Create output directory for this task
        output_dir = os.path.join("output", task_id)
        os.makedirs(output_dir, exist_ok=True)

        # Initialize video generator with task tracking and optional API key
        generator = VideoGenerator(
            task_id=task_id,
            tasks=tasks,
            openai_key=request.openai_key
        )

        # Generate video with the given parameters
        await generator.generate(
            topic=request.topic,
            num_images=request.num_images,
            language=request.language,
            text_model=request.text_model,
            image_model=request.image_model,
            video_length=request.video_length,
            output_dir=output_dir,
            use_web_search=request.use_web_search
        )

    except Exception as e:
        logger.error(f"Error in generate_video_task: {str(e)}")
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["error"] = str(e)
        raise

@app.post("/generate")
async def generate_video(request: VideoRequest, background_tasks: BackgroundTasks):
    # Validate number of images
    if not 1 <= request.num_images <= 10:
        raise HTTPException(status_code=400, detail="Number of images must be between 1 and 10")
    
    # Create a new task ID
    task_id = str(uuid.uuid4())
    
    # Initialize task in the tasks dictionary
    tasks[task_id] = {
        "status": "queued",
        "current_step": "Initializing",
        "progress": 0,
        "created_at": datetime.now().isoformat()
    }
    
    # Add task to background tasks
    background_tasks.add_task(generate_video_task, task_id, request)
    
    return {"task_id": task_id, "status": "queued"}

@app.get("/status/{task_id}", response_model=TaskStatus)
async def get_status(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks[task_id]
    status = task.get("status", "queued")
    current_step = task.get("current_step", "")
    progress = task.get("progress", 0)
    error = task.get("error")
    
    return TaskStatus(
        status=status,
        current_step=current_step,
        progress=progress,
        error=error
    )

@app.get("/video/{task_id}")
async def get_video(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks[task_id]
    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail="Video generation not completed")
    
    video_path = os.path.join("output", task_id, f"{task_id}.mp4")
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video file not found")
    
    return FileResponse(video_path, media_type="video/mp4", filename=f"video_{task_id}.mp4")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception handler caught: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred"}
    )

# Create output directories if they don't exist
os.makedirs("output", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
