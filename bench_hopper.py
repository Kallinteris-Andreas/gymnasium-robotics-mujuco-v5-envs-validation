import gymnasium as gym
from envs import hopper_v5
import numpy as np

from stable_baselines3 import TD3, PPO
from stable_baselines3.common.logger import configure
#from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.vec_env import DummyVecEnv
from my_eval import EvalCallback

RUNS = 10  # Number of Statistical Runs
TOTAL_TIME_STEPS = 1_000_000
#ALGO = TD3
ALGO = PPO
EVAL_SEED = 1234
EVAL_FREQ = 2500
EVAL_ENVS = 20

for run in range(0, RUNS):
    #env = gym.make('Hopper-v4')
    #eval_env = gym.make('Hopper-v4')
    env = gym.wrappers.TimeLimit(hopper_v5.HopperEnv(), max_episode_steps=1000)
    eval_env = gym.wrappers.TimeLimit(hopper_v5.HopperEnv(), max_episode_steps=1000)

    #eval_path = 'results/Hopper_v4_TD3/run_' + str(run)
    #eval_path = 'results/Hopper_v5_TD3/run_' + str(run)
    #eval_path = 'results/Hopper_v4_PPO/run_' + str(run)
    eval_path = 'results/Hopper_v5_PPO/run_' + str(run)

    eval_callback = EvalCallback(eval_env, seed=EVAL_SEED, best_model_save_path=eval_path, log_path=eval_path, n_eval_episodes=EVAL_ENVS, eval_freq=EVAL_FREQ, deterministic=True, render=False, verbose=True)

    model = ALGO("MlpPolicy", env, seed=run, verbose=1, device='cuda')
    model.set_logger(configure(eval_path, ["csv"]))

    model.learn(total_timesteps=TOTAL_TIME_STEPS, callback=eval_callback)

