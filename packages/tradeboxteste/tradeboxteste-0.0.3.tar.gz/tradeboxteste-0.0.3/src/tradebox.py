import pandas as pd
import numpy as np
import gym
from gym import spaces
from gym.utils import seeding

class TradeBox(gym.Env):
	def __init__(self, filename):
		super(TradeBox, self).__init__()
		self.stp = 0
		self.csv_file = pd.read_csv(filename)
		self.action_space = spaces.Discrete(3)
		self.pre_max = self.csv_file['Preço'].max()
		self.pre_min = self.csv_file['Preço'].min()
		self.qtd_max = self.csv_file['QTD'].max()
		self.qtd_min = self.csv_file['QTD'].min()
		self.max_pre_max = self.csv_file['Pmax'].max()
		self.min_pre_min = self.csv_file['Pmin'].min()
		self.max_pre_min = self.csv_file['Pmax'].min()
		self.min_pre_max = self.csv_file['Pmin'].max()
	

		self.low = np.array(
		    [self.pre_min, self.qtd_min, self.csv_file['Abertura'].min() ,self.min_pre_min, self.max_pre_min], dtype=np.float32
		)
		self.high = np.array(
		    [self.pre_max, self.qtd_max, self.csv_file['Abertura'].max(), self.min_pre_max, self.max_pre_max], dtype=np.float32
		)

		self.observation_space  = spaces.Box(
		    self.low, self.high, dtype=np.float32
		)

		
		

	def step(self, action):
		state = self.csv_file[['Preço','QTD','Abertura','Pmax','Pmin']].iloc[self.stp].values
		next_state = self.csv_file[['Preço','QTD','Abertura','Pmax','Pmin']].iloc[self.stp+1].values

		#a = 0 vender
		#a = 1 comprar
		#a = 2 segurar
		if action == 0 and state[0] <= next_state[0]:
			reward = -1

		if action == 0 and state[0] > next_state[0]:
			reward = 1

		if action == 1 and state[0] <= next_state[0]:
			reward = 1

		if action == 1 and state[0] > next_state[0]:
			reward = -1

		if action ==2:
			reward = -50

		self.stp+=1
		
		done = finish()
		info = ''
		return next_state, reward, done, info


	def finish(self):
		if self.stp == (len(self.csv_file)-1):
			self.stp = 0
			return True
		else:
			return False


	def reset(self):
		self.stp = 0
		return self.csv_file[['Preço','QTD','Abertura','Pmax','Pmin']].iloc[self.stp].values



