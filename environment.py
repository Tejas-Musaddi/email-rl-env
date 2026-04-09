from tasks import EMAILS
from grader import grade_action

MAX_STEPS = 10


class EmailEnv:
    def __init__(self, mode="easy"):
        self.mode = mode

        # ✅ FIX: support ALL tasks
        if mode == "all":
            self.dataset = (
                EMAILS["easy"] +
                EMAILS["medium"] +
                EMAILS["hard"]
            )
        else:
            self.dataset = EMAILS[mode]

        self.index = 0
        self.step_count = 0
        self.current = None

    def reset(self):
        self.index = 0
        self.step_count = 0
        self.current = self.dataset[self.index]

        return {
            "email_text": self.current["text"],
            "sender": self.current["sender"],
            "subject": self.current["subject"],
            "step_count": 0
        }

    def step(self, action):
        self.step_count += 1

        # ✅ ALWAYS grade
        score, _ = grade_action(action, self.current, self.step_count)

        # ✅ move to next task
        self.index += 1

        done = (
            self.index >= len(self.dataset)
            or self.step_count >= MAX_STEPS
        )

        if not done:
            self.current = self.dataset[self.index]
            obs = {
                "email_text": self.current["text"],
                "sender": self.current["sender"],
                "subject": self.current["subject"],
                "step_count": self.step_count
            }
        else:
            obs = None

        return obs, float(score), done, {}

    def state(self):
        return {
            "current_email": self.current,
            "step_count": self.step_count,
            "index": self.index,
            "mode": self.mode
        }
