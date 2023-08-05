def isArms_num(n):
    temp = n
    sum = 0
    while temp > 0:
        digit = temp % 10
        sum = sum + digit ** 3
        temp = temp // 10
    if n == sum:
        return True
    else:
        return False