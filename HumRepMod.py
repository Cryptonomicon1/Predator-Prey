'''
https://scipy-cookbook.readthedocs.io/items/LoktaVolterraTutorial.htm

du/dt = au - u^2/k - buv/k
dv/dt = -cv + dbu*v

u: number of prey
v: number of predators

a: prey growth
b: prey death rate due to predators
k: prey carrying capacity
c: predator death
d: number of prey required to create new predator

zero starting conditions = [0, 0] and [c/(d*b), a/b]
'''

# -------------------------------------------------------------

import numpy as np
import pylab as p
from scipy import integrate
from math import sqrt

# -------------------------------------------------------------

stone_k = 6.1774153694
bronze_k = 12.4747221167
iron_k = 18.4537278947
org_k = 22.0351886675
medieval_k = 45*.64
k = bronze_k			# Prey Carrying Capacity

per_k = 0.6

slow_a = 0.0010178269	# Prey Birth Rate (Slow)
fast_a = 0.0021199625	# Prey Birth Rate (Fast)
a = fast_a				# Prey Birth Rate
b = 0.005				# Prey Death rate due to Predators
d = 0.3					# Number of Prey to Make new Predator
c = per_k*k*d*b			# Predator Death Rate

# -------------------------------------------------------------

# timeline = [t, k, a, per_k]
timeline = [
[0, bronze_k, fast_a, 0.8],
[2100, iron_k, fast_a, 0.8],
#[2500, iron_k, fast_a, 0.6],
[3270, org_k, slow_a, 0.6],
[3800, medieval_k, fast_a, 0.6],
[6500, medieval_k, fast_a, 0.8],
#[4000, medieval_k, fast_a, 0.4],
#[6000, medieval_k, fast_a, 0.8],
[12000, medieval_k, -slow_a, 0.8]
]
# -------------------------------------------------------------

def dX_dt(X, t, k, a, c):
	return np.array([a*X[0]-(a*X[0]*X[0]/k)-(b*X[0]*X[1]/k), -c*X[1]+d*b*X[0]*X[1]])

def Model(XO, t, k, a, c):
	pop_over_span, infodict = integrate.odeint(dX_dt, XO, t, args=(k, a, c), full_output=True)
	infodict['message']
	return pop_over_span

X = np.array([[0,0]])

for i in range(len(timeline[:-1])):
	t_i = timeline[i][0]
	t_f = timeline[i+1][0]
	t_d = t_f - t_i
	t = np.linspace(0, t_d, t_d)

	k = timeline[i][1]
	a = timeline[i][2]
	c = timeline[i][3]*k*d*b

	if i==0:
		XO = np.array([1*c/(d*b), 0.1*( ( k*a-( a*c/(d*b) ) )/b )])
	else:
		XO = np.array([X[-1][0], X[-1][1]])
	temp = Model(XO, t, k, a, c)

	X = np.concatenate([X, temp])

	if i==0:
		X = X[1:]

t = np.linspace(0, len(X), len(X))

humans, reptilians = X.T
f1 = p.figure()
p.plot(t, humans, 'r-', label='Humans')
p.plot(t, reptilians, 'b-', label='Reptilians')
p.grid()
p.legend(loc='best')
p.xlabel('Time (years)')
p.ylabel('Population ( creature/(km^2) )')
p.title('Population of Reptilians and Humans Over Time')
f1.savefig('humans_and_reptilians_1.png')
