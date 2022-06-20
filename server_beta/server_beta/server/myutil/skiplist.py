# coding=utf-8
# 跳表的Python实现

import random

# 最高层数设置为4
MAX_LEVEL = 4


def randomLevel():
    k = 1
    while random.randint(1, 100) % 2:
        k += 1
    k = k if k < MAX_LEVEL else MAX_LEVEL
    return k


def traversal(skiplist):
    level = skiplist.level
    i = level - 1
    while i >= 0:
        level_str = 'header'
        header = skiplist.header
        while header:
            level_str += ' -> %s' % header.key
            header = header.forward[i]
        #print(level_str)
        i -= 1


class Node(object):
    def __init__(self, level, key, value):
        self.key = key
        self.value = value
        self.forward = [None] * level


class Skiplist(object):
    def __init__(self):
        self.level = 0
        self.header = Node(MAX_LEVEL, 0, 0)

    def insert(self, key, value):
        # 更新的最大层数为 MAX_LEVEL 层
        update = [None] * MAX_LEVEL
        p = self.header
        q = None
        k = self.level
        i = k - 1
        # i from k-1 to 0
        while i >= 0:
            q = p.forward[i]
            while q and q.key < key:
                p = q
                q = p.forward[i]
            update[i] = p
            i -= 1
        if q and q.key == key:
            return False

        k = randomLevel()
        if k > self.level:
            i = self.level
            while i < k:
                update[i] = self.header
                i += 1
            self.level = k

        q = Node(k, key, value)
        i = 0
        while i < k:
            q.forward[i] = update[i].forward[i]
            update[i].forward[i] = q
            i += 1

        return True

    def delete(self, key):
        update = [None] * MAX_LEVEL
        p = self.header
        q = None
        k = self.level
        i = k - 1
        # 跟插入一样 找到要删除的位置
        while i >= 0:
            q = p.forward[i]
            while q and q.key < key:
                p = q
                q = p.forward[i]
            update[i] = p
            i -= 1
        if q and q.key == key:
            i = 0
            while i < self.level:
                if update[i].forward[i] == q:
                    update[i].forward[i] = q.forward[i]
                i += 1
            del q
            i = self.level - 1
            while i >= 0:
                if not self.header.forward[i]:
                    self.level -= 1
                i -= 1
            return True
        else:
            return False

    def search(self, key):
        i = self.level - 1
        while i >= 0:
            q = self.header.forward[i]
            while q and q.key <= key:
                if q.key == key:
                    return q.key, q.value, i
                q = q.forward[i]
            i -= 1
        return None


def main():
    import random
    number_list=[]
    for i in range(50000):
        number_list.append(i*2 + random.randint(-2, 2))
    skiplist = Skiplist()
    for number in number_list:
        skiplist.insert(number, None)

    '''traversal(skiplist)
    print(skiplist.search(9634))
    skiplist.delete(4)
    traversal(skiplist)'''
    
    import time
    iTime1=time.time()
    print(skiplist.search(9634))
    iTime2=time.time()
    
    iTime3=time.time()
    print(9634 in number_list)
    iTime4=time.time()
    
    print("skiplist:%s, list%s"%(iTime2-iTime1, iTime4-iTime3))

if __name__ == '__main__':
    main()