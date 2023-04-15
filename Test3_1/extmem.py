'''
复刻extmem.c和extmem.h文件
'''
import os

class TagBuffer:
    def __init__(self, bufsize, blksize):
        '''
        初始化TagBuffer
        :param bufsize: 缓冲区大小
        :param blksize: 块大小
        '''
        # I/O次数
        self.numIO = 0
        # 缓冲区大小
        self.bufSize = bufsize 
        # 块大小
        self.blkSize = blksize
        # 缓冲区块总数
        self.numAllBlk = bufsize // (blksize + 1)
        # 缓冲区空余块数
        self.numFreeBlk = self.numAllBlk
        # 缓冲区已有块数
        self.blkcount = 0
        # 数据
        self.data = []
        # 块可获得标记
        self.used = []
        # 初始化缓冲区的每一块
        for i in range(self.numAllBlk):
            self.data.append([])
            self.used.append(False)

    def freeBuffer(self):
        '''
        释放缓冲区
        '''
        self.data = []
        self.used = []
        for i in range(self.numAllBlk):
            self.data.append([])
            self.used.append(False)
        self.countFreeBlk()

    def getNewBlockInBuffer(self):
        '''
        从缓冲区申请一个新的块
        :return: 申请成功返回块编号; 否则返回False
        '''
        if (self.numFreeBlk == 0):
            print('No free Block!')
            return False
        for i in range(8):
            if self.used[i] == False:
                self.used[i] = True
                self.countFreeBlk()
                return i

    def freeBlockInBuffer(self, free_num):
        '''
        :param free_num: 块编号
        释放缓冲区的块
        '''
        if self.used[free_num] == True:
            self.used[free_num] = False
            self.countFreeBlk()
        self.data[free_num] = []

    def readBlockFromDisk(self, addr):
        '''
        读取地址addr处到缓冲区
        :param addr: 磁盘块地址
        :return: 读取成功返回盘号; 否则返回False
        '''
        # 文件地址(磁盘块格式化的地址, 在blocks文件夹中)
        fnm = 'blocks/' + addr + '.blk'
        if self.numFreeBlk == 0:
            print('Buffer Overflows!')
            return False
        fop = open(fnm)
        if not fop:
            print('Reading Block Failed!')
            return False
        frd = fop.readline().split(' ')[:-1]
        fop.close()
        # 寻找未使用的块
        for i in range(self.numAllBlk):
            if self.used[i] == False:
                self.used[i] = True
                self.data[i] = frd
                self.countFreeBlk()
                self.numIO = self.numIO + 1
                return i

    def writeBlockToDisk(self, addr, blkto):
        '''
        将缓冲区内的块写入地址addr磁盘块
        :param addr: 磁盘块地址
        :param blkto: 写入块编号
        :return: 写入成功返回True; 否则返回False
        '''
        # 文件地址(磁盘块格式化的地址, 在blocks文件夹中)
        fnm = 'blocks/' + addr + '.blk'
        self.blkcount = self.blkcount + 1
        fop = open(fnm, 'w')
        if not fop:
            print('Reading Block Failed!')
            return False
        for i in self.data[blkto]:
            fop.write(str(i) + ' ')
        fop.write(str(self.blkcount) + ' ')
        fop.close()
        self.data[blkto] = []
        self.used[blkto] = False
        self.countFreeBlk()
        self.numIO = self.numIO + 1
        return True

    def countFreeBlk(self):
        '''
        更新可用缓冲区块数量
        '''
        count = 0
        for i in range(self.numAllBlk):
            if self.used[i] == False:
                count += 1
        self.numFreeBlk = count

def dropBlockOnDisk(addr):
    '''
    从磁盘上删除地址为addr的磁盘内容
    :param addr: 待删除磁盘地址
    :return: 删除成功返回True; 否则返回False
    '''
    fnm = "blocks/" + addr + ".blk"
    if not os.path.exists(fnm):
        return False
    os.remove(fnm)
    return True
