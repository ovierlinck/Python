def follow1Dir(tail, head):
    if tail < head:
        return tail + 1
    if tail > head:
        return tail - 1
    return tail


def follow(tail, head):
    if abs(tail[0] - head[0]) <= 1 and abs(tail[1] - head[1]) <= 1:
        return tail

    return [follow1Dir(tail[0], head[0]), follow1Dir(tail[1], head[1], )]


if __name__ == "__main__":

    delta = {
        "U": [0, 1],
        "D": [0, -1],
        "L": [-1, 0],
        "R": [1, 0],
    }
    with open("data1.txt", "r") as input:

        head = [0, 0]
        tail = [0, 0]

        visited = set()
        visited.add("%i/%i" % (tail[0], tail[1]))

        for line in input:
            dir, steps = line.split()
            steps = int(steps)
            for i in range(steps):
                move = delta[dir]
                head[0] += move[0]
                head[1] += move[1]

                tail = follow(tail, head)
                print("Moving %s: HEAD: %s - TAIL: %s" % (dir, head, tail))

                visited.add("%i/%i" % (tail[0], tail[1]))

    print("Nb visited = %i" % len(visited))
    print(visited)
