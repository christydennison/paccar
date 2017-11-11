import numpy as np
from hmmlearn import hmm
np.random.seed(42)


X1 = [[0.0,23.0,101.5, 0], [0.0,22.0,101.5, 0], [0.0,23,101.7, 0]]
X2 = [[0.0,24.68,102.0, 0], [0.0,24.5,103.5, 0.2], [0.0,25.5,103.2, 0.5], [0.0,26.5,103.2, 1]]
X = np.concatenate([X1, X2])
lengths = [len(X1), len(X2)]

num_states = 3
# HMM model with Gaussian emissions
model = hmm.GaussianHMM(n_components=num_states, covariance_type="full", n_iter=1000)
model.fit(X, lengths)


print(model.transmat_)


print(model.predict(X,lengths))

