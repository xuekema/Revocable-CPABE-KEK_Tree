'''查找覆盖集, 先找到撤销列表中所有节点的路径集合，然后判断生成最小覆盖集'''

# def cover(t: Tree, reList: List[Node]) -> List[Node]:
def cover(tree, reList):
    minCover = []
    revocable = []
    for node in reList:
        tempList = tree.getPath2(node)
        #print(tempList)
        for i in tempList:
            if i not in revocable:
                revocable.append(i)
    #测试
    # for i in revocable:
    #     print(i.id)
    for i in revocable:
        #print("i:",i.id)
        if i.isleaf == True:
            #print("isleaf")
            continue
        if i.lchild not in revocable:
            #print("i.lchild:", i.lchild.id)
            minCover.append(i.lchild.id)
        if i.rchild not in revocable:
            #print("i.rchild:", i.rchild.id)
            minCover.append(i.rchild.id)
    if len(revocable) == 0:
        minCover.append(1)

    return minCover




# def findNotReco(tree, revoList, node):
#     if node.lchild not in revoList:
#         return node.lchild
#     if node.rchild not in revoList:
#         return node.rchild
#