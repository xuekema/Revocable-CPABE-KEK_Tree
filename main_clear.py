'''
    author:coco
    date:2022/6/12
    paper:A Traceable and Revocable Ciphertext-Policy Attribute-based Encryption Scheme Based on Privacy Protection
'''
from Tree import *
from Cover import *
from traceable_revocable_hidden_clear import *
from time import *

#系统用户列表
U = ['A','B','C','D','E']
tree = Tree()
list_u_id = tree.creatTree2(U)

#初始化双线行映射
grp = PairingGroup("SS512")

TRH = TRH_CPabe(grp)
begin = time()
(pk, msk) = TRH.Setup(tree)
end = time()
print('Setup time:',end - begin)


policy = '(identity and sex)'
T = {'IDENTITY': 'teacher', 'SEX': 'female'}
W = {'policy': policy, 'T':T}
m = grp.random(GT)
R = []
R_node = []
for i in R:
    temp = tree.SearchU(tree.root, i)
    R_node.append(temp[1])
begin = time()
CT = TRH.Encrypt(pk, m, W, R_node)
end = time()
print('Encyption time:', end - begin)

u = 'E'
id = list_u_id[u]
u_node_list = tree.SearchU(tree.root, u)
u_node = u_node_list[1]
S = {'IDENTITY':'teacher', 'SEX':'female'}
begin = time()
key = TRH.KeyGen(u_node, msk, pk, S)
end = time()
print('Keygeneration time:', end - begin)

###解密
begin = time()
message = TRH.Decrypt(u_node, pk, CT, key)
end = time()
print('message: ',message)
if message == m:
    print('success')
    print('Decryption time:', end - begin)
else:
    print('fail')

resKeyCheck = TRH.KeySanityCheck(key,pk)