from __future__ import division
import numpy as np
from hmmlearn import hmm

states = ["Rainy", "Sunny"]
n_states = len(states)

observations = ["walk", "shop", "clean"]
n_observations = len(observations)

start_probability = np.array([0.6, 0.4])

transition_probability = np.array([
  [0.7, 0.3],
  [0.4, 0.6]
])

emission_probability = np.array([
  [0.1, 0.4, 0.5],
  [0.6, 0.3, 0.1]
])

model = hmm.MultinomialHMM(n_components=n_states)
model.startprob_=start_probability
model.transmat_=transition_probability
model.emissionprob_=emission_probability

# predict a sequence of hidden states based on visible states
bob_says = [0, 2, 1, 1, 2, 0]
model = model.fit(bob_says)
logprob, alice_hears = model.decode(bob_says, algorithm="viterbi")
print "Bob says:", ", ".join(map(lambda x: observations[x], bob_says))
print "Alice hears:", ", ".join(map(lambda x: states[x], alice_hears))







from __future__ import division
import numpy as np
from hmmlearn import hmm

states = ["Healthy", "Critical", "Broken"]
n_states = len(states)

observations = ["cold", "hot"]
n_observations = len(observations)

start_probability = np.array([0.6, 0.4])

transition_probability = np.array([
  [0.6, 0.3, 0,1],
  [0.3, 0.4, 0.3]
  [0, 0, 1]
])

emission_probability = np.array([
  [0.8, 0.2],
  [0.5, 0.5]
  [0.1, 0.9]
])

model = hmm.MultinomialHMM(n_components=n_states)
model.startprob_=start_probability
model.transmat_=transition_probability
model.emissionprob_=emission_probability

# predict a sequence of hidden states based on visible states
conditions = [0, 1, 1, 1, 1, 1]
model = model.fit(conditions)
logprob, results = model.decode(conditions, algorithm="viterbi")
print "Bob says:", ", ".join(map(lambda x: observations[x], conditions))
print "Alice hears:", ", ".join(map(lambda x: states[x], results))
