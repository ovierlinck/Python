def drawPixel(i, x, pixels):
    if i % 40 == 0:
        pixels += "\n"

    if abs((i % 40) - x) <= 1:
        pixels += "#"
    else:
        pixels += "."

    print(pixels)

    return pixels


if __name__ == "__main__":

    with open("data1.txt", "r") as input:

        i = 0
        x = 1
        pixels = ""

        for line in input:
            pixels = drawPixel(i, x, pixels)

            if line.startswith("addx"):
                increment = int(line.split(" ")[1].strip())
                print("%i %s" % (i, line.strip(" \n")))
                i += 1
                pixels = drawPixel(i, x, pixels)

                x += increment
                print("%i   +%i => x=%i" % (i, increment, x))
            else:  # noop
                print("%i noop" % i)

            i += 1

    print(pixels)
