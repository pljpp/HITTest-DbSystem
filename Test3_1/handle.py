'''
对关系R和关系S的基本处理
'''
import random
import relation

def randomR():
    r = relation.R(random.randint(1, 40), random.randint(1, 1000))
    return r

def randomS():
    s = relation.S(random.randint(20, 60), random.randint(1, 1000))
    return s

def createRS():
    '''
    构造满足数量的R,S关系(禁止全重复元组)
    :return: R, S
    '''
    R = []
    S = []
    # R有112个元组
    for i in range(112):
        tempR = randomR()
        # 剔除重复元组
        while tempR in R:
            tempR = randomR()
        R.append(tempR)
    # S有224个元组
    for i in range(224):
        tempS = randomS()
        # 剔除重复元组
        while tempS in S:
            tempS = randomS()
        S.append(tempS)
    return R, S

def WriteRtoDisk(buffer, R):
    '''
    将缓冲区的关系R写入磁盘
    :param buffer: 缓冲区
    :param R: 关系R
    '''
    cnt = 0
    # R所需块的数量(上限16个)
    blknum = 0
    toR = []
    for r in R:
        toR.append(r.A)
        toR.append(r.B)
        cnt = cnt + 1
        if cnt % 7 == 0:
            toR.append(0)
            # 不满15继续存储
            if blknum != 15:
                toR.append(blknum + 1)
            # 满15覆盖
            else:
                toR.append(0)
            # 写入缓冲区0
            buffer.data[0].extend(toR)
            buffer.writeBlockToDisk('r' + str(blknum), 0)
            blknum = blknum + 1
            toR = []
            buffer.freeBlockInBuffer(0)

def WriteStoDisk(buffer, S):
    '''
    将缓冲区的关系S写入磁盘
    :param buffer: 缓冲区
    :param S: 关系S
    '''
    cnt = 0
    blknum = 0
    toS = []
    for s in S:
        toS.append(s.C)
        toS.append(s.D)
        cnt = cnt + 1
        if cnt % 7 == 0:
            toS.append(0)
            if blknum != 15:
                toS.append(blknum + 1)
            else:
                toS.append(0)
            buffer.data[0].extend(toS)
            buffer.writeBlockToDisk('s' + str(blknum), 0)
            blknum = blknum + 1
            toS = []
            buffer.freeBlockInBuffer(0)

def printRS(buffer):
    '''
    打印RS关系
    :param buffer: 缓冲区
    '''
    for i in range(16):
        addr = 'r' + str(i)
        n = buffer.readBlockFromDisk(addr)
        for j in range(7):
            a = buffer.data[n][2 * j]
            b = buffer.data[n][2 * j + 1]
            print('R: ', a, b)
        buffer.freeBlockInBuffer(n)
    for i in range(32):
        addr = 's' + str(i)
        n = buffer.readBlockFromDisk(addr)
        for j in range(7):
            c = buffer.data[n][2 * j]
            d = buffer.data[n][2 * j + 1]
            print('S: ', c, d)
        buffer.freeBlockInBuffer(n)
