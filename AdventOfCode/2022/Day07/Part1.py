class Folder:
    def __init__(self, name, parent):
        self.parent = parent
        self.name = name
        self.localFiles = dict()  # map name to size
        self.children = list()


    def getChild(self, name):
        for c in self.children:
            if c.name == name:
                return c


    def getLocalSize(self):
        return sum(value for key, value in self.localFiles.items())


    def getTotalSize(self):
        return self.getLocalSize() + sum(c.getTotalSize() for c in self.children)


def dumpFolder(folder, prefix):
    print("%s FOLDER %s (local size:%i - full size:%i)" % (prefix, folder.name, folder.getLocalSize(), folder.getTotalSize()))
    for key, value in folder.localFiles.items():
        print("%s   %s (size:%i)" % (prefix, key, value))
    for subfolder in folder.children:
        dumpFolder(subfolder, prefix + "   ")


def search100000(folder):
    """
    Sum of sizes of folders with size <=100000, including folder
    :param folder:
    :return:
    """
    size = folder.getTotalSize()
    sum = size if size < 100000 else 0
    for subfolder in folder.children:
        sum += search100000(subfolder)

    return sum


if __name__ == "__main__":

    root = Folder("/", None)
    current = None

    with open("data1.txt", "r") as input:
        for line in input:
            line = line.strip()

            if line.startswith("$"):
                listingDir = False

            if line == "$ cd /":
                current = root
            elif line.startswith("$ cd "):
                childName = line[5:]
                if childName == "..":
                    current = current.parent
                else:
                    child = current.getChild(childName)
                    assert child is not None, "Folder '%s' should have a child named '%s' but has %s" % (
                        current.name, childName, ", ".join(c.name for c in current.children))
                    current = child
            elif line.startswith("$ ls"):
                listingDir = True
            else:
                assert listingDir
                if line.startswith("dir "):
                    dirName = line[4:]
                    if not current.getChild(dirName):
                        child = Folder(dirName, current)
                        current.children.append(child)
                else:
                    parts = line.split(" ")
                    size = int(parts[0])
                    name = parts[1]
                    if not current.localFiles.get(name):
                        current.localFiles[name] = size

    dumpFolder(root, "")

    print(search100000(root))
