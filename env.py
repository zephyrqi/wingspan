import json
from pathlib import Path


class WingspanEnv:
    def __init__(self):
        # Load data
        base_path = Path(__file__).parent / "data"
        with open(base_path / "birds.json", "r") as f:
            self.birds = json.load(f)["birds"]
        with open(base_path / "actions.json", "r") as f:
            self.actions = json.load(f)["actions"]

    def reset(self):
        """Initialize a fresh game state."""
        self.state = {
            "food": {},              # food inventory
            "hand": [b["id"] for b in self.birds[:2]],  # start with 2 birds
            "board": [],             # birds played
            "score": 0
        }
        return self.state

    def _get_bird(self, bird_id):
        """Find bird data by ID."""
        for b in self.birds:
            if b["id"] == bird_id:
                return b
        return None


if __name__ == "__main__":
    env = WingspanEnv()
    obs = env.reset()
    print(json.dumps(obs, indent=2))