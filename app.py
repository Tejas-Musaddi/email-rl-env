from fastapi import FastAPI
from environment import EmailEnv

app = FastAPI()
env = EmailEnv(mode="easy")

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/reset")
@app.post("/reset")
def reset():
    return env.reset()