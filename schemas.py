from pydantic import BaseModel


class ResearchRequest(BaseModel):
    topic: str


class ResearchStartResponse(BaseModel):
    job_id: str
    status: str
    message: str


class ResearchStatusResponse(BaseModel):
    job_id: str
    status: str
    topic: str


class ResearchReportResponse(BaseModel):
    job_id: str
    status: str
    topic: str
    report: str
    feedback: str