# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 09:15:10 2017

@author: gaurav
"""

import time
from queue import PriorityQueue

def valid_moves(state):
	valid_moves = ['Up','Down','Left','Right']
	zero_index = state.index(0)
	column_pos = zero_index%3

	if column_pos==0:valid_moves.remove('Left')
	if column_pos==2:valid_moves.remove('Right')
	if (zero_index - 3) < 0: valid_moves.remove('Up')
	if (zero_index + 3) > 8: valid_moves.remove('Down')

	return valid_moves

def neighbors(state):

	
	valid_move = valid_moves(state)
	neighbors = [None]*4	
	zero_index = state.index(0)

	for moves in valid_move:
		new_board = list(state)

		if moves =='Up':
			temp = new_board[zero_index-3]
			new_board[zero_index - 3] = new_board[zero_index]
			new_board[zero_index] = temp
			neighbors[0] = new_board

		if moves=='Down':
			new_board = list(state)
			temp = new_board[zero_index+3]
			new_board[zero_index+3] = new_board[zero_index]
			new_board[zero_index] = temp
			neighbors[1] = new_board

		if moves == 'Right':
			new_board = list(state)
			temp = new_board[zero_index+1]
			new_board[zero_index+1] = new_board[zero_index]
			new_board[zero_index] = temp
			neighbors[3] = new_board
		
		if moves == 'Left':
			new_board = list(state)
			temp = new_board[zero_index-1]
			new_board[zero_index-1] = new_board[zero_index]
			new_board[zero_index] = temp
			neighbors[2] = new_board


	return neighbors

class Node:
	def __init__(self,state,priority=0):	#state = list of config
		self.state = state
		self.priority = priority
		self.parent = None
		self.depth = 0
		self.path_cost = 0
		self.key =  "".join(str(x) for x in self.state)

	def _compare(self, other, method):
		try:
			return method(self._cmpkey(), other._cmpkey())
		except (AttributeError, TypeError):
			return NotImplemented

	def __lt__(self, other):
		return self._compare(other, lambda s,o: s < o)

	def __eq__(self,other):
		return self._compare(other,lambda s,o: s==o)

	def set_state(self,new_state):
		self.state = new_state

	def set_priority(self):
		self.priority = heur(self.state) + self.depth

	def set_parent(self,new_parent):		#parent = Node
		self.parent = new_parent

	def set_depth(self,new_depth):			
		self.depth = new_depth

	def path_cost(self,path_cost):
		self.path_cost = path_cost + 1

	def get_dir(self,new_dir):
		self.dir = new_dir

	# def add(self,node):
	# 	self.Node[node.key]=node

	# def add_to_frontierbfs(self,node):
	# 	self.fron_key_holder.append(node.key)



	# def get_stamp(self): #returns string stamp of 'self.loc'
	# 	return "".join(str(x) for x in self.state)

	def get_path(self):
		path = []
		x = self
		while x.parent != None:
			path.append(x.dir)
			x = x.parent

		return(list(reversed(path)))

	def goal_check(self):
		goal = [0,1,2,3,4,5,6,7,8]
		return(self.state == goal)

def BFS(initialState):
	frontier = []
	state=Node(initialState)
	state.set_depth(0)
	state.set_parent(None)
	frontier.append(state)
#    explored = set()
	exploredstamps= set()
	exploredstamps.add(state.key)
	UDLR=["Up","Down","Left","Right"]
	max_fringe_size=0
	max_depth=0
	max_mem=0
	while not(frontier==[]): 
		max_fringe_size=max(max_fringe_size,len(frontier))
		state = frontier.pop(0)
		
		if (state.goal_check()): return [[UDLR[i] for i in state.get_path()],
		len(state.get_path()), len(exploredstamps)-len(frontier)-1,
		 len(frontier), max_fringe_size, 
		state.depth, max_depth,time.time(),max_mem]

		successor = neighbors(state.state)
		for index,item in enumerate(successor):
			if item!=None:
				child=Node(item)
			
			if not(child.key in exploredstamps):
				child.set_depth(state.depth+1)
				child.set_parent(state)
				child.get_dir(index)
				frontier.append(child)
#                    explored.add(child
				exploredstamps.add(child.key)
				max_depth=max(max_depth,child.depth)
	return False

def DFS(initialState):
	frontier = []
	state=Node(initialState)
	state.set_depth(0)
	state.set_parent(None)
	frontier.append(state)
	#    explored = set()
	exploredstamps= set()
	exploredstamps.add(state.key)
	UDLR=list(reversed(["Right","Left","Down","Up"]))
	max_fringe_size=0
	max_depth=0
	max_mem=0

	while not(frontier==[]): 
		max_fringe_size=max(max_fringe_size,len(frontier))
		state = frontier.pop()
		if (state.goal_check()): 
			return [[UDLR[i] for i in state.get_path()],len(state.get_path()), 
					len(exploredstamps)-len(frontier)-1, len(frontier), max_fringe_size, 
					state.depth, max_depth,time.time(),max_mem]
		successor = list(reversed(neighbors(state.state)))

		for index,item in enumerate(successor):
			if item!=None:
				child=Node(item)

				if not(child.key in exploredstamps):
					child.set_depth(state.depth+1)
					child.set_parent(state)
					child.get_dir(index)
					frontier.append(child)
					#explored.add(child)
					exploredstamps.add(child.key)
					max_depth=max(max_depth,child.depth)

	return False

def heur(state,i=0):
	goal = [0,1,2,3,4,5,6,7,8]
	for value in state:
		if goal[i] != value:
			i += 1

	return i


def AST(state):
	closedset = []
	frontier = PriorityQueue()
	start  = Node(state)
	frontier.put((heur(state), start))
	exploredstamps = set()
	exploredstamps.add(start.key)

	while not(frontier==[]): 
		priority,node = frontier.get()
		if node.goal_check():
			return node.state

		closedset.append(node)

		successor = neighbors(node.state)
		for index,value in enumerate(successor):
			if value != None:
				child = Node(node.state)

				if not(child.key in exploredstamps):

					child.set_depth(state.depth+1)
					child.set_parent(state)
					child.get_dir(index)

					score = child.depth + heur(child.state)
					value_obj = Node(value,score)
					frontier.put((score,value_obj))


	return False

#
#if __name__ == '__main__':
print(DFS([6,1,8,4,0,2,7,3,5]))
# 	file = open('output.txt', 'w')
# 	file.write('cost_of_path: %s\n' % len(state.path_to_goal))
# 	file.write('max_search_depth: %s\n' % max_depth)
# 	file.write('running_time: %s\n' % time.time())


'''x = PriorityQueue()
	
	for value in successors::
		priori = heur(value)
		x.put((priori,Node(value,priori)))'''