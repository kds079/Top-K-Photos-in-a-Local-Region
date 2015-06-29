import numpy as np
from scipy.sparse import csc_matrix

def pageRank(G, s = .85, maxerr = .001, sIter = 30, rwVector = None):
    """
    Computes the pagerank for each of the n states.

    Used in webpage ranking and text summarization using unweighted
    or weighted transitions respectively.


    Args
    ----------
    G: matrix representing state transitions
       Gij can be a boolean or non negative real number representing the
       transition weight from state i to j.

    Kwargs
    ----------
    s: probability of following a transition. 1-s probability of teleporting
       to another state. Defaults to 0.85

    maxerr: if the sum of pageranks between iterations is bellow this we will
            have converged. Defaults to 0.001
    """
    n = G.shape[0]
    # from sklearn.preprocessing import normalize

    # transform G into markov matrix M
    M = csc_matrix(G,dtype=np.float)
    x = np.array(M.sum(1))
    rsums = np.array(M.sum(1))[:,0]
    ri, ci = M.nonzero()
    # M.data /= rsums[ri]

    # bool array of sink states
    sink = rsums==0

    # Compute pagerank r until we converge
    ro, r = np.zeros(n),  np.ones(n) / float(n)  #np.ones(n)
    nIter = 0
    Ti = []
    while (np.sum(np.abs(r-ro)) > maxerr) and (nIter < sIter):
        ro = r.copy()
        # calculate each pagerank at a time
        for i in xrange(0,n):
            # inlinks of state i
            # tmp = M[:,i].todense()
            tmp = M[i,:].todense()
            # Ii = np.array(tmp)[:,0]
            Ii = np.array(tmp)
            # account for sink states
            Si = sink / float(n)
            # account for teleportation to state i
            if rwVector is None:
                Ti = np.ones(n) / float(n)
            else:
                Ti = np.array(rwVector)

            tmp2 = Ii*s + Si*s + Ti*(1-s)
            sum1 = sum(tmp2)
            # r[i] = ro.dot( Ii*s + Si*s + Ti*(1-s) )
            r[i] = (Ii*s).dot(ro) + Ti[i]*(1-s)
        nIter += 1
    print('pagerank iteration : ' + str(nIter))
    # print(sum(Ti))

    print(np.sum(r/sum(r)))
    # return normalized pagerank
    return r/sum(r)




if __name__=='__main__':
    # Example extracted from 'Introduction to Information Retrieval'

    G = np.array([[0,0,4,0,0,0,0],
                  [0,1,1,0,0,0,0],
                  [3,0,5,1,0,0,0],
                  [0,0,0,1,1,0,0],
                  [0,0,0,0,0,0,1],
                  [0,0,0,0,0,1,1],
                  [0,0,0,1,4,0,1]])

    # G = np.array([[0,0,4,0,0,0,0],
    #               [0,1,1,0,0,0,0],
    #               [3,0,5,1,0,0,0],
    #               [0,0,0,1,1,0,0],
    #               [0,0,0,0,0,0,1],
    #               [0,0,0,0,0,1,1],
    #               [0,0,0,1,4,0,1]])
    # G = np.array([[0,1,1,1,1],
    #               [1,0,1,3,1],
    #               [1,2,0,5,6],
    #               [2,1,1,1,1],
    #               [2,1,2,1,2]])
    # G = np.array([[0  ,1/3,1/3,1/3],
    #               [1/3,0  ,1/3,1/3],
    #               [1/3,1/3,0  ,1/3],
    #               [1/3,1/3,1/3,0]])

    print pageRank(G,s=.83)
