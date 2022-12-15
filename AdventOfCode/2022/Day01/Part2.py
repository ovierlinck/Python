if __name__ == "__main__":
    with open("data1.txt", "r") as input:
        maxSum = list()
        currentSum = 0
        for line in input:
            if not line.strip():
                maxSum.append(currentSum)
                maxSum = sorted(maxSum, reverse=True)[0:3]

                currentSum = 0
                print("temp max = %s" % maxSum)
            else:
                value = int(line)
                currentSum += value

        print("Sum of MAX=%i" % sum(maxSum))
