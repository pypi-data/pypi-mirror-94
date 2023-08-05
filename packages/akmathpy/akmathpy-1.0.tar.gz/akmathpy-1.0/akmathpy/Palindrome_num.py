def isPalind_num(n):
    temp = n
    palind = 0
    while n > 0:
        digit = n % 10
        palind = palind*10+digit
        n=n//10
    if temp == palind:
        return True
    else:
        return False
