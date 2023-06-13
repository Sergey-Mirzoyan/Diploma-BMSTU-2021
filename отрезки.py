from random import randint
from math import *
import time
import timeit
import pickle
import numpy as np
import os
import sys
sys.set_int_max_str_digits(0)

def fill (W, H):
    current_field = next_field = [[0 for i in range(W)] for j in range(H)]
    entrp = 0
    while entrp == 0:
        entrp = round((time.process_time_ns() * timeit.timeit()))#% (W*H)/2
        entrp = entrp % 10000
    print(entrp)
    current_field = [[2 if i == W // entrp or j == H // entrp else 0 for i in range(W)] for j in range(H)]  
    for j in range (W):
        for i in range(H):
            if i != 0 and j!= 0:
                if entrp % i == 0 or entrp % j== 0:
                    current_field[i][j] = i % 3
                elif i > j and not (2 * i + j) % 4:
                    current_field[i][j] = 2 
                else:
                    current_field[i][j-i] = 1
    return next_field, current_field

def check_cell(current_field, x, y,W, H):
    count = 0
    
    for j in range(y - 1, y + 2):
        for i in range(x - 1, x + 2):
            if current_field[j % H][i % W] != 0:
                count += 1
    # Zombie
    if current_field[y][x] == 2:
        count -= 1
        if count == 2 or count == 4:
            return 2
        return 0
    else:
        if count == 6:
            return 2

    # Alive
    if current_field[y][x] == 0:
        count -= 1
        if count == 2 or count == 3:
            return 1
        return 0
    else:
        if count == 3:
            return 1
        return 0

def life(W, H, next_field, current_field, tries):
    for k in range(tries):
        for x in range(1, W - 1):
            for y in range(1, H - 1):
                next_field[y][x] = check_cell(current_field, x, y,W,H)
          
        current_field = [*next_field]
    
    return current_field
        
def print_field(field, W, H, pref):
     if H!= 0:    
        f = open('nums'+pref+'.txt','w')
        for i in range(len(field)):
            buf = ''
            for j in range(len(field[i])):
                buf += str(field[i][j])
            f.write(buf+'\n')
        f.close()
     else:
        f = open('nums'+pref+'.txt','w')
        buf = ''
        for i in range(len(field)):
            buf += str(field[i])+''
        f.write(buf)
        f.close()
    
def convert_base(num, to_base, from_base):
    # first convert to decimal number
    n = int(num, from_base) if isinstance(num, str) else num
    # now convert decimal to 'to_base' base
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = ""
    while n > 0:
        n,m = divmod(n, to_base)
        res += alphabet[m]
    return res[::-1]

def Knut_test(U, flag):
    n = len(U)
    u2 = 0
    u_sum2 = 0
    # print(U)
    if isinstance(U[0], str):
        for i in range(len(U)):
            U[i] = int(U[i])

    u_sum2 = sum(U)**2
    U1U2 = 0
    for i in range(n-1):
        U1U2 += U[i]*U[i+1]
        u2 += U[i]**2
    C = (n*U1U2 - u_sum2)/(n*u2 - u_sum2)
    un = (-1)/(n-1)
    sigma = sqrt((n**2)/(((n-1)**2)*(n-2)))
    if flag == 1:
        if un - 2*sigma < C < un + 2*sigma:
            print('Хорошее значение - ', C)
            
        else:
            print('Нехорошее значение - ', C)
            
    return C

def choise_line(current_field):
    summ = 0
    summax = 0
    masmax = []
    cmin = 1
    x = []
    masK = []
    masnum = []
    KK = 0
    for k in range(1,len(current_field)-1):
        x = current_field[k]
        masK.append(k)
        num = ''
        num3 = ''
        for j in x:
            num += str(j)
            num3 += str(j)
        
        if sum(x) == 0:
            continue
        num = convert_base(num, 2, 3)
        num = list(num)
        
        c = Knut_test(num, 0)
        if c == '!!!':
            continue
        if abs(c) < cmin:
            masmax = num
            masnum = num3
            cmin = c
            KK = k
    print("K: ", KK)
    return KK, masmax, masnum
    


def read_bits(bits, length, count=None):
    masnums = ''.join(str(i) for i in bits)
    return masnums[:length]

rand_nums1 = []
def ranging1(W, H, current_field, tries, KK, a, b):
    # life(W, H, current_field, current_field, tries)
    # rand_nums = []
    next_field = current_field 
    for k in range(tries):
        for x in range(1, W - 1):
            for y in range(1, H - 1):
                next_field[y][x] = check_cell(current_field, x, y,W,H)
        
        rand_nums1.append(ranging(current_field[KK], a, b))
        # print(k)
        current_field = [*next_field]
    return rand_nums1
    
# def main():
W, H = 3000, 100
tries = 12
repeats = 100
minimum, maximum = 1000,100000

print("\tFill......................................................................./")
current_field, next_field = fill(W,H)

print("\tlife......................................................................./")
current_field = life(W, H, next_field, current_field, tries)

# print("\tprint....................................................................../")
# print_field(current_field, W, H, '_current_field')

print("\tChose line................................................................./")
line_indx, line, line3 = choise_line(current_field)
   
# print("\tprint_the_line3............................................................/")
# print_field(line3, W, 0, '_3')
    
print("\tprint_the_result.........................................................../")
print_field(line, W, 0, '')
    
# start = time.time()    
# main()
# end = time.time()
# print('WORK TIME: ', end - start)