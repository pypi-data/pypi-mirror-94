def isPrime_num(n):
    if n > 1:
        for i in range(2,n):
            if (n % i == 0):
                return False
                break
        else:
             return True
    else:
        return False
