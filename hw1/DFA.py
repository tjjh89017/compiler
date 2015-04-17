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
			if a not in self.delta[state].keys():
				return ""
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
		for a in input_string:
			new_states = set([])
			for state in states:
				try:
					new_states = self.lambda_state(new_states | self.delta[state][a])
				except KeyError:
					pass
			states = new_states

		return self.lambda_state(states)

	def lambda_state(self, states):

		if not states:
			return states

		proc_states = states.copy()
		change = True
		while len(proc_states):
			state = proc_states.pop()
			new_states = self.delta[state][self.empty_symbol]
			if not new_states in states:
				proc_states = proc_states | new_states
				states = states | new_states

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

def __repr(frozen, F):

	result = ",".join(sorted(x for x in frozen))
	if frozen in F:
		return "*" + result
	return result

def main():

	f = open(sys.argv[1], "r")
	# remove the last empty string
	s = f.read().split("\n")[:-1]
	f.close()
	# remove the last parameter
	transition_table = {}
	alpha = s[0].split(",")
	s = s[1:]
	F = []

	for state in s:
		q = state.split(" ")
		if not q[-1]:
			q = q[:-1]
		transition_table[q[0]] = {}
		for trans in zip(alpha, q[1:]):
			if trans[1] != "0":
				transition_table[q[0]][trans[0]] = trans[1]
			if "*" in trans[1]:
				F.append(trans[1])

	D = DFA(transition_table, s[0].split()[0], F, alpha)
	st = input()
	if D.valid(st):
		print("valid")
	else:
		print("error")

if __name__ == '__main__':
	main()
