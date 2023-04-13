class Node(object):
    """节点类"""

    def __init__(self, id, parent=None, lchild=None, rchild=None, isleaf=False):
        self.u = None
        self.id = id
        self.parent = parent
        self.lchild = lchild
        self.rchild = rchild
        self.isleaf = isleaf

    def getId(self):
        return self.id

    def getParent(self):
        return self.parent

    def getLchild(self):
        return self.lchild

    def getRchild(self):
        return self.rchild
