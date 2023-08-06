
import os
import sys
import math
import random
import itertools
import csv

P = {'+': 1, '-': 1, '*': 2, '/': 2}

def calc(a, o, b):
    ea, eb = a['e'], b['e']
    va, vb = eval(a['e']), eval(b['e'])
    c = a['c'] + b['c']
    if 'o' in a and P[a['o']] < P[o]:
        ea = '(' + a['e'] + ')'
    if 'o' in b and P[o] > P[b['o']]:
        eb = '(' + b['e'] + ')'
    if 'o' in b and P[o] == P[b['o']]:
        if (o == '+' and b['o'] == '+') or (o == '*' and b['o'] == '*'):
            pass
        else:
            eb = '(' + b['e'] + ')'
    e = ea + o + eb
    if o == '+':
        c += 1
        if va + vb == 24:
            pass
        else: #和越大越复杂
            t = va + vb
            if t <= 10:
                pass
            else:
                c += t*1.2
    elif o == '-':
        c += 1
        t = va - vb
        if t < 0: #减出负数
            c += 100
    elif o == '*':
        c += 1
        if va == 1 and vb == 1: #与1相乘不增加复杂度
            pass
        elif va * vb == 24:
            pass
        else: #积越大越复杂
            t = va * vb
            if t <= 10:
                pass
            else:
                c += t
    elif o == '/':
        c += 2
        if va == vb: #相同数相除不增加复杂度
            pass
        else:
            c += 3
            y = math.modf(va / vb)[0]
            if y > 0: # 商为小数
                c += 800
                if math.modf(y * 100000)[0] > 0: #无理数
                    c += 800
    return {'r': eval(e), 'e': e, 'o': o, 'c': int(c)}

def node1_get(a):
    return [{'r': a, 'e': str(a), 'c': 0}]

def node2_get(a, b):
    A = a if isinstance(a, list) else node1_get(a)
    B = b if isinstance(b, list) else node1_get(b)
    z = [ ]
    for a in A:
        for b in B:
            if a['c'] < b['c']:
                z.append(calc(b, '+', a))
                z.append(calc(b, '*', a))
            else:
                z.append(calc(a, '+', b))
                z.append(calc(a, '*', b))

            z.append(calc(a, '-', b))
            z.append(calc(b, '-', a))
            if b['r'] != 0: z.append(calc(a, '/', b))
            if a['r'] != 0: z.append(calc(b, '/', a))
    return z

def node3_get(a, b, c):
    return node2_get(a, node2_get(b, c)) + \
           node2_get(b, node2_get(a, c)) + \
           node2_get(c, node2_get(a, b))

def node4_get(a, b, c, d):
    return node2_get(node2_get(a, b), node2_get(c, d)) + \
           node2_get(node2_get(a, c), node2_get(b, d)) + \
           node2_get(node2_get(a, d), node2_get(b, c)) + \
           node2_get(a, node3_get(b, c, d)) + \
           node2_get(b, node3_get(a, c, d)) + \
           node2_get(c, node3_get(a, b, d)) + \
           node2_get(d, node3_get(a, b, c))

def fx(target, values):
    n = len(values)
    if n == 4:
        z = node4_get(values[0], values[1], values[2], values[3])
    elif n == 3:
        z = node3_get(values[0], values[1], values[2])
    return list(filter(lambda x: math.isclose(x['r'], target, rel_tol=1e-10), z))

def show(z, n=99999, complex_fold=True):
    z.sort(key=lambda x: x['c'])
    i = 0
    e = []
    c = []
    for a in z:
        if i < n and a['e'] not in e:
            if complex_fold and a['c'] in c: continue
            e.append(a['e'])
            c.append(a['c'])
            print('{0:>4}={1:<16}{2}'.format(round(a['r']), a['e'], a['c']))
            i += 1

C = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 4

def All():
    D = list(itertools.combinations(C,4))
    S = []
    for v in D:
        u = [v[0], v[1], v[2], v[3]]
        u.sort()
        if u not in S:
            S.append(u)
    return S


def main():
    if len(sys.argv) >= 2:
        if sys.argv[1] in ['-h', '-H', '--help']:
            print('24p 1 2 3 4 # for query')
            print('24p # for play game')
            return

    v = list(map(lambda x: int(x), sys.argv[1:]))
    n = len(v)

    if n == 0:
        D = list(itertools.combinations(C,4))
        while True:
            v = []
            while True:
                v = list(random.choice(D))
                b = fx(24, v)
                if len(b) > 0: break
            os.system('clear')
            print('')
            print('\u2661', '\u2664', '  {}  {}  {}  {}  '.format(v[0], v[1], v[2], v[3]), '\u2667', '\u2662')
            if input('') != '': break
            show(b, 6)
            q = input('')
            if q == 'a': 
                show(b, 99999, False)
            elif q == 'b': 
                show(b, 99999)
            elif q == '': continue
            if input('') != '': break

    if n == 1:
        Q = int(sys.argv[1])
        S = All()
        for i, v in enumerate(S):
            b = fx(24, v)
            b.sort(key=lambda x: x['c'])
            if len(b) > 0:
                a = b[0]
                if Q < a['c']:
                    print('{}%'.format(int(i/len(S) * 100)), v, '{0:>4}={1:<16}{2}'.format(int(a['r']), a['e'], a['c']))

    if n == 2:
        Q1 = int(sys.argv[1])
        Q2 = int(sys.argv[2])
        S = All()
        for i, v in enumerate(S):
            b = fx(24, v)
            b.sort(key=lambda x: x['c'])
            if len(b) > 0:
                a = b[0]
                if Q1 < a['c'] and a['c'] < Q2:
                    print('{}%'.format(int(i/len(S) * 100)), v, '{0:>4}={1:<16}{2}'.format(int(a['r']), a['e'], a['c']))

    if n == 3:
        for a in ['3', '4', '6', '8', '12', '1/3', '1/4', '1/6', '1/8', '24', '48', '72', '96']:
            r = eval('1.0*' + a)
            b = fx(r, v)
            b.sort(key=lambda x: x['c'])
            if len(b) > 0:
                print(a +'='+ b[0]['e']) 

    if n == 4:
        show(fx(24, v))
