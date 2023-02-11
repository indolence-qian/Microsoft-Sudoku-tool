# 测试文件
import pyautogui
import pytesseract
import time
from PIL import Image
import easyocr

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


def get_error():
    tt = []
    with open('data.txt', 'r+', encoding='utf-8') as f:
        for i in f:
            t = i.split(' ')
            # print(t)
            t[1] = t[1][0]
            print(t)
            tt.append(t)
    return tt


for i in range(N): maps[1 << i] = i
for i in range(M):
    for j in range(N):
        ones[i] += i >> j & 1

if __name__ == "__main__":
    while True:
        time.sleep(5)
        location = pyautogui.locateOnScreen('isRunning.png', confidence=0.9)
        if location != None:
            row, col, cell = [M - 1] * N, [M - 1] * N, [[M - 1] * 3 for _ in range(3)]
            # 获得截图
            for i in range(9):
                for j in range(9):
                    vi = i * 72 + i * 2 + i // 3 * 7
                    vj = j * 72 + j * 2 + j // 3 * 7
                    pyautogui.screenshot(str(i * 9 + j) + '.png', region=(354 + vj, 193 + vi, 72, 72))
                    image = Image.open(str(i * 9 + j) + '.png')
                    iimage = image.crop((2, 2, 70, 70))
                    iimage.save(str(i * 9 + j) + '.png')
            shudu = []
            # 开始图像识别
            data = get_error()
            print(data)
            text = easyocr.Reader(['ch_sim', 'en'], gpu=True)
            for i in range(9):
                for j in range(9):
                    flag = 0
                    for k in data:
                        print(k[0], ' ', k[1])
                        path = k[0]
                        an = k[1]
                        a = pyautogui.locate(path, str(i * 9 + j) + '.png', grayscale=True)
                        if a is not None:
                            shudu.append(an)
                            flag = 1
                            break
                    if flag:
                        continue
                    shuji = text.readtext(str(i * 9 + j) + '.png', detail=0)
                    if len(shuji) == 1:
                        shudu.extend(shuji)
                    else:
                        shudu.append('.')
                    print(i, ' ', j, ' ', shuji)
            # 开始数独运算
            lstr = shudu
            cnt = 0
            for i in range(N):
                for j in range(N):
                    if shudu[i * N + j] != '.':
                        t = int(shudu[i * N + j])
                        draw(i, j, t - 1, True)
                    else:
                        cnt += 1
            dfs(cnt)
            print(''.join(lstr))
            strs = ""
            for idx, i in enumerate(lstr):
                strs += str(i)
                if (idx + 1) % 9 == 0:
                    strs += '\n'
            print(strs)
            strs = strs + "\n\n答案有问题？请填写在下方输入框内,只看初始值"
            # 输出结果
            response = pyautogui.prompt(text=strs, title='数独答案', default="按行 列 正确值填写")
            if response is not None:
                res = response.split(' ')
                if len(res) != 3:
                    print("lens error!")
                elif res[0] < '0' or res[0] > '9' or res[1] < '0' or res[1] > '9' or res[2] < '0' or res[2] > '9':
                    print("data error!")
                else:
                    print(res)
                    image = Image.open(str(int(res[0]) * 9 + int(res[1])) + '.png')
                    image.save('t' + str(len(data)) + '.png')
                    f = open('data.txt', 'a+', encoding='utf-8')
                    f.write('\nt' + str(len(data)) + '.png ' + res[2])
                    f.close()
            # pyautogui.confirm(text='haha',title='答案',buttons=lstr)
            # print(shudu)
            # shuju = text.readtext('empty.png', detail=0)
            # print(shuju)
