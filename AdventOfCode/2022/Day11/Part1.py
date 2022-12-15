import math


class Monkey:
    def __init__(self, id, items, operation, test, ifTrue, ifFalse):
        self.id = id
        self.items = items
        self.operation = operation
        self.test = test
        self.ifTrue = ifTrue
        self.ifFalse = ifFalse
        self.nbInspection = 0


    def __str__(self):
        txt = ("Monkey %i:\n" % self.id)
        txt += "  Starting items: %s\n" % ",".join(str(item) for item in self.items)
        txt += "  Operation: new = old%s\n" % self.operation
        txt += "  Test: divisible by %i\n" % self.test
        txt += "    If true: throw to monkey %i\n" % self.ifTrue
        txt += "    If false: throw to monkey %i\n" % self.ifFalse
        txt += "==> Nb inspections = %i\n" % self.nbInspection

        return txt


    def doItem(self, monkeys):
        item = self.items.pop(0)
        operator = self.operation[0]
        assert operator in ("*", "+"), "Unsupported operand for %s" % self
        operand = self.operation[2:]
        if operand == "old":
            operand = item
        else:
            operand = int(operand)

        if operator == "*":
            value = item * operand
        else:
            value = item + operand

        value = math.floor(value / 3)

        target = self.ifTrue if value % self.test == 0 else self.ifFalse

        print("Monkey %i gives item %i to monkey %i" % (self.id, value, target))
        monkeys[target].items.append(value)
        self.nbInspection += 1


    def doTurn(self, monkeys):
        while (self.items):
            self.doItem(monkeys)


def parseMonkey(lines):
    assert len(lines) == 6, "Lines must have 6 lines but got %s" % "\n".join(lines)
    starts = ["Monkey ", "  Starting items:", "  Operation: new = old ", "  Test: divisible by ", "    If true: throw to monkey ",
              "    If false: throw to monkey "]

    for i in range(6):
        assert lines[i].startswith(starts[i]), "Error line %i: '%s' must start with '%s" % (i, lines[i], starts[i])

    id = int(lines[0].rstrip()[len(starts[0]):-1])
    items = [int(v.strip()) for v in lines[1].rstrip()[len(starts[1]):].split(",")]
    operation = lines[2].rstrip()[len(starts[2]):]
    test = int(lines[3].rstrip()[len(starts[3]):])
    ifTrue = int(lines[4].rstrip()[len(starts[4]):])
    ifFalse = int(lines[5].rstrip()[len(starts[5]):])

    return Monkey(id, items, operation, test, ifTrue, ifFalse)


def doRound(monkeys):
    for monkey in monkeys:
        monkey.doTurn(monkeys)


if __name__ == "__main__":

    with open("data1.txt", "r") as input:
        lines = []
        monkeys = []
        for line in input:
            if not line.strip():
                monkey = parseMonkey(lines)
                monkeys.append(monkey)
                lines = []
            else:
                lines.append(line)

    print("== START =====================================================")
    for monkey in monkeys:
        print(monkey)
        print()
    print("==============================================================")

    for i in range(20):
        doRound(monkeys)

        print("== End of round %i =====================================================" % i)
        for monkey in monkeys:
            print(monkey)
            print()
        print("========================================================================")

    nbInspections = [m.nbInspection for m in monkeys]
    nbInspections.sort(reverse=True)
    print("Nb Inspections = %s" % nbInspections)
    print("product=%i" % (nbInspections[0] * nbInspections[1]))
