from math import *
from node import *

class Tree(object):
    """树类"""
    def __init__(self, root = None):
        self.root = root

    def creatTree(self, U):
        #有bug,该函数创建的是满二叉树，而不是完全二叉树
        '''
        :param U:系統中用戶列表
        :return:返回树的根节点和用户身份编号字典
        '''
        n = len(U)
        N = 2 * n - 1
        nodelist = []
        identity_list = {}
        nodelist.append(Node(0))
        #计算树的深度
        depth = floor(log2(N)) + 1
        #依据节点个数算出树的深度，然后创建节点，并存在nodelist列表中
        for i in range(1, depth + 1):
            #树的每一层的节点实例化
            #每一层节点的编号为（2^(i-1),2^i-1）
            min = (int)(pow(2, i - 1))
            max = (int)(pow(2, i))
            for j in range(min, max):
                node = Node(j)
                if i == depth:
                    node.isleaf = True
                    identity_list[U[j-min]] = j
                nodelist.append(node)
        #print("len:", len(nodelist))
        #树的节点编号从1开始，将树中的节点依据二叉树的性质连接
        for i in range(1, len(nodelist)):
            node = nodelist[i]
            if(i != 1):
                node.parent = nodelist[(int)(i / 2)]
                #print(i,node.parent.id)
            if node.isleaf == False:
                node.lchild = nodelist[2 * i]
                node.rchild = nodelist[2 * i + 1]
        self.root = nodelist[1]
        return (nodelist[1], identity_list)

    def creatTree2(self, U):
        '''
        创建完全二叉树
        :param U:系統中用戶列表
        :return:返回树的根节点和用户身份编号字典
        '''
        n = len(U)
        N = 2 * n - 1
        # 存储节点的列表
        nodelist = [Node(0)]
        identity_list = {}
        for i in range(1, N+1):
            node = Node(i)
            nodelist.append(node)
        for i in range(1, N+1):
            # 非叶非父母节点
            if i != 1 and 2 * i + 1 <= N:
                nodelist[i].lchild = nodelist[2 * i]
                nodelist[i].rchild = nodelist[2 * i + 1]
                nodelist[i].parent = nodelist[(int)(i / 2)]
            # 根节点，无父母
            if i == 1:
                nodelist[i].lchild = nodelist[2 * i]
                nodelist[i].rchild = nodelist[2 * i + 1]
            # 叶结点
            if i != 1 and 2 * i > N:
                nodelist[i].parent = nodelist[(int)(i / 2)]
                nodelist[i].isleaf = True
                nodelist[i].u = U[i - n]
                identity_list[U[i - n]] = i
        self.root = nodelist[1]
        return identity_list

    #返回叶子节点到根节点的路径
    def getPath(self, leaf):
        if leaf == None:
            return []
        path = []
        temp = leaf
        while(temp.parent != None):
            path.insert(0,temp.id)
            #print("temp.id", temp.id)
            #print("temp.parent", temp.parent.id)
            temp = temp.parent
        path.insert(0,temp.id)
        return path

    def getPath2(self, leaf):
        if leaf == None:
            return []
        path = []
        temp = leaf
        while(temp.parent != None):
            # 每次在开头插入元素
            path.insert(0, temp)
            temp = temp.parent
        path.insert(0, temp)
        return path

    def preOrderTraversal(self, Root):
        if Root == None:
            return
        print(Root.id)
        self.preOrderTraversal(Root.lchild)
        self.preOrderTraversal(Root.rchild)
        #return Root.id

    def SearchU(self, Root, u):
        if Root == None:
            return
        if Root.isleaf:
            if Root.u == u:
                res = Root.id
                return [res, Root]
        #use = self.SearchU(Root.lchild, u)
        if self.SearchU(Root.lchild, u) == None:
            return self.SearchU(Root.rchild, u)
        else:
            return self.SearchU(Root.lchild, u)


