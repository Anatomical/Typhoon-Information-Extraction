'''
Author: your name
Date: 2021-07-12 19:21:35
LastEditTime: 2021-07-12 19:29:44
LastEditors: your name
Description: In User Settings Edit
FilePath: \EndGame\IO.py
'''


import os
import re

class FileReader:
    ''' 文件读取器 '''
    # !目前禁止使用！！！禁止使用！！！
    # todo 后期需要增加表格类型数据的读取
    # ? 文本预处理方案设计
    
    def __init__(self) -> None:
        self.txtDict={}

    def readFolder(self,folderPath):
        rootdir=os.path.join(folderPath)
        for (dirpath,dirnames,filenames) in os.walk(rootdir):
            for filename in filenames:
                if os.path.splitext(filename)[1]=='.txt':
                    year=os.path.splitext(filename)[0]
                    with open(folderPath+'\\'+filename, "r",encoding='utf-8') as f:
                        data = f.read()  # 读取文件
                        #   删除括号中的内容
                        self.txtDict[year]=data.replace('\n', '').replace('\r', '')
                        self.txtDict[year]=self.txtDict[year].replace('全市','深圳市').replace('我市','深圳市')\
                            .replace('我省','广东省').replace('今年',str(year)+'年').replace('ºC','°C').replace('－','-')
                        self.txtDict[year]=re.sub(u"\\（.*?）|\\- .*? -|\\{.*?}|\\[.*?]|\\【.*?】", "",\
                                     self.txtDict[year].encode('utf-8').decode())
                        self.txtDict[year]=self.txtDict[year].replace(' ', '')
                        #删除回车符、换行符、空格（不去掉空格的话会影响NLP任务）

        # 为了实现初步的指代消解与长句还原，这一步后需要修改在其他模块中进行
        for key in self.txtDict.keys():
            self.txtDict[key]=re.split('[。，；,]',self.txtDict[key])#删除空元素
            while '' in self.txtDict[key]:
                self.txtDict[key].remove('')
    
    def show(self):
        for k,v in self.txtDict.items():
            print("<---{0}年灾害公报--->".format(k))
            for i in range(len(v)):
                print("【{0}】：{1}".format(i+1,v[i]))