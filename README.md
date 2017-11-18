# paccar

[HMMLearn Tutorial](http://hmmlearn.readthedocs.io/en/stable/tutorial.html)

[Hidden Markov Models Wiki](https://en.wikipedia.org/wiki/Hidden_Markov_model)

[CS 229 Notes on HMM](http://cs229.stanford.edu/section/cs229-hmm.pdf)


Repair slices map format:

    {
        veh_id0: {
            repair_type0: [
                {
                    0: [snapshot0, snapshot1, ...],
                    1: [snapshot4, snapshot5, ...],
                    2: [snapshot6, snapshot7, ...]
                },
                {
                    0: [snapshot10, snapshot11, ...],
                    1: [snapshot14, snapshot15, ...],
                    2: [snapshot16, snapshot17, ...]
                }
            ],
            repair_type1: [
                {
                    0: [snapshot2, snapshot3, ...],
                    1: [snapshot4, snapshot5, ...],
                    2: [snapshot6, snapshot7, ...]
                },
                {
                    0: [snapshot10, snapshot11, ...],
                    1: [snapshot14, snapshot15, ...],
                    2: [snapshot16, snapshot17, ...]
                }
            ]
        },

        veh_id1: {
            repair_type0: [
                {
                    0: [snapshot0, snapshot1, ...],
                    1: [snapshot4, snapshot5, ...],
                    2: [snapshot6, snapshot7, ...]
                },
                {
                    0: [snapshot10, snapshot11, ...],
                    1: [snapshot14, snapshot15, ...],
                    2: [snapshot16, snapshot17, ...]
                }
            ],
            repair_type1: [
                {
                    0: [snapshot2, snapshot3, ...],
                    1: [snapshot4, snapshot5, ...],
                    2: [snapshot6, snapshot7, ...]
                },
                {
                    0: [snapshot10, snapshot11, ...],
                    1: [snapshot14, snapshot15, ...],
                    2: [snapshot16, snapshot17, ...]
                }
            ]
        }
    }