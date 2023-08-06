from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import range
import numpy as np
import matplotlib.pyplot as plt
from scipy import sparse, linalg
from AdaptivePELE.freeEnergies import utils
from AdaptivePELE.freeEnergies.utilitiesFreeEnergies import getStationaryDistr, getSortedEigen


def buildLinearChainCountMatrix():
    C = np.array([[6000., 3, 0, 0, 0, 0],
                  [3, 1000., 3, 0, 0, 0],
                  [0, 3, 1000., 3, 0, 0],
                  [0, 0, 3, 1000., 3, 0],
                  [0, 0, 0, 3, 1000., 3],
                  [0, 0, 0, 0, 3, 90000.]])
    return C+1/6.


def buildPCountMatrix():
    C = np.array([[600., 2, 2, 0, 0, 0],
                  [2, 100., 0, 2, 2, 0],
                  [2, 0, 100., 2, 2, 0],
                  [0, 2, 2, 100., 0, 2],
                  [0, 2, 2, 0, 100., 2],
                  [0, 0, 0, 2, 2, 9000.]])
    return C+1/6.


def normaliseMatrixVectors(M):
    normArray = []
    for x in M:
        normArray.append(x / np.linalg.norm(x))
    return np.array(normArray)


def normaliseMatrixRows(M):
    sums = M.sum(axis=1)
    T = M / sums[:, np.newaxis]
    return T


def buildTransitionMatrix(C):
    return normaliseMatrixRows(C)


def buildRevTransitionMatrix_fast(C, iterations=5):
    """
        #Implemented as Prinz paper
    """
    X = C + C.T
    x = X.sum(axis=1)
    c = C.sum(axis=1)

    return loop(iterations, X, x, C, c)


def loop(iterations, X, x, C, c):

    n = len(x)

    c_vec = c[:, np.newaxis]
    A = c_vec - C + c_vec.T - C.T

    for _ in range(iterations):
        for i in range(n):
            X[i, i] = C[i, i] * (x[i] - X[i, i]) / (c[i] - C[i, i])

        x = X.sum(axis=1)

        x_vec = x[:, np.newaxis]

        B = c_vec*(x_vec.T - X) + c_vec.T*(x_vec - X) - (C + C.T) * (x_vec + x_vec.T - 2 * X)
        Z = -(C+C.T) * (x_vec - X) * (x_vec.T - X)

        indicesU = np.triu_indices(n, 1)
        X[indicesU] = (-B[indicesU] + np.sqrt(B[indicesU]**2 - 4 * A[indicesU]*Z[indicesU])) / (2 * A[indicesU])
        X.T[indicesU] = X[indicesU]

        x = X.sum(axis=1)

    T = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            T[i, j] = X[i, j] / x[i]
    return T
    # return X / x[:,np.newaxis]


def buildRevTransitionMatrix(C):
    """
        #Implemented as Prinz paper
    """
    X = C + C.T
    x = X.sum(axis=1)
    c = C.sum(axis=1)

    iterations = 1000
    n = len(x)

    T = np.zeros(C.shape)
    for _ in range(iterations):
        # if it != 0 and it % 10 == 0:
        #    print(it)
        for i in range(n):
            X[i, i] = C[i, i] * (x[i] - X[i, i]) / (c[i] - C[i, i])
        x = X.sum(axis=1)
        for i in range(n - 1):
            for j in range(i + 1, n):
                a = c[i] - C[i, j] + c[j] - C[j, i]
                b = c[i] * (x[j]-X[i, j]) + c[j] * (x[i] - X[i, j])-(C[i, j] + C[j, i])*(x[i] + x[j] - 2*X[i, j])
                z = -(C[i, j] + C[j, i])*(x[i] - X[i, j])*(x[j] - X[i, j])
                X[i, j] = X[j, i] = (-b + np.sqrt(b**2 - 4*a*z))/(2*a)
        x = X.sum(axis=1)

    for i in range(n):
        for j in range(n):
            T[i, j] = X[i, j] / x[i]
    return T


def runSimulation(P, steps, startingPosition, states):
    position = startingPosition
    traj = np.zeros(steps)
    traj[0] = position
    for step in range(1, steps):
        position = np.random.choice(states, p=P[position])
        traj[step] = position
    return traj


def runSetOfSimulations(numberOfSimulations, P, steps, initial_states, verbose=True):
    trajs = []
    states = np.array(range(P.shape[0]))
    cumul = P.cumsum(axis=1)
    assert len(initial_states) == numberOfSimulations
    for sim, startingPosition in zip(range(numberOfSimulations), initial_states):
        if verbose and sim % 100 == 0:
            print("Simulation", sim)
        traj = utils.runSimulation(cumul, steps, startingPosition, states)
        trajs.append(traj)
    return np.array(trajs)

# def estimateCountMatrix(trajectories, n, tau):
#     counts = np.zeros((n, n))
#
#     #for traj in trajectories:
#     for i, traj in enumerate(trajectories):
#         print(i)
#         for i in range(len(traj) - tau):
#             fromState = traj[i]
#             toState = traj[i + tau]
#
#             counts[fromState][toState] += 1
#     return counts


def estimateCountMatrix(trajectories, n, tau):
    rows = []
    cols = []
    for traj in trajectories:
        if traj.size > tau:
            rows.append(traj[0:-tau])
            cols.append(traj[tau:])

    if len(rows) == 0:
        raise ValueError('Too long lagtime')

    row = np.concatenate(rows)
    col = np.concatenate(cols)
    data = np.ones(row.size)
    C = sparse.coo_matrix((data, (row, col)), shape=(n, n))
    return C.toarray()


