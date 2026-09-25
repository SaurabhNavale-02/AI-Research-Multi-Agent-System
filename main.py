from fastapi import FastAPI, BackgroundTasks,HTTPException
from pipeline import run_research_pipeline
from schemas import (
    ResearchReportResponse,
    ResearchRequest,
    ResearchStartResponse,
    ResearchStatusResponse
)
import uuid

app = FastAPI()

jobs = {}


@app.get("/")
def home():
    return {"message": "AI Research API is running"}


def run_research_job(job_id: str, topic: str):
    try:
        jobs[job_id]["status"] = "running"

        result = run_research_pipeline(topic)

        jobs[job_id]["status"] = "completed"
        jobs[job_id]["report"] = result["report"]
        jobs[job_id]["feedback"] = result["feedback"]

    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)


@app.post("/research",status_code=202,response_model=ResearchStartResponse)
def research(request: ResearchRequest, background_tasks: BackgroundTasks):

    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "status": "queued",
        "topic": request.topic
    }

    background_tasks.add_task(
        run_research_job,
        job_id,
        request.topic
    )

    return {
        "job_id": job_id,
        "status": "queued",
        "message": "Research started"
    }


@app.get("/research/{job_id}/status",response_model=ResearchStatusResponse)
def research_status(job_id: str):

    if job_id not in jobs:
        raise HTTPException(
            status_code=404,
            detail="Research job not found"
        )

    job = jobs[job_id]

    return {
        "job_id": job_id,
        "status": job["status"],
        "topic": job["topic"]
    }



@app.get("/research/{job_id}/report",response_model=ResearchReportResponse)
def research_report(job_id: str):

    if job_id not in jobs:
        raise HTTPException(
            status_code=404,
            detail="Research job not found"
        )

    job = jobs[job_id]

    if job["status"]=="queued":
        raise HTTPException(
            status_code=202,
            detail="Research is not started yet"
        )

    if job["status"]=="running":
        raise HTTPException(
            status_code=202,
            detail="Research is  still running "
        )

    if job["status"] != "completed":
        raise HTTPException(
            status_code=202,
            detail="Research is not completed yet"
        )

    if job["status"]=="failed":
        raise HTTPException(
            status_code=500,
             detail=job.get("error", "Research failed")
        )

    
    return {
        "job_id": job_id,
        "status":job["status"],
        "topic": job["topic"],
        "report": job["report"],
        "feedback": job["feedback"]
    }

