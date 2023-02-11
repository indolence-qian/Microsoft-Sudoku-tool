# 常量
N, M = 9, 1 << 9
ones, maps = [0] * M, {}
# 变量
row, col, cell = [], [], []
lstr = []


def draw(x, y, t, is_set):
    if is_set:
        lstr[x * N + y] = str(t + 1)
    else:
        lstr[x * N + y] = '.'
    v = 1 << t
    if not is_set: v = -v
    row[x] -= v
    col[y] -= v
    cell[x // 3][y // 3] -= v


def lowbit(x):
    return x & -x


def get(x, y):
    return row[x] & col[y] & cell[x // 3][y // 3]


def dfs(cnt):
    if cnt == 0: return True
    minv = 10
    x, y = 0, 0
    for i in range(N):
        for j in range(N):
            if lstr[i * N + j] == '.':
                state = get(i, j)
                if ones[state] < minv:
                    minv = ones[state]
                    x, y = i, j
                    # 当只有一个位置可填时跳出循环
                    if minv == 1: break
        else:
            continue
        break
    state = get(x, y)
    while state:
        t = maps[lowbit(state)]
        draw(x, y, t, True)
        if dfs(cnt - 1): return True
        draw(x, y, t, False)
        state -= lowbit(state)
    return False


for i in range(N): maps[1 << i] = i
for i in range(M):
    for j in range(N):
        ones[i] += i >> j & 1

while True:
    strs = input().strip()
    if strs == 'end': break
    row, col, cell = [M - 1] * N, [M - 1] * N, [[M - 1] * 3 for _ in range(3)]
    lstr = list(strs)
    cnt = 0
    for i in range(N):
        for j in range(N):
            if strs[i * N + j] != '.':
                t = int(strs[i * N + j])
                draw(i, j, t - 1, True)
            else:
                cnt += 1
    dfs(cnt)
    print(''.join(lstr))
