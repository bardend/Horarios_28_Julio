import random
import time

def random_long(a, b):
    return a + random.randint(0, b - a - 1)

maxn = 10
vis = [[0 for _ in range(maxn)] for _ in range(maxn)]

def f(n):
    global vis
    vis = [[0 for _ in range(maxn)] for _ in range(maxn)]
    ban, take = [], []
    ret = []
    for i in range(n):
        take.append(i)
    while len(ret) != (n * (n - 1)) // 2:
        if len(ban) + len(take) != n:
            print("bad")
        if not take:
            take = ban[:]
            ban.clear()
        if len(take) == 1:
            a = take[0]
            id = random_long(0, len(ban))
            b = ban[id]
            take.pop()
            for e in ban:
                if e != a and e != b:
                    take.append(e)
            ban.clear()
            ban.extend([a, b])
        else:
            id1 = random_long(0, len(take))
            a = take[id1]
            take.pop(id1)
            id2 = random_long(0, len(take))
            b = take[id2]
            take.pop(id2)
            ban.extend([a, b])
        if a == b:
            continue
        if a > b:
            a, b = b, a
        if not vis[a][b] and a < n and b < n:
            vis[a][b] = 1
            ret.append((a, b))
    return ret