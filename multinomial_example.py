from __future__ import division
import numpy as np
from hmmlearn import hmm

states = ["Healthy", "Critical", "Broken"]
n_states = len(states)

observations = ["cold", "hot"]
n_observations = len(observations)

start_probability = np.array([0.6, 0.3, 0.1])

transition_probability = np.array([
  [0.6, 0.3, 0,1],
  [0.3, 0.4, 0.3],
  [0, 0, 1]
])

emission_probability = np.array([
  [0.8, 0.2],
  [0.5, 0.5],
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
print "conditions:", ", ".join(map(lambda x: observations[x], conditions))
print "results:", ", ".join(map(lambda x: states[x], results))
