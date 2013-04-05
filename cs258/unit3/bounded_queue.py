# TASK:
#
# Write a random tester for the Queue class.
# The random tester should repeatedly call 
# the Queue methods on random input in a 
# semi-random fashion. for instance, if 
# you wanted to randomly decide between 
# calling enqueue and dequeue, you would 
# write something like this:
#
# q = Queue(500)
# if (random.random() < 0.5):
#     q.enqueue(some_random_input)
# else:
#     q.dequeue()
#
# You should call the enqueue, dequeue, 
# and checkRep methods several thousand 
# times each.

import array
import random

class Queue:
    def __init__(self,size_max):
        assert size_max > 0
        self.max = size_max
        self.head = 0
        self.tail = 0
        self.size = 0
        self.data = array.array('i', range(size_max))

    def empty(self):
        return self.size == 0

    def full(self):
        return self.size == self.max

    def enqueue(self,x):
        if self.size == self.max:
            return False
        self.data[self.tail] = x
        self.size += 1
        self.tail += 1
        if self.tail == self.max:
            self.tail = 0
        return True

    def dequeue(self):
        if self.size == 0:
            return None
        x = self.data[self.head]
        self.size -= 1
        self.head += 1
        if self.head == self.max:
            self.head = 0
        return x

    def checkRep(self):
        assert self.tail >= 0
        assert self.tail < self.max
        assert self.head >= 0
        assert self.head < self.max
        if self.tail > self.head:
            assert (self.tail-self.head) == self.size
        if self.tail < self.head:
            assert (self.head-self.tail) == (self.max-self.size)
        if self.head == self.tail:
            assert (self.size==0) or (self.size==self.max)

# Write a random tester for the Queue class.
def test():
    N = 100
    for i in range(N):
        size = random.randint(1,10000)
        q = Queue(size)
        q.checkRep()
        is_empty = q.empty()
        q.checkRep()
        assert is_empty
        is_full = q.full()
        q.checkRep()
        assert not is_full

        # stress dequeue when empty
        for i in range(size+1):
            succ = q.dequeue()
            q.checkRep()
            assert succ is None
            is_empty = q.empty()
            q.checkRep()
            assert is_empty
            is_full = q.full()
            q.checkRep()
            assert not is_full

        # stress normal enqueue
        l = []
        for i in range(size):
            x = random.randint(1,1000000)
            succ = q.enqueue(x)
            q.checkRep()
            assert succ
            l.append(x)
        is_full = q.full()
        q.checkRep()
        assert is_full
        is_empty = q.empty()
        q.checkRep()
        assert not is_empty

        # stress enqueue when full
        for i in range(size+1):
            succ = q.enqueue(i)
            q.checkRep()
            assert not succ
            is_full = q.full()
            q.checkRep()
            assert is_full
            is_empty = q.empty()
            q.checkRep()
            assert not is_empty

        # stress normal dequeue
        for i in range(size):
            value = q.dequeue()
            q.checkRep()
            v = l.pop(0)
            assert value == v
            is_full = q.full()
            q.checkRep()
            assert not is_full
            is_empty = q.empty()
            q.checkRep()
            if i < size-1:
                assert not is_empty
            else:
                assert is_empty
        is_empty = q.empty()
        q.checkRep()
        assert is_empty
        is_full = q.full()
        q.checkRep()
        assert not is_full

        # stress dequeue when empty again
        for i in range(size+1):
            succ = q.dequeue()
            q.checkRep()
            assert succ is None
            is_empty = q.empty()
            q.checkRep()
            assert is_empty
            is_full = q.full()
            q.checkRep()
            assert not is_full


test()


