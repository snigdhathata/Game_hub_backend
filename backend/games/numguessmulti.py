import numpy as np
import random

class BiDirectionalGuessingRL:
    def __init__(self):
        self.Q_ai_guess = {}
        self.ai_number = random.randint(1, 100)

    # ---------- AI PART ----------
    def get_ai_state(self, low, high, level):
        return f"ai_{low}_{high}_{level}"

    def ai_choose_action(self, state, epsilon=0.1):
        if state not in self.Q_ai_guess:
            self.Q_ai_guess[state] = np.random.rand(3) * 0.5
        if np.random.random() < epsilon:
            return np.random.choice(3)
        return np.argmax(self.Q_ai_guess[state])

    def ai_get_guess(self, low, high, level):
        state = self.get_ai_state(low, high, level)
        action = self.ai_choose_action(state)

        range_size = high - low
        if action == 0:
            guess = low + int(range_size * 0.2)
        elif action == 2:
            guess = high - int(range_size * 0.2)
        else:
            guess = (low + high) // 2

        return {
            "guess": guess,
            "action": int(action),
            "q_table_size": len(self.Q_ai_guess)
        }

    # ---------- USER PART ----------
    def check_user_guess(self, guess):
        if guess == self.ai_number:
            result = "correct"
            number = self.ai_number
            self.ai_number = random.randint(1, 100)  # reset
            return {"result": result, "ai_number": number}

        elif guess < self.ai_number:
            return {"result": "lower"}

        else:
            return {"result": "higher"}

    def reset(self):
        self.ai_number = random.randint(1, 100)
