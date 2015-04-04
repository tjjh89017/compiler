#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

class NFA:

	def __init__(self, transition_table, init_state, final_state, symbol, empty_symbol):
		self.delta = transition_table
		self.q0 = init_state
		self.F = final_state
		self.symbol = symbol
		self.empty_symbol = empty_symbol

	def delta_hat(self, state, input_string):

		states = self.lambda_state(set([state]))
		print(states)
		for a in input_string:
			new_states = set([])
			for state in states:
				try:
					new_states = new_states | self.delta[state][a]
				except KeyError:
					pass
			states = new_states
		print(states)
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

	pass

def main():

	f = open(sys.argv[1], "r")
	# remove the last empty string
	s = f.read().split("\n")[:-1]
	# remove the last parameter
	alphabet = ["LAMBDA"] + s[0].split(",")[1:-1]
	transition_table = {}

	for i, states in enumerate(s[1:], 1):
		transition_table[str(i)] = {}
		for j, state in enumerate(states.split(" "), 0):
			transition_table[str(i)][alphabet[j]] = set(x for x in state.split(",") if x not in ['0', '*'])

	N = NFA(transition_table, 1, len(s[1:]), alphabet, "LAMBDA")
	N.delta_hat('1', 'a')
	#print(N.delta_hat('1', 'b'))
	print(N.delta_hat('1', 'a'))
	#N.delta_hat('1', 'a')

	print()
	print(N.delta)

	pass

if __name__ == '__main__':
	main()