'''
Author: your name
Date: 2021-07-12 19:21:35
LastEditTime: 2021-07-12 19:28:58
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \EndGame\Extraction.py
'''

from dataStructure import CONLL2Tree, PreOrder, SPO, Tree2Sentence, findChild, getPath
import Baidu
import Tencent
import hanlp

def SequenceDistance(conll,trigger):
    '''
    @description: 求句法依存树的序列距离
    @param {conll=conll类型数据,trigger=触发词(Word类型数据)}
    @return {None}
    '''
    for word in conll.wordList:
        word.SQD=abs(word.ID-trigger.ID)
    
def DependencyDistance(conll,trigger):
    '''
    @description: 求句法依存树的依存距离
    @param {conll=conll类型数据,trigger=触发词(Word类型数据)}
    @return {None}
    '''
    ''' 最低公共祖先lca '''
    lca=None
    triggerPath=getPath(conll,trigger)
    for i,word in enumerate(conll.wordList):
        if word.ID==trigger.ID:
            ''' 触发词本身的依存距离直接就是0 '''
            conll.wordList[i].DED=0
        else:
            ''' 求其他词的依存距离 '''
            wordPath=getPath(conll,word)
            ''' 找句法依存树中两个词的最低公共祖先 '''
            for ii in wordPath:
                for jj in triggerPath:
                    if(ii.ID==jj.ID):
                        lca=ii
                if lca is not None:
                    break
                
            lcaPath=getPath(conll,lca)
            # 两个结点的距离计算公式
            conll.wordList[i].DED=len(triggerPath)+len(wordPath)-2*len(lcaPath)
      
def getScore(conll,a,b):
    '''
    @description: 根据序列距离与依存距离来求评估值score
    @param {conll=conll类型数据,a=序列距离的系数,b=依存距离的系数}
    @return {*}
    '''
    for i,word in enumerate(conll.wordList):
        score=round(a*word.SQD+b*word.DED,2)
        conll.wordList[i].SCORE=score

def bubbleSort_BY_score(wordList):
    '''
    @description: # 根据评估值scroe对词列表wordList冒泡排序
    @param {wordList=词列表}
    @return {None}
    '''
    for i,iword in enumerate(wordList):
        for j,jword in enumerate(wordList[:-1]):
            if wordList[j].SCORE>wordList[j+1].SCORE:
                wordList[j+1],wordList[j]=wordList[j],wordList[j+1]

def isTarget(text,api='baidu'):
    '''
    @description: 是否是我想抽取的句子
    @param {text=待分析文本,api=默认API为Baidu}
    @return {如果是,则返回conll和句子中的触发词;如果不是,则返回None,[]}
    '''
    conll=None
    triggerTag=['带来','导致','触发','造成','引起','引发','影响']
    common=[val for val in triggerTag if val in text]
    if common:
        if api=='baidu':
            conll=Baidu.parse(text)
        elif api=='tencent':
            conll=Tencent.parse(text)
        elif api=='hanlp':
            conll=hanlp.parse(text)
        else:
            pass
    return conll,common
    
def getCause_Effect(conll,common,a=0.1,b=1):
    '''
    @description: 抽取表示因果关系的三元组
    @param {conll=conll类型数据,common=句子中包含的触发词}
    @return {*}
    '''
    if common:
        result=[]
        entityTag=['n','nz','vn','an','nr']
        for word in conll.wordList:
            if word.LEMMA in common:
                S,P,O='','',''
                P=word.LEMMA
                SequenceDistance(conll,word)
                DependencyDistance(conll,word)
                getScore(conll,a,b)
                ''' 截取触发词之前的词 '''
                preList=conll.wordList[:word.ID-conll.wordList[-1].ID-1]
                ''' 截取触发词之后的词 '''
                postList=conll.wordList[word.ID:]
                ''' 根据评估值冒泡排序，加以词性限制，获取触发词对应的实体对 '''
                
                # todo 这边暂时考虑一对一的模式，后序再考虑一对多，多对多
                
                ''' 寻找触发词前面的实体 '''
                bubbleSort_BY_score(preList)
                for word in preList:
                    if word.POSTAG in entityTag:
                        S=word
                        break
                    
                ''' 寻找触发词后面的实体 '''
                bubbleSort_BY_score(postList)
                for word in postList:
                    if word.POSTAG in entityTag:
                        O=word
                        break
                    
                # todo 扩充实体内容 比如：天气-->高温天气，山竹-->超强台风“山竹”
                tree=CONLL2Tree(conll)
                if S:
                    S=expandEntity(tree,S)
                if O:
                    O=expandEntity(tree,O)
                
                # todo 触发词和实体1、实体2的位置不一定是像“实体1—触发词-实体2”,后期需要对不同的模式进行归纳
                # *先假设目前的三元组都是“实体1—触发词-实体2”模式
                # *根据“和”、“、”等并列关系来从一句话中分解出多个并列关系
                O=O.replace("、","和")
                O=O.split("和")
                for o in O:
                    spo=SPO(S,P,o)
                    print(spo)
                    result.append(spo)
        return result
    else:
        print("不包含触发词！")
    
    return None

def expandEntity(tree,entity):
    ''' 先从整棵树中找到实体为根的那棵子树 '''
    childTree=[]
    PreOrder(tree,findChild,entity,childTree)
    
    ''' 然后聚合这棵子树下面的结点变为一个完整的句子 '''
    sentence=Tree2Sentence(childTree[0])
    
    ''' 返回句子 '''
    return sentence
    
