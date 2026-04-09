import os
from openai import OpenAI
from environment import EmailEnv
from models import Action

# =========================
# ENV VARIABLES
# =========================
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

# =========================
# OPENAI CLIENT
# =========================
client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

# =========================
# ACTION PARSER
# =========================
def parse_action(text: str):
    text = (text or "").lower()

    return Action(
        category="spam" if "spam" in text else "work",
        priority="high" if "urgent" in text else "low",
        action="delete" if "spam" in text else "reply"
    )

# =========================
# MAIN LOOP
# =========================
def run():
    env = EmailEnv(mode="all")
    obs = env.reset()

    print(f"[START] task=full-triage env=email-env model={MODEL_NAME}")

    rewards = []
    step = 0
    success = True

    try:
        done = False

        while not done:
            step += 1

            # LLM call
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "user",
                        "content": f"""
You are an email assistant.

Given:
{obs}

Return:
category (spam/work/personal),
priority (high/medium/low),
action (reply/delete/archive/flag)
"""
                    }
                ]
            )

            text = response.choices[0].message.content

            # Safe parsing
            try:
                action = parse_action(text)
            except Exception:
                action = Action(category="work", priority="low", action="archive")

            # Environment step
            obs, reward, done, _ = env.step(action)

            reward_val = round(reward.score, 2)
            rewards.append(reward_val)

            print(
                f"[STEP] step={step} "
                f"action={action.dict()} "
                f"reward={reward_val:.2f} "
                f"done={'true' if done else 'false'} "
                f"error=null"
            )

    except Exception as e:
        success = False
        print(
            f"[STEP] step={step} action=error "
            f"reward=0.00 done=true error={str(e)}"
        )

    # =========================
    # SCORE CALCULATION (MANDATORY)
    # =========================
    total_reward = sum(rewards)
    score = total_reward / max(1, len(rewards))
    score = min(max(score, 0.0), 1.0)

    rewards_str = ",".join(f"{r:.2f}" for r in rewards)

    print(
        f"[END] success={'true' if success else 'false'} "
        f"steps={step} score={score:.2f} rewards={rewards_str}"
    )

# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    run()
