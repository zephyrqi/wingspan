from env import WingspanEnv

env = WingspanEnv()
state = env.reset()
print("state:", state)

bird = env._get_bird(2)
print("bird 2:", bird)


obs, reward, done, info = env.step("gain_food", food_type = "invertebrate")