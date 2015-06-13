#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

def is_nonterminal(s):

	return s.isupper()

def is_terminal(s):

	return not is_nonterminal(s) and not s == "l"

def __calc(F, prod_list):

	while __iter(F, prod_list):
		pass

def __iter(F, prod_list):

	change = False
	for p in prod_list:
		if __iter_prod(F, p):
			change = True
	return change
	pass

def __iter_prod(F, p):

	#F[p[0]]
	length = len(F[p[0]])
	if p[1] == "l":
		F[p[0]].add("l")
	else:
		for term in p[1]:
			if is_terminal(term):
				F[p[0]].add(term)
				break
			if term in F.keys():
				F[p[0]] = F[p[0]] | F[term]
				if "l" not in F[term]:
					break
				
	return length != len(F[p[0]])
	pass

def FIRST(G):

	first = {}
	for gs in G.keys():
		first[gs] = set()

	prod_list = []
	for key in G.keys():
		for g in G[key]:
			prod_list.append((key, g))

	# iter all procduction rule
	__calc(first, prod_list)
	return first
	pass

def closure1(prod_list, LR1set, F):

	items = LR1set.copy()
	current_pos = 0
	new_pos = 0
	current_size = -1
	while current_size != len(items):
		new_pos = len(items)
		current_size = len(items)

		lr1items = list(items)
		print()
		print("lr1items")
		print(lr1items)
		for item in lr1items[current_pos:current_size]:
			if item[1][-1] == "*":
				continue
			next_construction = item[1][item[1].find("*") + 1]
			if is_terminal(next_construction):
				continue
			##########
			temp = item[1].find("*")
			if temp + 2 >= len(item[1]):
				continue
			helper_production = item[1][temp + 2]
			##########
			first_result = None
			if helper_production not in F.keys():
				first_result = set([helper_production])
			else:
				first_result = F[helper_production]
			for product in prod_list:
				if product[0] != next_construction:
					continue
				for term in first_result:
					items.add((product[0], "*" + product[1], frozenset(set([term]))))

		current_pos = new_pos
		print()
		print(items)

	return items

def main():

	if len(sys.argv) < 3:
		print("error: too few argument")

	grammer = None
	test_case = None
	with open(sys.argv[1], "r") as f:
		grammer = f.read().split('\n')

	test_case = grammer[int(grammer[0]) + 2:-1]
	grammer = grammer[1:int(grammer[0]) + 1]

	print(grammer)
	print()
	print(test_case)

	# grammer parse
	G = {}
	for g in grammer:
		if g[0] not in G.keys():
			G[g[0]] = []
		G[g[0]].append(g[3:])

	# test case parse
	T = []
	for t in test_case:
		ts = t.split()
		T.append((ts[0][0],ts[0][3:], frozenset(set([x for x in ts[1][1:-1] if x != ',']))))

	print()
	print("T")
	print(T)
	print()
	print("G")
	print(G)

	print()
	F = FIRST(G)
	print("FIRST")
	print(F)
	'''
	for key in G.keys():
		print(key)
		print(first_set(G, key))
		print()
	'''
	# calc closure1
	prod_list = []
	for key in G.keys():
		for g in G[key]:
			prod_list.append((key, g))
	print()
	print("prod_list")
	print(prod_list)

	for t in T:
		closure1(prod_list, set([t]), F)
		print("t")
		print(t)
		print("#")

	pass

if __name__ == "__main__":
	main()
