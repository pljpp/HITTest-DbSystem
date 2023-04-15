'''
实验三第二部分
'''
import re
from treelib import Tree, Node

'''形式化表达式'''
exp1 = 'select [ename = \'Mary\' & dname = \'Research\'] (employee join department)'
exp2 = 'projection [bdate] (select [ename = \'John\' & dname = \'Research\'] (employee join department))'
exp3 = 'select [essn = \'01\'] (projection [essn, pname] (works_on join project))'
'''使用到的关系的属性'''
employee = ['ename', 'dno']
department = ['dname', 'dno', 'bdate']
project = ['pno', 'pname']
works_on = ['pno', 'essn']
attrdict = {'employee': employee, 'department': department, 'project': project, 'works_on': works_on}

def queryTree(exp):
    '''
    将形式化表达式转化为查询执行树
    :param exp: 形式化表达式
    :return: 成功返回查询执行树; 否则返回False
    '''
    assert isinstance(exp, str)
    template = r'^(select|projection)\s*\[([^\]]*)\]\s*\((.*)\)$'
    find = re.findall(template, exp, re.I)[0]
    assert len(find) == 3
    if find:
        # 行为(select或projection)
        action = find[0]
        assert action in ('select', 'projection')
        # 条件
        term = find[1]
        # from子句
        target = find[2]
        quetree = Tree()
        quetree.create_node(tag = '{} [{}]'.format(action, term), identifier = '{} [{}]'.format(action, term))
        tartree = targetTree(target)
        # 合并from子句的子树
        quetree.paste('{} [{}]'.format(action, term), tartree)
        return quetree
    else:
        return False

def targetTree(exp):
    '''
    将SQL形式化语句中对应from子句的部分转化为树
    :param exp: 形式化表达式
    :return: 查询执行树
    '''
    assert isinstance(exp, str)
    # select或projection语句
    if exp.startswith('select') or exp.startswith('projection'):
        quertree = queryTree(exp)
        return quertree
    # join运算
    else:
        template = r'^([\w]+)\s+join\s+([\w]+)$'
        find = re.findall(template, exp, re.I)[0]
        assert len(find) == 2
        if find:
            part1 = find[0]
            part2 = find[1]
            tartree = Tree()
            tartree.create_node(tag = 'join', identifier = 'join')
            tartree.create_node(tag = part1, identifier = part1, parent = 'join')
            tartree.create_node(tag = part2, identifier = part2, parent = 'join')
            return tartree

def optiTreeSelect(quetree):
    '''
    根据启发式关系代数优化算法(选择运算)优化查询执行树(因为语句最多只有2层选择/投影运算, 所以不以递归的方式实现)
    :param quetree: 查询执行树
    :return: 优化后的查询执行树
    '''
    assert isinstance(quetree, Tree)
    # 全部节点
    allnode = quetree.all_nodes()
    # 根节点
    root = allnode[0].tag
    # 选择移动到作用关系前
    if root.startswith('select'):
        template = r'^select\s+\[([^\]]*)\]$'
        # 条件
        find = re.findall(template, root, re.I)[0]
        termdict = getTermAttr(find)
        # 获得以select语句为根节点的子树的叶节点列表
        leave = [getTagNode(lef) for lef in quetree.leaves(root)]
        # 字典中剩余的键值对
        countdict = len(termdict)
        # 将选择运算移动到叶节点前
        for termkey in termdict.keys():
            termrela = getAttrRela(termkey)
            for forrela in termrela:
                if forrela in leave:
                    selexp = 'select [{}{}]'.format(termkey, termdict[termkey])
                    # 仅剩一个键值对(主要考虑到单条件的select子句: tree中不能含有相同的节点)
                    if countdict == 1:
                        quetree = deleteAbove(quetree, root)
                    quetree = insertAbove(quetree, forrela, selexp)
                    countdict = countdict - 1
        return quetree
    elif root.startswith('projection'):
        # 子节点
        nextnode = allnode[1].tag
        temptree = quetree.subtree(nextnode)
        newtree = optiTreeSelect(temptree)
        quetree.remove_node(nextnode)
        quetree.paste(root, newtree)
        return quetree
    else:
        return quetree

