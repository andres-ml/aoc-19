from queue import PriorityQueue

def BFS(start, expand):
    queue = PriorityQueue()
    queue.put((0, start))
    while not queue.empty():
        length, current = queue.get()
        yield current
        for adjacent in expand(current):
            queue.put((length + 1, adjacent))