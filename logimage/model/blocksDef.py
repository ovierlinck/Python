class IBlocksDef:
    """
    Interface for definition of blocks, i.e. list of block size + info to ease solving
    """


    def getNbDefs(self):
        pass


    def getDef(self, index):
        pass


class BlocksDef(IBlocksDef):
    """
    Basic implementation of IBlocksDef
    """


    def __init__(self, blocks):
        """
        :param iterable of block size:
        """
        self.blocks = [block for block in blocks]  # Internal copy


    def __str__(self):
        return "BlockDefs[%s]" % ",".join(str(b) for b in self.blocks)


    def getNbDefs(self):
        return len(self.blocks)


    def getDef(self, index):
        return self.blocks[index]