def optiTree(quetree, shadow = []):
    '''
    根据启发式关系代数优化算法优化查询执行树(因为语句最多只有2层选择/投影运算, 所以不以递归的方式实现)
    当且仅当节点是projection时, 其子树才可以进行投影优化
    :param quetree: 查询执行树
    :param shadow: 投影运算所需的属性列表, 默认为空
    :return: 优化后的查询执行树
    '''
    # 移动select运算
    quetree = optiTreeSelect(quetree)
    assert isinstance(quetree, Tree)
    # 全部节点
    allnode = quetree.all_nodes()
    # 根节点(两种情况: projection和join)
    root = allnode[0].tag
    # 对节点projection的子树进行优化
    def optiTreeJoin(quetree, root, shadow = []):
        '''
        优化投影运算
        :param quetree: 查询执行树
        :param root: 根节点(指定为'join')
        :param shadow: 投影运算所需的属性列表, 默认为空
        :return: 查询执行树
        '''
        assert root == 'join'
        # 获得其子树的叶节点
        leave = [getTagNode(lef) for lef in quetree.leaves(root)]
        assert len(leave) == 2
        # 获取叶节点作自然连接运算所需的公共关系(同时也是投影运算所需要的关系)
        attrcom = list(set(attrdict[leave[0]]) & set(attrdict[leave[1]]))
        shadow.extend(attrcom)
        # 在join之后增加投影算法
        for leaf in leave:
            childnode = quetree.parent(leaf).tag
            if childnode.startswith('select'):
                childnode = childnode
                # 获取shadow与attrdict[leaf]的交集->childnode子树的投影属性
                tempsd = list(set(shadow) & set(attrdict[leaf]))
            else:
                childnode = leaf
                tempsd = list(set(shadow) & set(attrdict[leaf]))
            node = 'projection {}'.format(tempsd)
            quetree = insertAbove(quetree, childnode, node)
        return quetree
    if root.startswith('projection'):
        # 其子节点必为join
        joinnode = quetree.is_branch(root)[0]
        assert joinnode == 'join'
        template = r'^projection\s+\[([^\]]+)\]'
        find = re.findall(template, root, re.I)[0]
        template = r'(\w+)'
        find = re.findall(template, find, re.I)
        shadow.extend(find)
        # 对join子树优化
        quetree = optiTreeJoin(quetree, joinnode, shadow)
    return quetree

def getTagNode(node):
    '''
    获得Node类型节点的名称
    :param node: 节点
    :return: 节点名称
    '''
    assert isinstance(node, Node)
    return node.tag

def getAttrRela(attr):
    '''
    获取含有特定属性的关系
    :param attr: 属性
    :return: 含有属性的关系
    '''
    rela = []
    for i, j in attrdict.items():
        if attr in j:
            rela.append(i)
    return rela

def insertAbove(quetree, child, node):
    '''
    在节点child之前插入node节点
    :param quetree: 查询执行树
    :param child: 节点标识
    :param node: 插入节点标识
    :return: 查询执行树
    '''
    assert isinstance(quetree, Tree)
    assert isinstance(child, str)
    assert isinstance(node, str)
    instree = Tree()
    parent = getTagNode(quetree.parent(child))
    instree.create_node(tag = node, identifier = node)
    # instree.create_node(tag = child, identifier = child, parent = node)
    temptree = quetree.subtree(child)
    instree.paste(node, temptree)
    quetree.remove_node(child)
    quetree.paste(parent, instree)
    return quetree

def deleteAbove(quetree, above):
    '''
    将优化时冗余的select[]节点删除(由于select[]的父节点唯一, 子节点唯一, 所以逻辑上不会出现问题)
    :param quetree: 查询执行树
    :param above: 可删除的节点(where子句)
    :return: 删除后的查询执行树
    '''
    # select的子节点只有一个
    child = quetree.is_branch(above)[0]
    # select的父节点
    parent = quetree.parent(above)
    deltree = quetree.subtree(child)
    # 待删除节点是根节点
    if parent is None:
        quetree = deltree
    # 待删除节点非根
    else:
        parent = parent.tag
        quetree.remove_node(above)
        quetree.paste(parent, deltree)
    return quetree

def getTermAttr(exp):
    '''
    将条件子句转化为{属性, 剩余部分}形式的字典
    :param exp: 条件子句
    :return: 字典形式的条件; 失败返回False
    '''
    template = r'([\w]+)(\s+[^&]+[^\s&])'
    find = re.findall(template, exp, re.I)
    if find:
        termdict = dict(find)
        return termdict
    return False
    
if __name__ == "__main__":
    quetree = queryTree(exp1)
    quetree.show()
    quetree = optiTree(quetree, [])
    quetree.show()
    del quetree
    quetree = queryTree(exp2)
    quetree.show()
    quetree = optiTree(quetree, [])
    quetree.show()
    del quetree
    quetree = queryTree(exp3)
    quetree.show()
    quetree = optiTree(quetree, [])
    quetree.show()
    del quetree
