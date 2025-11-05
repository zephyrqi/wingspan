import json
from pathlib import Path
from copy import deepcopy


class WingspanEnv:
    def __init__(self):
        # load data
        base_path = Path(__file__).parent / "data"
        with open(base_path / "birds.json", "r") as f:
            self.birds = json.load(f)["birds"]
        with open(base_path / "actions.json", "r") as f:
            self.actions = json.load(f)["actions"]

        # define food types used in this simplified game
        self.food_types = ["invertebrate", "rodent", "fish", "seed", "fruit"]

    def reset(self):
        self.turn = 0
        self.max_turns = 20  # arbitrary episode length for now

        self.state = {
            "food": {ft: 0 for ft in self.food_types},
            "hand": [b["id"] for b in self.birds[:2]],
            "board": [],
            "score": 0,
        }
        return self._obs()

    def _obs(self):
        # return a copy so outside code can't mutate internal state by accident
        return deepcopy(self.state)

    def _get_bird(self, bird_id):
        for b in self.birds:
            if b["id"] == bird_id:
                return b
        return None

    # ---------- NEW PART: step ----------
    def step(self, action, **kwargs):
        """
        action: str, one of: "gain_food", "play_bird"
        kwargs: extra info, e.g. food_type="invertebrate", bird_id=1
        """
        assert action in self.actions, f"Unknown action: {action}"
        spec = self.actions[action]

        reward = 0.0

        if spec["type"] == "gain_food":
            food_type = kwargs.get("food_type", "invertebrate")
            if food_type not in self.food_types:
                food_type = "invertebrate"
            amount = spec.get("amount", 1)
            self.state["food"][food_type] += amount
            # tiny reward so agent doesn't get 0 all the time
            reward = 0.01

        elif spec["type"] == "play_bird":
            bird_id = kwargs.get("bird_id", None)
            if bird_id is not None and bird_id in self.state["hand"]:
                bird = self._get_bird(bird_id)
                cost = bird.get("food_cost", {})
                if self._can_pay_food(cost):
                    self._pay_food(cost)
                    self.state["hand"].remove(bird_id)
                    self.state["board"].append(bird_id)
                    pts = float(bird.get("points", 0))
                    self.state["score"] += pts
                    reward = pts
                # else: not enough food → do nothing, reward stays 0

        # advance time
        self.turn += 1
        done = self.turn >= self.max_turns

        return self._obs(), reward, done, {}

    def _can_pay_food(self, cost_dict):
        for ft, amt in cost_dict.items():
            if self.state["food"].get(ft, 0) < amt:
                return False
        return True

    def _pay_food(self, cost_dict):
        for ft, amt in cost_dict.items():
            self.state["food"][ft] -= amt


if __name__ == "__main__":
    env = WingspanEnv()
    obs = env.reset()
    print("initial:", obs)

    # test sequence
    obs, r, done, _ = env.step("gain_food", food_type="invertebrate")
    print("after gain_food:", obs, r, done)

    # try to play bird 1
    obs, r, done, _ = env.step("play_bird", bird_id=1)
    print("after play_bird:", obs, r, done)