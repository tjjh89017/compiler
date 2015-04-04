#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from functools import reduce

class DFA:

	def __init__(self, transition_table, init_state, final_state, symbol):

		self.delta = transition_table
		self.q0 = init_state
		self.F = final_state
		self.symbol = symbol

	def delta_hat(self, state, input_string):

		for a in input_string:
			state = self.delta[state][a]
		return state

	def valid(self, input_string):

		return self.delta_hat(self.q0, input_string) in self.F

class NFA:

	def __init__(self, transition_table, init_state, final_state, symbol, empty_symbol):

		self.delta = transition_table
		self.q0 = init_state
		self.F = final_state
		self.symbol = symbol
		self.empty_symbol = empty_symbol

	def delta_hat(self, state, input_string):

		states = self.lambda_state(set([state]))
		#print(states)
		for a in input_string:
			new_states = set([])
			for state in states:
				try:
					new_states = new_states | self.delta[state][a]
				except KeyError:
					pass
			states = new_states
		#print(states)
		return self.lambda_state(states)

	def lambda_state(self, states):

		if not states:
			return states

		change = True
		while change:
			for state in states.copy():
				if states >= self.delta[state][self.empty_symbol]:
					change = False
					break
				states = states | self.delta[state][self.empty_symbol]

		return states

	def alphabet(self):

		return [x for x in self.symbol if x != self.empty_symbol]

def convert_NFA_to_DFA(N):

	q0 = frozenset([x for x in N.lambda_state(set([N.q0]))])
	queue = set([q0])
	unproc_queue = queue.copy()
	delta = {}
	F = []
	symbol = N.alphabet()

	while len(unproc_queue) > 0:
		q_set = unproc_queue.pop()
		if not q_set:
			continue
		delta[q_set] = {}
		for a in symbol:
			new_states = reduce(lambda x, y: x | y, [N.delta_hat(q, a) for q in q_set])
			new_states = frozenset(new_states)
			delta[q_set][a] = new_states
			# new state, put into queue
			if not new_states in queue:
				queue.add(new_states)
				unproc_queue.add(new_states)

	for q_set in queue:
		if len(q_set & N.F) > 0:
			F.append(q_set)

	return DFA(delta, q0, F, symbol)
	pass

def __repr(frozen):

	return ",".join(sorted(x for x in frozen))

def main():

	f = open(sys.argv[1], "r")
	# remove the last empty string
	s = f.read().split("\n")[:-1]
	f.close()
	# remove the last parameter
	alphabet = ["LAMBDA"] + s[0].split(",")[1:-1]
	transition_table = {}

	for i, states in enumerate(s[1:], 1):
		transition_table[str(i)] = {}
		for j, state in enumerate(states.split(" "), 0):
			transition_table[str(i)][alphabet[j]] = set(x for x in state.split(",") if x not in ['0', '*'])

	N = NFA(transition_table, '1', set([str(len(s[1:]))]), alphabet, "LAMBDA")	
	D = convert_NFA_to_DFA(N)

	# output
	f = open(sys.argv[2], "w")
	f.write(",".join(D.symbol) + "\n")
	queue = set([D.q0])
	while len(queue) > 0:
		state = queue.pop()
		if not state:
			continue
		if state in D.F:
			f.write("*")
		f.write(__repr(state) + " ")
		for a in D.symbol:
			result = D.delta_hat(state, a)
			queue.add(result)
			if not result:
				f.write("0 ")
			else:
				if result in D.F:
					f.write("*")
				f.write(__repr(result) + " ")

		f.write("\n")
	f.close()

if __name__ == '__main__':
	main()