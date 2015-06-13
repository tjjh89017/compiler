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
	"""
	Interesting it is. by Yoda
	"""
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
		#print()
		#print("lr1items")
		#print(lr1items)
		#print(lr1items[current_pos:current_size])
		#print()
		#for item in lr1items[current_pos:current_size]:
		for item in lr1items:
			#print(item)
			if item[1][-1] == "*":
				continue
			next_construction = item[1][item[1].find("*") + 1]
			if is_terminal(next_construction):
				continue
			##########
			temp = item[1].find("*")
			if temp + 2 == len(item[1]):
				helper_production = "l"
				#continue
			elif temp + 2 > len(item[1]):
				continue
			else:
				helper_production = item[1][temp + 2]
			##########
			first_result = None
			if helper_production not in F.keys():
				#first_result = set([helper_production])
				#print(helper_production)
				#print("if helper_production not in F.keys():")
				if is_terminal(helper_production):
					first_result = set([helper_production])
				else:
					first_result = item[2].copy()
			else:
				first_result = F[helper_production]
			for product in prod_list:
				if product[0] != next_construction:
					continue
				for term in first_result:
					items.add((product[0], "*" + product[1], frozenset(set([term]))))

		#current_pos = new_pos
		#print(current_size)
		#print(len(items))
		#print()

	return items


def main():
	"""
	TODO
	this is a fucking unmaintainable code
	inside this code, you will see some fucking voodoo.
	do not trace it
	thank you :)
	sometimes comment is important. (:
	As you can see, the comment lines are much more than the code.
	angel I love you
	I love ADL
	I will be a good PHD student in ADL CSIE
	Thou shall not play with my code. by Tade God
	IoT sentoku rocks
	"""
	if len(sys.argv) < 3:
		print("error: too few argument")
		sys.exit(1)

	grammer = None
	test_case = None
	with open(sys.argv[1], "r") as f:
		grammer = f.read().split('\n')

	test_case = grammer[int(grammer[0]) + 2:-1]
	grammer = grammer[1:int(grammer[0]) + 1]

	#print(grammer)
	#print()
	#print(test_case)
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
		T.append((ts[0][0], ts[0][3:], frozenset(set([x for x in ts[1][1:-1] if x != ',']))))

	#print()
	#print("T")
	#print(T)
	#print()
	#print("G")
	#print(G)

	#print()
	F = FIRST(G)
	#print("FIRST")
	#print(F)

	# calc closure1
	prod_list = []
	for key in G.keys():
		for g in G[key]:
			prod_list.append((key, g))
	#print()
	#print("prod_list")
	#print(prod_list)

	with open(sys.argv[2], "w") as f:

		for t in T:
			items = closure1(prod_list, set([t]), F)
			#print(items)
			out = {}
			for item in items:
				s = item[0] + "->" + item[1]
				if s not in out:
					out[s] = set()
				out[s] = out[s] | item[2]
	
			#print(out)
			for index, element in out.items():
				f.write(index + " {" + ",".join(list(element)) + "}\n")
				#print("t")
			f.write("#\n")
			#print(t)
			#print("#")

	# Thou shall not pass by 肝道夫
	pass

if __name__ == "__main__":
	main()
