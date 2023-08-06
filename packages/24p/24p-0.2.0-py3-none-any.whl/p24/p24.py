
import os
import sys
import time
import signal
import math
import random
import itertools
import csv


def calc(a, o, b):
    P = {'+': 1, '-': 1, '*': 2, '/': 2}
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

def get1(a):
    return [{'r': a, 'e': str(a), 'c': 0}]

def get2(a, b):
    A = a if isinstance(a, list) else get1(a)
    B = b if isinstance(b, list) else get1(b)
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

def get3(a, b, c):
    return get2(a, get2(b, c)) + \
           get2(b, get2(a, c)) + \
           get2(c, get2(a, b))

def get4(a, b, c, d):
    return get2(get2(a, b), get2(c, d)) + \
           get2(get2(a, c), get2(b, d)) + \
           get2(get2(a, d), get2(b, c)) + \
           get2(a, get3(b, c, d)) + \
           get2(b, get3(a, c, d)) + \
           get2(c, get3(a, b, d)) + \
           get2(d, get3(a, b, c))

def fx(target, values):
    n = len(values)
    if n == 4:
        z = get4(values[0], values[1], values[2], values[3])
    elif n == 3:
        z = get3(values[0], values[1], values[2])
    return list(filter(lambda x: math.isclose(x['r'], target, rel_tol=1e-10), z))

def fy(z, complex_fold=True):
    z.sort(key=lambda x: x['c'])
    e = []
    c = []
    d = []
    for a in z:
        if a['e'] not in e:
            if complex_fold and a['c'] in c: continue
            e.append(a['e'])
            c.append(a['c'])
            d.append({'e': str(round(a['r'])) + '=' + a['e'], 'c': a['c']})
    return d

################################

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


def sigint_handler(signum, frame):
    print ('catched interrupt signal!')
    exit()


status = ''
start = 0
result = []
def new_question(space):
    global status, start, result
    v, b = [], []
    while True:
        v = list(random.choice(space))
        b = fx(24, v)
        if len(b) > 0: break
    os.system('clear')
    print('')
    print('\u2661', '\u2664', '  {}  {}  {}  {}  '.format(v[0], v[1], v[2], v[3]), '\u2667', '\u2662')
    status = "new question"
    start = int(time.time())
    return b

def show_answer(d, n, f, delta):
    global status, start, result
    r = fy(d, f)
    if n == 1:
        print(r[0]["e"])
        print("")
        print("complexity", r[0]["c"])
        print("total", len(r), "solutions")
        print("cost", delta, "seconds")
    else:
        for i, a in enumerate(r):
            if i < n:
                print('{0:<16}{1}'.format(a['e'], a['c']))
    status = "show answer"

def main():
    global status, start, result
    if len(sys.argv) >= 2:
        if sys.argv[1] in ['-h', '-H', '--help']:
            print('24p 1 2 3 4 # for query')
            print('24p # for play game')
            return

    signal.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGHUP, sigint_handler)
    signal.signal(signal.SIGTERM, sigint_handler)

    v = list(map(lambda x: int(x), sys.argv[1:]))
    n = len(v)

    if n == 0:
        space = list(itertools.combinations(C,4))
        result = new_question(space)
        while True:
            Q = input('')
            if Q == 'q': exit()
            if status == "new question":
                delta = int(time.time()) - start
                if Q == "":
                    show_answer(result, 1, True, delta)
                else:
                    if Q == "a": show_answer(result, 99999, False, delta)
                    elif Q == "b": show_answer(result, 99999, True, delta)
                    elif Q == "n": show_answer(result, 99999, True, delta)
                    print("cost ", delta, " seconds")
    
            elif status == "show answer":
                if Q == "a": show_answer(result, 99999, False, 0)
                elif Q == "b": show_answer(result, 99999, True, 0)
                else: result = new_question(space)

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
        show_answer(fx(24, v), 99999, False, 0)
