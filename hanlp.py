'''
Author: your name
Date: 2021-07-12 19:21:35
LastEditTime: 2021-07-12 19:29:15
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \EndGame\hanlp.py
'''

from dataStructure import CONLL
from pyhanlp import *

def parse(text):
    '''
    @description: 调用pyhanlp 1.X版本依存句法分析功能
    @param {text=待分析句子}
    @return {conll格式的依存句法树}
    '''
    sentence = HanLP.parseDependency(text)
    print('pyhanlp 1.X调用完毕')
    conll=CONLL()
    conll.getHanLP(sentence)
    return conll