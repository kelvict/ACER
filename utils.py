import plotly
from plotly.graph_objs import Scatter
import torch
from torch import multiprocessing as mp


# Global counter
class Counter():
  def __init__(self):
    self.val = mp.Value('i', 0)
    self.lock = mp.Lock()

  def increment(self):
    with self.lock:
      self.val.value += 1

  def value(self):
    with self.lock:
      return self.val.value


# Converts a state from the OpenAI Gym (a numpy array) to a batch tensor
def state_to_tensor(state):
  return torch.from_numpy(state).float().unsqueeze(0)


# Converts an index and size into a one-hot batch tensor
def action_to_one_hot(action_index, action_size):
  action = torch.zeros(1, action_size)
  action[0, action_index[0, 0]] = 1
  return action


# Creates an extended input (state + previous action + reward + timestep)
def extend_input(state, action, reward, timestep, volatile=False):
  reward = torch.Tensor([reward]).unsqueeze(0)
  timestep = torch.Tensor([timestep]).unsqueeze(0)
  return torch.cat((state, action, reward, timestep), 1)


def plot_line(xs, ys):
  plotly.offline.plot({
    'data': [Scatter(x=xs, y=ys)],
    'layout': dict(title='Rewards',
                   xaxis={'title': 'Step'},
                   yaxis={'title': 'Total Reward'})
  }, filename='rewards.html', auto_open=False)
