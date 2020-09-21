import gym
import numpy as np
from ddqn import DDQNAgent
from utils import plot_learning_curve, make_env

if __name__ == '__main__':
    env = make_env()
    best_score = -np.inf
    load_checkpoint = False
    n_games = 100
    agent = DDQNAgent(gamma = 0.99, epsilon=1.0, lr=0.001,
                      input_dims = (env.observation_space.shape),
                      n_actions = env.action_space.n, memory_size=5000,
                      episode_min = 0.1, batch_size=32, replace=10000,
                      episode_dec = 1e-5, check_point_dir = 'models',
                      algorithm='DDQNAgent', env_name='PongNoFrameskip-v4')

    if load_checkpoint:
        agent.load_models()

    fname = agent.algorithm + '_' + agent.env_name + '_lr' + str(agent.lr) + \
        '_' + str(n_games) + 'agmes'
    figure_file = 'plots/' + 'fname' + './png'
    n_steps = 0
    scores, episode_history, steps_array = [], [], []

    for i in range(n_games):
        done = False
        observation = env.reet()
        score = 0
        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done, info = env.step(action)
            score += reward
            if not load_checkpoint:
                agent.store_transition(observation, action, reward, observation_, int(done))
                agent.learn()
            observation = observation_
            n_steps += 1
        scores.append(score)
        steps_array.append(n_steps)
        avg_score = np.mean(scores[-100:])
        print('episode: ', i, 'score: ', score,
              'averate score %.1f' % avg_score, 'best score %.2f' % best_score,
              'epsilon %.2f' % agent.epsilon, 'steps', n_steps)

        if avg_score > best_score:
            best_score = avg_score

        episode_history.append(agent.epsilon)
        if load_checkpoint and n_steps >= 18000:
            break

    x = [i+1 for i in range(len(scores))]
    plot_learning_curve(steps_array, scores, episode_history, figure_file)