def printMatrix(matrix):
    for array in matrix:
        for element in array:
            print("%e" % element)
        print("")


def estimateTransitionMatrix(trajectories, n, tau, symm=True):
    C = estimateCountMatrix(trajectories, n, tau) + 1./n
    if symm:
        return utils.buildRevTransitionMatrix(C)
    return buildTransitionMatrix(C)


def getSortedEigenFromDtrajs(tau, trajs, n, symm=True):
    estimatedT = estimateTransitionMatrix(trajs, n, tau, symm=symm)
    # T.T*pi = pi; or pi*T = pi, where pi is col and row array respectively
    return getSortedEigen(estimatedT)


def getStationaryDistrFromTransition(transitionMatrix):
    _, eic = getSortedEigen(transitionMatrix)
    return getStationaryDistr(eic[:, 0])


def getRelativeEntropy(goldenStationary, goldenT, T):
    return np.dot(goldenStationary, goldenT*np.log(goldenT/T)).sum()


def getRelativeEntropyVectors(goldenStationary, distP):
    return np.dot(goldenStationary, np.log(goldenStationary/distP))


def getGoldenTForGivenTau(T, tau):
    n = T.shape[0]
    accT = np.eye(n)
    for _ in range(tau):
        accT = np.dot(accT, T)
    return accT


def analyseEigenvalEvol(trajs, taus, n):
    allEigenvals = []
    probabilities = []
    for tau in taus:
        eigenvals, eigenvectors = getSortedEigenFromDtrajs(tau, trajs, n, symm=True)
        allEigenvals.append(eigenvals)
        probabilities.append(getStationaryDistr(eigenvectors[:, 0]))

    allEigenvals = np.array(allEigenvals).real  # rework
    probabilities = np.array(probabilities)
    return allEigenvals, probabilities


def plotEigenvalEvolutionInTau(allEigenvals, probabilities, taus, n, golden=None):

    fig = plt.figure(1)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_yscale('log')
    valuesToPlot = n
    for i in range(1, valuesToPlot):
        ax.plot(taus, allEigenvals[:, i])
    plt.legend(["State %d" % d for d in range(n)])
    plt.ylabel("Eigenvalues")
    plt.xlabel("Lagtime")
    plt.figure(2)
    for i in range(1, valuesToPlot):
        plt.plot(taus, -taus/np.log(allEigenvals[:, i]))
    plt.legend(["State %d" % d for d in range(n)])
    plt.ylabel("Implied timescales")
    plt.xlabel("Lagtime")
    plt.figure(3)
    for i in range(n):
        plt.plot(taus, probabilities[:, i], 'x', label="State %d" % i)
        if golden is not None:
            plt.axhline(golden[i], label="Golden state %d" % i)
    # if golden is not None:
    #     plt.hlines(golden, taus[0], taus[-1])
    plt.legend()
    plt.xlabel("Lagtime")
    plt.ylabel("Probability")


def main():
    numberOfStates = 6
    # steps = 50
    # numberOfSimulations = 60000
    # taus = np.array([1,10,20,50,100,200,500])
    # taus = np.array([1])

    n = numberOfStates

    C = buildLinearChainCountMatrix()
    T = buildTransitionMatrix(C)

    eigenvals, eigenvectors = linalg.eig(T, left=True, right=False)
    sortedIndices = np.argsort(eigenvals)[::-1]
    # stationary distribution
    goldenStationary = getStationaryDistr(eigenvectors[:, sortedIndices[0]])

    print("real C")
    print(printMatrix(C))
    print("real T")
    print(printMatrix(T))
    print("=====")

    # trajs = runSetOfSimulations(numberOfSimulations, T, steps)
    # np.save("trajs_S_50_60000.npy", trajs)
    # np.save("trajs_chain_small.npy", trajs)
    trajs = np.load("trajs_S_50_60000.npy")

    taus = np.array(range(1, 49))
    # taus = np.array([1, 10, 25,  50,  75,  100,  250,  500,  750,  1000,  2000,  2500])
    eigenvals_evol, probabilities_evol = analyseEigenvalEvol(trajs, taus, n)
    plotEigenvalEvolutionInTau(eigenvals_evol, probabilities_evol, taus, n)

    simLengths = list(range(50, 2000, 50))
    simLengths = list(range(10, 50, 5))
    trajNumbers = list(range(0, 600, 5))
    trajNumbers = [600]

    entropies = np.zeros(len(simLengths))
    tau = 1
    for trajNum in trajNumbers:
        for i, j in enumerate(simLengths):
            trimmedTrajs = trajs[0:trajNum, :j]
            eigenvals, _ = getSortedEigenFromDtrajs(tau, trimmedTrajs, n)
            # stationary = getStationaryDistr(eigenvec[:,0])

            estimatedT = estimateTransitionMatrix(trimmedTrajs, n, tau)
            goldenT = getGoldenTForGivenTau(T, tau)

            rEntropy = getRelativeEntropy(goldenStationary, goldenT, estimatedT)
            print(j, rEntropy)
            entropies[i] = rEntropy

    fig = plt.figure(3)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_yscale('log')
    plt.plot(simLengths, entropies)
    plt.show()

if __name__ == "__main__":
    main()
