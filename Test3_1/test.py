'''
实验三第一部分
'''
import extmem
import handle

def testSelect(buffer, ra = 40, sc = 60):
    '''
    关系选择算法
    :param buffer: 缓冲区
    :param ra: R关系中的A属性, 默认40
    :param sc: S关系中的C属性, 默认60
    '''
    # 关系R
    num = 0
    for i in range(16):
        # 从磁盘块读信息
        addr = 'r' + str(i)
        n = buffer.readBlockFromDisk(addr)
        for j in range(7):
            a = int(buffer.data[n][2 * j])
            b = int(buffer.data[n][2 * j + 1])
            if a == ra:
                print('testSelect_R: ', a, b)
                num = num + 1
                buffer.data[1].append(a)
                buffer.data[1].append(b)
                if num % 7 == 0:
                    buffer.writeBlockToDisk('testSelect_R' + str((num - 1) // 7), 1)
                    buffer.freeBlockInBuffer(1)
        buffer.freeBlockInBuffer(n)
    # 元组不足8的块
    if num % 7 != 0:
        buffer.writeBlockToDisk('testSelect_R' + str((num - 1) // 7), 1)
        buffer.freeBlockInBuffer(1)
    # 关系S
    num = 0
    for i in range(32):
        addr = "s" + str(i)
        n = buffer.readBlockFromDisk(addr)
        for j in range(7):
            c = int(buffer.data[n][2 * j])
            d = int(buffer.data[n][2 * j + 1])
            if (c == sc):
                print("testSelect_S: ", c, d)
                num = num + 1
                buffer.data[1].append(c)
                buffer.data[1].append(d)
                if num % 7 == 0:
                    buffer.writeBlockToDisk('testSelect_S' + str((num - 1) // 7), 1)
                    buffer.freeBlockInBuffer(1)
        buffer.freeBlockInBuffer(n)
    # 元组不足8的块
    if num % 7 != 0:
        buffer.writeBlockToDisk('testSelect_S' + str((num - 1) // 7), 1)
        buffer.freeBlockInBuffer(1)
    
def testShadow(buffer, relation = 'R', attribute = 'A'):
    '''
    关系投影算法
    :param buffer: 缓冲区
    :param relation: 关系, 默认R
    :param attribute : 属性, 默认A
    '''
    assert relation == 'R' or relation == 'S'
    assert attribute == 'A' or attribute == 'B' or attribute == 'C' or attribute == 'D'
    print('>>>>Relation: ', relation, 'Shadow: ', attribute)
    # 定义偏移量
    if attribute == 'A' or attribute == 'C':
        bias = 0
    else:
        bias = 1
    # 定义块总数
    if relation == 'R':
        total = 16
    else:
        total = 32
    # 定义集合剔除重复元素
    shadow = set()
    for i in range(total):
        fnm = 'r' + str(i)
        brd = buffer.readBlockFromDisk(fnm)
        for j in range(7):
            bsd = buffer.data[brd][2 * j + bias]
            shadow.add(bsd)
        buffer.freeBlockInBuffer(brd)
    # 申请新块存储投影
    tosd = buffer.getNewBlockInBuffer()
    count = 0
    num = 0
    for item in shadow:
        buffer.data[tosd].append(item)
        print(item, end = ' ')
        count = count + 1
        if count % 14 == 0 and count != 0:
            buffer.writeBlockToDisk('testShadow' + str(num), tosd)
            num = num + 1
            print()
            buffer.freeBlockInBuffer(tosd)
            tosd = buffer.getNewBlockInBuffer()
    # 补全剩余
    if 14 * num < len(shadow):
        buffer.writeBlockToDisk('testShadow' + str(num), tosd)
        print()
        buffer.freeBlockInBuffer(tosd)
    
def testNLJ(buffer):
    '''
    实现循环嵌套连接NLJ算法(采用6块外层循环, 1块内层循环, 1块存储结果)
    :param buffer: 缓冲区
    '''
    # 释放缓冲区
    buffer.freeBuffer()
    num = 0
    nljlist = []
    # 将体积大的S属性作为内层, 体积小的R属性作为外层
    # R属性采用6块存储只需要循环3次: 16/6向上取整
    for i in range(3):
        br = []
        # 清空缓冲区
        buffer.freeBuffer()
        for j in range(6):
            if 6 * i + j >= 16:
                break
            rr = buffer.readBlockFromDisk('r' + str(6 * i + j))
            br.append(rr)
        for rt in br:
            for k in range(32):
                rs = buffer.readBlockFromDisk('s' + str(k))
                for li in range(7):
                    for lj in range(7):
                        if buffer.data[rt][2 * li] == buffer.data[rs][2 * lj]:
                            nljlist.append(buffer.data[rt][2 * li])
                            nljlist.append(buffer.data[rt][2 * li + 1])
                            nljlist.append(buffer.data[rs][2 * lj + 1])
                            # 写入磁盘(1个块)
                            if len(nljlist) % 21 == 0:
                                num = len(nljlist)
                                templist = nljlist[num - 21: num].copy()
                                bjoin = buffer.getNewBlockInBuffer()
                                for item in range(0, len(templist), 3):
                                    buffer.data[bjoin].append(templist[item])
                                    buffer.data[bjoin].append(templist[item + 1])
                                    buffer.data[bjoin].append(templist[item + 2])
                                buffer.writeBlockToDisk('testNLJ' + str(num // 21 - 1), bjoin)
                                buffer.freeBlockInBuffer(bjoin)
                                templist = []
                # 清除S关系的块
                buffer.freeBlockInBuffer(rs)
    # 处理最后一次写入文件或者不满7个元组的文件
    if num < len(nljlist):
        templist = nljlist[num: len(nljlist)].copy()
        bjoin = buffer.getNewBlockInBuffer()
        for item in range(0, len(templist), 3):
            buffer.data[bjoin].append(templist[item])
            buffer.data[bjoin].append(templist[item + 1])
            buffer.data[bjoin].append(templist[item + 2])
        # num未作改变
        buffer.writeBlockToDisk('testNLJ' + str(num // 21), bjoin)
        buffer.freeBlockInBuffer(bjoin)
    
def testSMJ(buffer):
    '''
    实现排序归并连接SMJ算法(6块关系R, 1块关系S, 1块结果)
    外层采用BLJ算法, 内层采用SMJ算法
    :param buffer: 缓冲区
    '''
    # 释放缓冲区
    buffer.freeBuffer()
    smjlist = []
    for i in range(3):
        # 清空缓冲区
        buffer.freeBuffer()
        smjr = blocksort(buffer, 'R', 6 * i)
        for j in range(32):
            smjs = blocksort(buffer, 'S', j)
            for k in range(0, len(smjr), 2):
                for l in range(0, len(smjs), 2):
                    if smjs[l] == smjr[k]:
                        smjlist.append(smjs[l])
                        smjlist.append(smjs[l + 1])
                        smjlist.append(smjr[k + 1])
                        # 写入文件(1个块)
                        if len(smjlist) % 21 == 0:
                            num = len(smjlist)
                            templist = smjlist[num - 21: num].copy()
                            sjoin = buffer.getNewBlockInBuffer()
                            for item in range(0, len(templist), 3):
                                buffer.data[sjoin].append(templist[item])
                                buffer.data[sjoin].append(templist[item + 1])
                                buffer.data[sjoin].append(templist[item + 2])
                            buffer.writeBlockToDisk('testSMJ' + str(num // 21 - 1), sjoin)
                            buffer.freeBlockInBuffer(sjoin)
                            templist = []
                    # S.C<R.A, 则S向前移动
                    elif smjs[l] < smjr[k]:
                        pass
                    # S.C>R.A, 则关系S之后的元组都大于R的元组, 应该跳过此次S关系的循环
                    else:
                        continue
    # 释放缓冲区
    # 处理最后一次写入文件或者不满7个元组的文件
    buffer.freeBuffer()
    if num < len(smjlist):
        templist = smjlist[num: len(smjlist)].copy()
        sjoin = buffer.getNewBlockInBuffer()
        for item in range(0, len(templist), 3):
            buffer.data[sjoin].append(templist[item])
            buffer.data[sjoin].append(templist[item + 1])
            buffer.data[sjoin].append(templist[item + 2])
        # num未作改变
        buffer.writeBlockToDisk('testSMJ' + str(num // 21), sjoin)
        buffer.freeBlockInBuffer(sjoin)
    
def testHJ(buffer):
    '''
    实现哈希连接HJ算法(只采用最简单的模哈希算法)
    :param buffer: 缓冲区
    '''
    # 释放缓冲区
    buffer.freeBuffer()
    # 哈希桶: 存储文件号和元组偏移
    dr = {}
    ds = {}
    # 模数
    divisor = 10
    # 关系R的哈希文件
    for i in range(16):
        rr = buffer.readBlockFromDisk('r' + str(i))
        for j in range(7):
            a = int(buffer.data[rr][2 * j])
            if a % divisor in dr.keys():
                dr[a % divisor].append((i, j))
            else:
                dr[a % divisor] = []
                dr[a % divisor].append((i, j))
        buffer.freeBlockInBuffer(rr)
    # 关系S的哈希文件
    for i in range(32):
        rs = int(buffer.readBlockFromDisk('s' + str(i)))
        for j in range(7):
            c = int(buffer.data[rs][2 * j])
            if c % divisor in ds.keys():
                ds[c % divisor].append((i, j))
            else:
                ds[c % divisor] = []
                ds[c % divisor].append((i, j))
        buffer.freeBlockInBuffer(rs)
    # 桶内排序
    for k in range(divisor):
        if k in dr.keys():
            dr[k] = sorted(dr[k])
        if k in ds.keys():
            ds[k] = sorted(ds[k])
    # 哈希连接
    count = 0
    num = 0
    hjoin = buffer.getNewBlockInBuffer()
    hjlist = []
    for k in range(divisor):
        for i in range(8):
            buffer.freeBlockInBuffer(i)
        if k not in dr.keys() or k not in ds.keys():
            continue
        rlist = dr[k]
        slist = ds[k]
        for i in rlist:
            rir = buffer.readBlockFromDisk('r' + str(i[0]))
            a = buffer.data[rir][2 * i[1]]
            b = buffer.data[rir][2 * i[1] + 1]
            for j in slist:
                rjs = buffer.readBlockFromDisk('s' + str(j[0]))
                c = buffer.data[rjs][2 * j[1]]
                d = buffer.data[rjs][2 * j[1] + 1]
                if a == c:
                    hjlist.append(a)
                    hjlist.append(b)
                    hjlist.append(d)
                buffer.freeBlockInBuffer(rjs)
            buffer.freeBlockInBuffer(rir)
    for item in range(0, len(hjlist), 3):
        if count % 7 == 0 and count != 0:
            buffer.writeBlockToDisk('testHJ' + str(count // 7 - 1), hjoin)
            buffer.freeBlockInBuffer(hjoin)
            hjoin = buffer.getNewBlockInBuffer()
            num = num + 1
        buffer.data[hjoin].append(hjlist[item])
        buffer.data[hjoin].append(hjlist[item + 1])
        buffer.data[hjoin].append(hjlist[item + 2])
        count = count + 1
    # 同时处理最后一次写入文件或者不满7个元组的文件
    if 7 * num < count:
        buffer.writeBlockToDisk('testHJ' + str(num), hjoin)
        buffer.freeBlockInBuffer(hjoin)
    
def blocksort(buffer, relation, bias):
    '''
    对关系relation的块以一定数量分组进行排序(关系R采用6块一组, 关系S采用1块一组)
    :param buffer: 缓冲区
    :param relation: 关系
    :param bias: 文件号偏移
    :return: 对一定数量的块归并排序(最小单位采用选择排序)后的结果
    '''
    assert relation in ('R', 'S')
    # 关系R
    if relation == 'R':
        relation = 'r'
        groupc = []
        for i in range(2):
            r1 = buffer.readBlockFromDisk(relation + str(bias + 2 * i))
            r2 = buffer.readBlockFromDisk(relation + str(bias + 2 * i + 1))
            groupa = [int(a) for a in buffer.data[r1][0:14]]
            groupb = [int(b) for b in buffer.data[r2][0:14]]
            groupa = selfsort(groupa)
            groupb = selfsort(groupb)
            groupc.append(groupsort4(groupa, groupb))
            buffer.freeBlockInBuffer(r1)
            buffer.freeBlockInBuffer(r2)
        groupd = groupc[1]
        groupc = groupc[0]
        groupc = groupsort4(groupc, groupd)
        del groupd
        # 排序块12, 13, 14, 15
        if bias == 12:
            return groupc
        r3 = buffer.readBlockFromDisk(relation + str(bias + 4))
        r4 = buffer.readBlockFromDisk(relation + str(bias + 5))
        groupe = selfsort([int(a) for a in buffer.data[r3][0:14]])
        groupf = selfsort([int(b) for b in buffer.data[r4][0:14]])
        buffer.freeBlockInBuffer(r3)
        buffer.freeBlockInBuffer(r4)
        groupd = groupsort4(groupe, groupf)
        # 尽量模拟缓冲区
        del groupe
        del groupf
        groupc = groupsort4(groupc, groupd)
        del groupd
        return groupc
    # 关系S
    else:
        relation = 's'
        # 选择排序返回有序的关系S文件块
        s1 = buffer.readBlockFromDisk(relation + str(bias))
        groupc = [int(c) for c in buffer.data[s1][0:14]]
        buffer.freeBlockInBuffer(s1)
        groupc = selfsort(groupc)
        return groupc
    
def groupsort4(groupa, groupb):
    '''
    对块groupa和groupb进行归并排序, 要求二者已然有序
    :param groupa: 归并排序的元素
    :param groupb: 归并排序的元素
    :return: 归并排序后的整体块
    '''
    result = []
    i, j = 0, 0
    while i < len(groupa) and j < len(groupb):
        if groupa[i] <= groupb[j]:
            result.append(groupa[i])
            result.append(groupa[i + 1])
            i = i + 2
        else:
            result.append(groupb[j])
            result.append(groupb[j + 1])
            j = j + 2
    while i < len(groupa):
        result.append(groupa[i])
        result.append(groupa[i + 1])
        i = i + 2
    while j < len(groupb):
        result.append(groupb[j])
        result.append(groupb[j + 1])
        j = j + 2
    return result
    
def selfsort(blk):
    '''
    对块blk内部数据进行选择排序
    :param blk: 块数据
    :return: 排序后的数据
    '''
    for i in range(0, len(blk) - 2, 2):
        for j in range(i, len(blk), 2):
            if blk[i] > blk[j]:
                tempa = blk[i]
                tempb = blk[i + 1]
                blk[i] = blk[j]
                blk[i + 1] = blk[j + 1]
                blk[j] = tempa
                blk[j + 1] = tempb
    return blk
    
if __name__ == '__main__':
    # 缓冲区初始化
    buffer = extmem.TagBuffer(520, 64)
    '''
    # 构造数据
    R, S = handle.createRS()
    handle.WriteRtoDisk(buffer, R)
    handle.WriteStoDisk(buffer, S)
    print('==========Origin==========')
    handle.printRS(buffer)
    print('==========Origin==========\n')
    
    # 查询
    print('==========Select==========')
    testSelect(buffer, 40, 60)
    print('==========Select==========\n')
    
    # 投影
    print('==========Shadow==========')
    testShadow(buffer, 'R', 'A')
    print('==========Shadow==========\n')
    
    # 循环嵌套连接
    print('==========NLJ==========')
    testNLJ(buffer)
    print('==========NLJ==========\n')
    
    # 排序归并连接
    print('==========SMJ==========')
    testSMJ(buffer)
    print('==========SMJ==========\n')
    
    # 哈希连接
    print('==========HJ==========')
    testHJ(buffer)
    print('==========HJ==========\n')
    '''
    # 释放缓冲区
    buffer.freeBuffer()
