from queue import PriorityQueue

def BFS(start, expand):
    tiebreaker = 0
    queue = PriorityQueue()
    queue.put((0, tiebreaker, start))
    while not queue.empty():
        length, _, current = queue.get()
        yield current
        for adjacent in expand(current):
            tiebreaker += 1
            queue.put((length + 1, tiebreaker, adjacent))