'''
Version 0.05

from MfP3 import putzer

from MfP3 import picard

from sympy.abc import x,y

from sympy import *

# Putzer

M = Matrix([[1,-1], [1,3]])

putzer(M)


# Picard

f = y**2

x0 = 0

y0 = 1

n = 3

picard(f,x0,y0,n)

'''

# Imports

from sympy.matrices import Matrix, eye, zeros, ones, diag

from sympy import pprint

from sympy import init_printing

from sympy import *

import sympy as sympy

from sympy.abc import x,y

# import console

from sympy import symbols

import math 

def putzer(M):
	# Init

	# console.clear()
	
	print("\n\n ==== Putzer ==== \n\n")

	init_printing()
	
	# Define matrix

	print("\n=== Voraussetzungen ===\n")

	print("Die gegebene Matrix ist\n")

	A = symbols('A')

	pprint(Eq(S(A), M, evaluate = False))

	print("\nDaher ist das charakteristische Polynom von A\n")

	pprint(M.charpoly().as_expr())

	print("\nMit den Nullstellen (Eigenwerte der Matrix)\n")

	eigen = M.eigenvals()

	nullstellen = [p for p in eigen.keys() for i in range(0,eigen[p])]

	print(nullstellen)

	print("\n=== Beginn des Putzer-Algorithmus ===\n")

	print("\nEs gilt für die Matrizen\n")

	E = eye(int(math.sqrt(len(M))))

	mats = [E]

	pprint(Eq(S('P_0'),E, evaluate = False))
	
	print("\n\nPᵢ := (A - λᵢ)Pᵢ₋₁, (i ∈ {1,...,n})")

	for i in range(0, len(nullstellen)):
		cm = (M - nullstellen[i]*E)*mats[i]
		print("\n\n")
		pprint(Eq(S('P_' + str(i + 1)),cm, evaluate = False))
		mats.append(cm)
	
	
	print("\nEs gilt für die Differentialgleichungen\n")
	
	print("w₁' = λ₁w₁, w₁(0) = 1\n")
	
	print("wᵢ' = λᵢwᵢ + wᵢ₋₁, wᵢ(0) = 0, (i ∈ {2,...,n})\n\n")
	
	x = sympy.symbols('x')
	w1 = sympy.Function('w_1')
	ode = sympy.Eq(sympy.Derivative(w1(x),x),w1(x)*nullstellen[0])
	
	pprint(ode)
	
	sol = sympy.dsolve(ode,w1(x),ics={w1(0):1})
	rsol = sol.rhs


	pprint(sol)

	funcs = [rsol]

	for i in range(1, len(nullstellen)):
		cf = sympy.Function('w_' + str(i + 1))
		print("\n")
		ode = sympy.Eq(sympy.Derivative(cf(x),x),cf(x)*nullstellen[i] + funcs[i - 1])
		pprint(ode)
		sol = sympy.dsolve(ode,cf(x),ics={cf(0):0})
		pprint(sol)
		rsol = sol.rhs
		funcs.append(rsol)
	
	print("\n\n")

	print("=== Berechnen des Gesamtergebnisses ===")
	
	print("\n exp(xA) = ∑ wᵢ(x) Pᵢ₋₁")
	
	erg = funcs[0]*mats[0]

	for i in range(1,len(nullstellen)):
		erg = erg + funcs[i]*mats[i]
	
	erg = simplify(erg)

	print("\n\n")

	res = Eq(S('exp(xA)'), erg, evaluate = False)

	pprint(res)
	
# Picard

def picard(f,x0,y0,n):
	
	print("\n\n ==== Picard ==== \n\n")
	
	init_printing()

	print("=== Gegeben ist ===\n")

	pprint(Eq(S("dy/dx"), f, evaluate = False))
	
	print("\n also ein AWP der Form y' = f(x,y), y(x₀) = y₀")

	print("\n\n")

	s = y0 + integrate(f.subs(y,0),(x,x0,x))

	print("=== Damit folgen die Picard-Iterierten ===\n")
	
	pprint(Eq(S("P"),y0 + Integral(f.subs(y,0),(x,x0,x))))

	pprint(Eq(S("P"),s,evaluate = False))

	picards = [s]

	for i in range(0,n):
		print("\n\n")
		pc = y0 + integrate(f.subs(y,picards[i]),(x,x0,x))
		
		pprint(Eq(S("P^" + str(i + 2)),y0 + Integral(f.subs(y,picards[i]),(x,x0,x)),evaluate = False))
		
		picards.append(pc)
		pprint(Eq(S("P^" + str(i + 2)),pc,evaluate = False))

