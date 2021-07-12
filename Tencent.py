'''
Author: your name
Date: 2021-07-12 19:21:35
LastEditTime: 2021-07-12 19:31:03
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \EndGame\Tencent.py
'''

from dataStructure import CONLL
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.nlp.v20190408 import nlp_client, models
# TODO:请在下面填上您腾讯服务的SecretId、SecretKey
SecretId=""
SecretKey=""

def segment(text):
    '''
    @description: 腾讯自然语言处理 词法分析API
    @param {text=待分析句子}
    @return {resp=词法分析结果}
    '''
    try: 
        cred = credential.Credential(SecretId, SecretKey) 
        httpProfile = HttpProfile()
        httpProfile.endpoint = "nlp.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile) 

        req = models.LexicalAnalysisRequest()
        params = {
            "Text": text
        }
        req.from_json_string(json.dumps(params))

        resp = client.LexicalAnalysis(req) 
        # print(resp.to_json_string()) 
        return resp

    except TencentCloudSDKException as err: 
        print(err) 


def IncompleteParse(text):
    '''
    @description: 腾讯自然语言处理 依存句法分析APII(不包含词法分析)
    @param {text=待分析句子}
    @return {resp=句法分析结果}
    '''
    try: 
        cred = credential.Credential(SecretId, SecretKey) 
        httpProfile = HttpProfile()
        httpProfile.endpoint = "nlp.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile) 

        req = models.DependencyParsingRequest()
        params = {
            "Text": text
        }
        req.from_json_string(json.dumps(params))

        resp = client.DependencyParsing(req) 
        # print(resp.to_json_string()) 
        return resp

    except TencentCloudSDKException as err: 
        print(err)


def parse(text):
    '''
    @description: 结合词法分析和句法分析结果得到带有词法分析结果的依存树
    @param {text=待分析句子}
    @return {conll=conll类型数据结构}
    '''
    # ! 词法分析与依存句法分析两个功能的分析粒度不一致,无法进行整合
    # seg=segment(text)
    par=IncompleteParse(text)
    print('腾讯API调用完毕')
    conll=CONLL()
    conll.getTencent(par)
    return conll