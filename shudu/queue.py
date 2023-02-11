class Queue:
    def __init__(self):
        self.sz = 0
        self.its = []

    def push(self, x):
        self.sz += 1
        self.its.insert(0, x)

    def pop(self):
        print(self.its[len(self.its) - 1])
        return self.its.pop()

    def size(self):
        return self.sz


# q = Queue()
# q.push([8, 9])
# q.push([7, 8])
# q.push([6, 7])
# print(q.pop())
# print(q.pop())
# print(q.pop())
# for i in range(q.sz):
#     print(q.its[i])
