# https://scipy-cookbook.readthedocs.io/items/LoktaVolterraTutorial.htm

# du/dt = au - u^2/k - buv/k
# dv/dt = -cv + dbu*v

# u: number of prey
# v: number of predators

# a: prey growth
# b: prey death rate due to predators
# k: prey carrying capacity
# c: predator death
# d: number of prey required to create new predator

# zero starting conditions = [0, 0] and [c/(d*b), a/b]

# -------------------------------------------------------------

import os
import numpy as np
import pylab as p
from scipy import integrate
from math import sqrt
from math import e
from math import log

# -------------------------------------------------------------

# Stone Age -10000 to -8700 or t = 0
# Note: the stone age started much earlier but we will do this for now.
# Copper Age -8700 to -3300
# Bronze Age -3300 to -1200
# Iron Age -1200 to -30
# Roman Age -30 to 500
# Medieval Age 500 to 1500

# k = k_i*e^(t*r)
# r = natural_log(k/k_i)/t

# k = carrying capacity
# k = initial carrying capacity
# t = year
# r = rate of carrying capacity increase

# Two Points
# k_i = 1/0.16188 (or 1person / 40acres)@ t = -3300
# k_f = 45*0.64 (45people / km^2 arable land)*(64% arable land max) @ t = 1300
# delta_t = 4600 years

k_i = 1/0.16188
k_f = 45*0.64
stone_t = -10000
copper_t = -8700
bronze_t = -3300
iron_t = -1200
org_t = -30
medieval_t = 500
delta_t = medieval_t - stone_t
r = log(k_f/k_i)/delta_t

stone_k = k_i*e**((stone_t-stone_t)*r)
copper_k = k_i*e**((copper_t-stone_t)*r)
bronze_k = k_i*e**((bronze_t-stone_t)*r)
iron_k = k_i*e**((iron_t-stone_t)*r)
org_k = k_i*e**((org_t-stone_t)*r)
medieval_k = k_i*e**((medieval_t-stone_t)*r)

os.system("tput reset")
print("Stone Ages:")
print("Starting Year:", stone_t - stone_t)
print("Ending Year:", copper_t - stone_t)
print("Capacity", stone_k, "people/(km^2)")
print(" ")

print("Copper Ages:")
print("Starting Year:", copper_t - stone_t)
print("Ending Year:", bronze_t - stone_t)
print("Capacity", copper_k, "people/(km^2)")
print(" ")

print("Bronze Age:")
print("Starting Year:", bronze_t - stone_t)
print("Ending Year:", iron_t - stone_t)
print("Capacity", bronze_k, "people/(km^2)")
print(" ")

print("Iron Ages:")
print("Starting Year:", iron_t - stone_t)
print("Ending Year:", org_t - stone_t)
print("Capacity", iron_k, "people/(km^2)")
print(" ")

print("Age of Organization:")
print("Starting Year:", org_t - stone_t)
print("Ending Year:", medieval_t - stone_t)
print("Capacity", org_k, "people/(km^2)")
print(" ")

print("Medieval Ages:")
print("Starting Year:", medieval_t - stone_t)
print("Ending Year: Magically Never")
print("Capacity", medieval_k, "people/(km^2)")
print(" ")

del e
del log
del k_i
del k_f
del delta_t
del r

k = bronze_k			# Prey Carrying Capacity

per_k = 0.6

slow_a = 0.0010178269	# Prey Birth Rate (Slow)
fast_a = 0.0021199625	# Prey Birth Rate (Fast)
a = fast_a				# Prey Birth Rate
b = 0.005				# Prey Death rate due to Predators
d = 0.2					# Number of Prey to Make new Predator
c = per_k*k*d*b			# Predator Death Rate

# -------------------------------------------------------------

# timeline = [t, k, a, per_k]
timeline = [
[stone_t-stone_t, stone_k, fast_a, 0.6],
[copper_t-stone_t, copper_k, fast_a, 0.8],
[bronze_t-stone_t, bronze_k, fast_a, 0.6],
[iron_t-stone_t, iron_k, fast_a, 0.6],
[org_t-stone_t, org_k, fast_a, 0.6],
[medieval_t-stone_t, medieval_k, fast_a, 0.8],
[1.5*(medieval_t-stone_t), medieval_k, fast_a, 0.8],
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

	print("Year:", t_i)
	print("Human Birth Rate:", a)
	print("Human Death Rate Due to Lizards:", b*XO[1]/k)
	print("Human Death Rate Due to Overpop:", XO[0]/k)
	print("Reptilian Birth Rate:", d*b*XO[0])
	print("Reptilian Death Rate:", c)
	print(" ")

	temp = Model(XO, t, k, a, c)

	X = np.concatenate([X, temp])

	if i==0:
		X = X[1:]

t = np.linspace(0, len(X), len(X))
line_width = 1.25

humans, reptilians = X.T
f1 = p.figure()
p.plot(t, humans, 'k-', label='Humans')
p.plot(t, reptilians, 'r-', label='Reptilians')

s = str(copper_t - stone_t)
p.axvline(copper_t - stone_t, color='#33adff', lw=line_width, label='copper age: '+s)
s = str(bronze_t - stone_t)
p.axvline(bronze_t - stone_t, color='#0099ff', lw=line_width, label='bronze age: '+s)
s = str(iron_t - stone_t)
p.axvline(iron_t - stone_t, color='#007acc', lw=line_width, label='iron age: '+s)
s = str(org_t - stone_t)
p.axvline(org_t - stone_t, color='#005c99', lw=line_width, label='org age: '+s)
s = str(medieval_t - stone_t)
p.axvline(medieval_t - stone_t, color='#003d66', lw=line_width, label='middle age: '+s)

p.grid()
p.legend(loc='best')
p.xlabel('Time (years)')
p.ylabel('Population ( creatures/(km^2) )')
p.title('Population of Reptilians and Humans Over Time')
#p.axis([8800, 16000, -0.5, 27])
#p.text(0.2, 10, 'cop=1300\nbrnz=6700\niron=8800\norg=9970\nmid=10500', bbox=dict(alpha=0.5))
f1.savefig('Humans_and_Reptilians_4.png')
p.show()
