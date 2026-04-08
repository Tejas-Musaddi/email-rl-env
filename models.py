from pydantic import BaseModel

class Observation(BaseModel):
    email_text: str
    sender: str
    subject: str
    step_count: int

class Action(BaseModel):
    category: str
    priority: str
    action: str

class Reward(BaseModel):
    score: float
    reason: str