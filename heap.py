import heapq

class top_k_heap(object):
    def __init__(self, k):
        self.k = k
        self.data = []
 
    def push(self, elem):
        if len(self.data) < self.k:
            heapq.heappush(self.data, elem)
        else:
            topk_small = self.data[0]
            if elem > topk_small:
                heapq.heapreplace(self.data, elem)
 
    def top_k(self):
        return [x for x in reversed([heapq.heappop(self.data) for x in xrange(len(self.data))])]