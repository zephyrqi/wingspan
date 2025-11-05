from env import WingspanEnv

env = WingspanEnv()
state = env.reset()
print("state:", state)

bird = env._get_bird(2)
print("bird 2:", bird)


obs, reward, done, info = env.step("gain_food", food_type = "invertebrate")
obs, reward, done, info = env.step("gain_food", food_type = "rodent")
obs, reward, done, info = env.step("gain_food", food_type = "fish")
obs, reward, done, info = env.step("gain_food", food_type = "seed")
obs, reward, done, info = env.step("gain_food", food_type = "fruit")
obs, reward, done, info = env.step("play_bird", bird_id = 1)


obs, reward, done, info = env.step("play_bird", bird_id=99)
print("\nAFTER illegal play_bird (id=99):")
print("reward:", reward)
print("obs:", obs)


print("\nAFTER gain_food:")
print("obs:", obs)
print("reward:", reward)
print("done:", done)


