def stairs(n, N, X):
    X.add(n)
    if isLegal():
        if isSolution():
            print(str(X))
        else:
            stairs(n, N, X)

def isLegal(N, X):
    sum = 0
    for num in X:
        sum += X
        if sum > N:
            return False
    if len(X) > N:
        return False
    else:
        return True

def isSolution(N, X):
    sum = 0
    for num in X:
        sum += num
        if sum > N:
            return False
    if N == sum:
        return True
    else:
        return False

