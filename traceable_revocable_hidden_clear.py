'''
    paper: A traceble and Revocalble ciphertext-policy attribute-base encryption scheme based on privacy protection
    author: Coco
'''
from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.msp import MSP
from Cover import *
from AES import *

debug = False


class TRH_CPabe:
    def __init__(self, groupObj, verbose=False):
        global group
        self.group = groupObj
        self.util = MSP(self.group, verbose)

    # authority: input(lamda, A, T)
    def Setup(self, tree):
        '''

        :param T: 系统所有用户集合
        :return: 返回公钥和私钥
        '''

        if debug:
            print('\nSetup alogrithm:\n')
        g = self.group.random(G1)
        p = self.group.random(G1)
        a = self.group.random(ZR)
        alpha = self.group.random(ZR)
        h = self.group.random(G1)
        u = self.group.random(G1)

        # tree = Tree()
        # list_u_id = tree.creatTree2(U)

        X = {}
        Y = {}
        self.preOrderTraversal(tree.root, X, Y, g)

        K_temp = self.group.random(ZR)
        K = self.group.serialize(K_temp)
        # bytes to str
        K = K.decode('UTF-8')
        k = "".join(['' if i >= len(K) else K[i] for i in range(32)])
        # k_temp = self.group.random(ZR)
        # k = self.group.serialize(k_temp)
        egg_alpha = pair(g, g) ** alpha
        g_a = g ** a

        PP = {"p": p, "g": g, "h": h, "u": u, "egg_alpha": egg_alpha, "g_a": g_a, "Y": Y, "Tree": tree}
        MSK = {"a": a, "alpha": alpha, "X": X, "k": k}
        return PP, MSK

    # python在函数里传入列表 字典会改变他们的值
    def preOrderTraversal(self, Root, X, Y, g):
        '''
        :param Root: 树的根节点
        :param X: 保存树中每个节点的私钥部分-随机数
        :param Y: 保存树中每个节点的公钥部分
        :param g: 生成元
        :return: 递归把x,y存在字典里
        '''
        if Root == None:
            return
        xi = self.group.random(ZR)

        X[Root.id] = xi
        Y[Root.id] = g ** xi
        self.preOrderTraversal(Root.lchild, X, Y, g)
        self.preOrderTraversal(Root.rchild, X, Y, g)

    def Encrypt(self, PP, m, W, R_node):
        '''

        :param PP: 系统公共参数
        :param m: 需要加密的明文
        :param W: 访问控制方案，包括属性和属性值
        :param R: 撤销列表
        :return: 返回加密后的密文，其中包括部分访问策略
        '''
        if debug:
            print("\nencryption algorithm:\n")

        policy = self.util.createPolicy(W['policy'])
        mono_span_prog = self.util.convert_policy_to_msp(policy)
        num_cols = self.util.len_longest_row

        # t = []
        v = []
        # s = self.group.random(ZR)
        # v.append(s)
        for i in range(num_cols):
            # t.append(group.random(ZR))
            v.append(self.group.random(ZR))
        s = v[0]

        C = m * PP['egg_alpha'] ** s
        C0 = PP['g'] ** s
        C02 = PP['g_a'] ** s

        Ci1 = {}
        Ci2 = {}
        Ci3 = {}
        lamda_i_list = {}
        for attr, row in mono_span_prog.items():
            cols = len(row)
            lamda_i = 0
            for i in range(cols):
                lamda_i += row[i] * v[i]
            lamda_i_list[attr] = lamda_i
            t_i = self.group.random(ZR)
            C1 = (PP['h'] ** lamda_i) * (PP['u'] ** t_i)

            # get the name of the attributes
            attr_stripped = self.util.strip_index(attr)
            # 但是C2里是用属性名对应的属性值
            attr_value = W['T'][attr_stripped]
            # 如何将string类型的映射到群上
            attr_value_ZR = self.group.hash(attr_value, ZR)
            C2 = PP['g'] ** (-t_i * attr_value_ZR + lamda_i)

            C3 = PP['g'] ** t_i

            Ci1[attr] = C1
            Ci2[attr] = C2
            Ci3[attr] = C3

        Tree = PP['Tree']
        # R_node = []
        # for i in R:
        #     temp = Tree.SearchU(Tree.root, i)
        #     R_node.append(temp[1])
        T = {}
        mincover = cover(Tree, R_node)
        for node in mincover:
            T[node] = PP['Y'][node] ** s
            # T.append(PP['Y'][node] ** s)

        CT = {'C': C, 'C0': C0, 'C02': C02, 'Ci1': Ci1, 'Ci2': Ci2, 'Ci3': Ci3, 'T': T, 'R_node': R_node,
              'W_': W['policy']}
        return CT

    def KeyGen(self, u_node, msk, pk, S):
        '''

        :param u: 用户的身份
        :param msk: 主密钥
        :param pk: 系统公钥
        :param S:用户属性
        :return:用户解密密钥
        '''
        if debug:
            print('\n Key generation algorithm:\n')

        Tree = pk['Tree']
        # List = pk['Tree&List']['List']
        # id = List[u]
        # 用对称加密算法加密用户身份id
        # k = MSK['k'].decode('UTF-8')
        id = u_node.id
        k = msk['k']
        cipher = encrypt_AES(str(id), k)
        c = self.group.hash(cipher, ZR)

        # k = msk['k'].decode('UTF-8')
        # cipher = encrypt_AES(str(nodeId), k)
        # c = self.group.hash(cipher, ZR)
        r = self.group.random(ZR)

        K2 = c
        g = pk['g']
        a = msk['a']
        K = g ** (msk['alpha'] / (a + c)) * pk['h'] ** r
        L = g ** r
        L2 = g ** (a * r)

        K_tao = {}
        for key, value in S.items():
            s_tao = self.group.hash(value, ZR)
            v = g ** (s_tao * r) / pk['u'] ** ((a + c) * r)
            K_tao[key] = v

        X_i = {}
        path = Tree.getPath(u_node)
        for i in path:
            xi = msk['X'][i]
            X_i[i] = xi
        K_u = g ** (r / X_i[id])

        # # K_u = []
        #  X_i = {}
        #  for i in path:
        #      xi = msk['X'][i]
        #      # K_u.append(g ** (r / xi))
        #      X_i[i]  = xi
        #  K_u = g ** (r / msk['X'][path[-1]])

        SK = {'K2': K2, 'K': K, 'L': L, 'L2': L2, 'K_u': K_u, 'K_tao': K_tao, 'X_i': X_i, 'S': S, 'r': r, 'c': c}
        return SK

    def Decrypt(self, u_node, pk, CT, SK):

        if debug:
            print("\nDecrypt alogrithm:\n")
        # 先判断是否在撤销列表里
        R_node = CT['R_node']
        for i in R_node:
            if u_node is i:
                raise Exception("In the revocation list")

        user_atts = []
        for i in SK['S'].keys():
            user_atts.append(i)
        policy = self.util.createPolicy(CT['W_'])
        mono_span_prog = self.util.convert_policy_to_msp(policy)
        num_cols = self.util.len_longest_row

        pruned = self.util.prune(policy, user_atts)
        if pruned is False:
            raise Exception("Don't have the required attributes for decryption!")
        # coeffs = self.util.getCoefficients(policy)

        Tree = pk['Tree']
        path = Tree.getPath(u_node)

        coverList = cover(Tree, R_node)

        j = [i for i in path if i in coverList]
        x_j = SK['X_i'][j[0]]
        x_id = SK['X_i'][path[-1]]
        theta = x_id / x_j
        B = pair(SK['K_u'], CT['T'][j[0]]) ** theta

        F = 1
        e = 0
        for i in pruned:
            # attention:type(i) = binnode
            x = i.getAttributeAndIndex()
            y = i.getAttribute()
            i = str(i)
            a = pair((SK['L'] ** SK['K2']) * SK['L2'], CT['Ci1'][i])
            b = pair(SK['L'], CT['Ci2'][i])
            c = pair(SK['K_tao'][i], CT['Ci3'][i])
            F *= (a * b * c)
            e += 1

        D = pair(SK['K'], CT['C0'] ** SK['K2'] * CT['C02'])

        m = (CT['C'] * F) / (D * B)
        return m

    def KeySanityCheck(self, sk, pp):
        # first
        flag = True
        flag = flag and self.group.ismember(sk['K2']) and self.group.ismember(sk['K']) and self.group.ismember(
            sk['L']) and self.group.ismember(sk['L2']) and self.group.ismember(sk['K_u'])
        for i in sk['K_tao'].values():
            flag = flag and self.group.ismember(i)
        if flag:
            # second
            temp = pair(pp['g_a'], sk['L'])
            flag = flag and True if pair(pp['g'], sk['L2']) == temp and temp != 1 else False
            # third
            if flag:
                temp = pair(sk['K'], pp['g_a'] * (pp['g'] ** sk['K2']))
                flag = flag and True if temp == pp['egg_alpha'] * pair((sk['L'] ** sk['K2']) * sk['L2'],
                                                                       pp['h']) and temp != 1 else False
                # fourth
                if flag:
                    for key, value in sk['S'].items():
                        s_tao = self.group.hash(value, ZR)
                        temp = pair(sk['L'], pp['g']) ** s_tao
                        flag = flag and True if pair(sk['K_tao'][key], pp['g']) * pair((sk['L'] ** sk['K2']) * sk['L'],
                                                                                       pp['u']) and temp != 1 else False
                        if flag is False:
                            return False
                else:
                    return False
            else:
                return False
        else:
            return False
        return True
