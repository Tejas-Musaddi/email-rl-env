from tasks import EMAILS
from grader import grade_action

MAX_STEPS = 10

class EmailEnv:
    def __init__(self, mode="easy"):
        self.mode = mode
        self.dataset = EMAILS[mode]
        self.index = 0
        self.step_count = 0

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

        score, _ = grade_action(action, self.current, self.step_count)

        self.index += 1
        done = self.index >= len(self.dataset) or self.step_count >= MAX_STEPS

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
        return self.current