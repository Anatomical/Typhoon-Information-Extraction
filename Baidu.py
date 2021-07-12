'''
Author: your name
Date: 2021-07-12 19:21:35
LastEditTime: 2021-07-12 19:27:38
LastEditors: your name
Description: In User Settings Edit
FilePath: \EndGame\Baidu.py
'''

from dataStructure import CONLL
from aip import AipNlp

""" 你的 APPID AK SK """
# TODO:请在下面填上您百度云服务的APP_ID、API_KEY及SECRET_KEY
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


def parse(text):
    '''
    @description: 调用新版本X.2依存句法分析功能
    @param {text=待分析句子}
    @return {conll格式的依存句法树}
    '''
    """ 如果有可选参数 """
    options = {}
    options["mode"] = 0

    """ 带参数调用依存句法分析 """
    result=client.depParser(text, options)
    print('百度API调用完毕')
    conll=CONLL()
    conll.getBaidu(result)
    return conll
