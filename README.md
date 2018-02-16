#Modified Lotka-Volterra (Predator-Prey) Model

Most of my writing is in my code comments.
I will write that I used the Scipy ODE
Solver to solve a system of differential
equations. The equations exibit the 
Lotka-Volterra model with a modification
to include a carrying capacity for the
prey.

I wanted to model a population of humans
and lizard folk who eat humans. I did not
attempt to make the code nice. I was
moreso after the data.

I used real carrying capacities for each
age's technology levels. I used a real
birth rate from france between the year
1000 CE and 1300 CE. I used this rate
because this was a boom time when they
deforested, rediscovered technology,
and re-colonized land. This is the
fastest growth in medieval history. It
is also considered the "little warm
period." I used the prior time of
France's for a slower growth rate.
The slow growth rate was the time of
the Viking invasions, and plague.

The lizard folk's birth rate was set
to unusually fast.
My first attempt to account for the
number of calories a lizard person would
eat in humans from birth to adulthood
caused extremely slow lizard population
growth because humans are not very
nutritious! The model looks more exciting
with a faster growth rate. The lizard
death rate is set to drag down the human
population to 80% of their carrying
capacity.

The result was whenever the human tech
advanced and their carrying capacity
rose, the human population would
skyrocket towards their carrying
capacity. Then, when they hit 80% of
their capacity, the lizard growth would
go from negative to positive, and the
lizard population would soar, causing
negative growth in the human population.
The two populations go on a damped
oscillation until they level out. Then,
the next disturbance causes the next
damped oscillation.
