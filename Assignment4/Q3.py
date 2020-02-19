import numpy as np
def TrinomialTree(isAmerican, isCall, S0, K, r,q,sigma, n):
    N=360
    dt = 1 / N  # time steps
    u = np.exp(sigma * np.sqrt(2 * dt)) # up
    d = np.exp(- sigma * np.sqrt(2 * dt)) # down
    m = 1.0 # do not move

    # risk netural probabilities
    a = np.exp((r-q) * dt / 2)
    b = np.exp(-  sigma * np.sqrt(dt / 2))
    c = np.exp(sigma * np.sqrt(dt / 2))
    pu = ((a - b) / (c - b)) ** 2
    pd = ((c - a) / (c - b)) ** 2
    pm = 1 - pu - pd

    Tree = [np.array([S0])]
    for i in range(n): # generate the trinomial tree and calculated payoff
        prevT = Tree[-1]
        md=np.array([prevT[-1]*m])
        dd=np.array([prevT[-1]*d])
        ST = np.concatenate((prevT*u,md,dd),axis=None)
        Tree.append(ST)
    if isCall:
        payoffs = np.maximum(0, (Tree[n] - K))
    else:
        payoffs = np.maximum(0, (K - Tree[n]))
    for i in reversed(range(n)):
        payoffs = (payoffs[:-2] * pu + payoffs[1:-1] * pm + payoffs[2:] * pd) * np.exp(-r* dt)
        if isAmerican:
            payoffs = np.maximum(payoffs, Tree[i] - K) # that is an extra term for american option
            print(payoffs==Tree[i]-K)
            # since we need to check if we should exercise early
    return payoffs[0]
# vega is the partial derivaives of option price with respect of vol
# here we add an increment in sigma to get vega
def Vega(isAmerican, isCall, S0, K, r,q, sigma, n):
    d = 0.001
    return (TrinomialTree(isAmerican, isCall, S0, K, r,q, sigma + d, n) -
            TrinomialTree(isAmerican, isCall, S0, K, r,q, sigma, n)) / d

def FindIMPvol(targetCall, isAmerican, isCall, S, K, r,q,n):
    max= 1000 # max step of iteration
    tor = 1.0e-8 # tolerance for the difference
    sigma = 0.2 # initial guessing sigma
    for i in range(0, max):
        TriNTprice = TrinomialTree(isAmerican, isCall, S, K,  r, q,sigma,n)
        vega = Vega(isAmerican, isCall, S, K,  r,q, sigma,n)
        difference = TriNTprice - targetCall
        if abs(difference) < tor: # if difference is small enough, we get desired sigma
            return sigma
        sigma = sigma - difference / vega # if not, by definition of vega then use newton method
        # we get an iterative formula for sigma
    return sigma
def main():
    # screen call price used to calculate sigma
    callprice=[11.38,10.85,10.21,9.57,8.91,8.28,7.55,7.13,6.53,5.91,5.65]
    for i in range(310,321):
        print("Volatilities for strike K="+str(i)+" is "+str(FindIMPvol(callprice[i-310], True, True, 311.97, i, 0.016,0.0184,135)))
main()
