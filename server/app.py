from fastapi import FastAPI
from environment import EmailEnv
import uvicorn

app = FastAPI()

env = EmailEnv(mode="easy")

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/reset")
@app.post("/reset")
def reset():
    return env.reset()

def main():
    return app

if __name__ == "__main__":
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)
