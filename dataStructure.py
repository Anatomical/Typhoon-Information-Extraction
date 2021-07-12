'''
Author: your name
Date: 2021-07-12 19:21:35
LastEditTime: 2021-07-12 19:28:47
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \EndGame\dataStructure.py
'''

from Visualization import table,tree
import operator
'''
词与句子存储系列
    CONLL标注格式说明
    CONLL标注格式包含10列，分别为：
    —————————————————————————————————————————————————————————————————————————————
    ID   FORM    LEMMA   CPOSTAG POSTAG  FEATS   HEAD    DEPREL  PHEAD   PDEPREL
    —————————————————————————————————————————————————————————————————————————————

    只用到前８列，其含义分别为：

    1    ID      当前词在句子中的序号，１开始.
    2    FORM    当前词语或标点
    3    LEMMA   当前词语（或标点）的原型或词干，在中文中，此列与FORM相同
    4    CPOSTAG 当前词语的词性（粗粒度）
    5    POSTAG  当前词语的词性（细粒度）
    6    FEATS   句法特征，在本次评测中，此列未被使用，全部以下划线代替。
    7    HEAD    当前词语的中心词
    8    DEPREL  当前词语与中心词的依存关系

    在CONLL格式中，每个词语占一行，无值列用下划线'_'代替，列的分隔符为制表符'\t'，行的分隔符为换行符'\n'；句子与句子之间用空行分隔。
'''
class Word:
    '''
    CONLL的词数据结构
    '''
    def __init__(self,id,lemma,head,deprel,postag='',sqd='',ded='',score=''):
        '''
        @description: 初始化类
        @param {id=序号,lemma=词的文本,head=存储父节点,数据类型为Word,deprel=依存关系,postag=词性,\
            sqd=序列距离,ded=依存距离,score=最终得分}\n
            id,lemma,postag,head,deprel 为初始化时必须具有的参数\n
            ner,sqd,ded,scroe 为初始化时可选参数\n
        @return {None}
        '''
        self.ID=id
        self.LEMMA=lemma
        self.POSTAG=postag
        self.HEAD=head
        self.DEPREL=deprel
        self.SQD=sqd
        self.DED=ded
        self.SCORE=score

    def __str__(self):
        '''返回Word的描述信息'''
        return 'ID:{0}\tLEMMA:{1}\tPOSTAG:{2}\tHEAD:{3}\tDEPREL:{4}\tSQD:{5}\tDED:{6}\tSCORE:{7}'.\
            format(self.ID,self.LEMMA,self.POSTAG,self.HEAD,self.DEPREL,self.SQD,self.DED,self.SCORE)

class CONLL:
    '''
    CONLL数据结构
    '''
    def __init__(self):
        ''' 清空词列表 '''
        self.wordList=[]

    def getBaidu(self,parse):
        '''
        @description: 解析百度API的输出格式,并转化为conll
        @param {parse=百度api client.depParser的返回结果}
        @return {None}
        '''
        ''' 百度标识字典 '''
        Dependency_indicator=\
            {'SBV':'主谓关系','VOB':'动宾关系','POB':'介宾关系','ADV':'状中结构',\
            'CMP':'动补结构','ATT':'定中关系','F':'方位关系','COO':'并列关系','DBL':'兼语',\
            'DOB':'双宾语结构','VV':'连谓结构','IC':'子句结构','MT':'虚词成分','HED':'核心关系'}
        
        ''' 将每一个词转为Word类型存储 ''' 
        for item in parse['items']:
            word=Word(id=item['id'],lemma=item['word'],postag=item['postag'],head=item['head'],deprel=item['deprel'])
            self.wordList.append(word)

        ''' 修改HEAD属性,最后使得Word的HEAD属性存储其父节点的Word类型数据'''
        for i,child in enumerate(self.wordList):
            for parent in self.wordList:
                if child.HEAD!=0:
                    if child.HEAD==parent.ID:                       
                        self.wordList[i].HEAD=parent
                        break
                else:
                    self.wordList[i].HEAD=Word(id=0,deprel=None,head=None,postag='root',lemma='##核心##')
 
    def getHanLP(self,parse):
        '''
        @description: 解析HanLP的输出格式,并转化为conll
        @param {parse= HanLP.parseDependency的返回结果}
        @return {None}
        '''
        ''' 将每一个词转为Word类型存储 '''
        for word in parse.iterator():  # 通过dir()可以查看sentence的方法
            word=Word(id=word.ID,lemma=word.LEMMA,deprel=word.DEPREL,postag=word.POSTAG,head=word.HEAD.ID)
            self.wordList.append(word)
        ''' 修改HEAD属性,最后使得Word的HEAD属性存储其父节点的Word类型数据'''
        for i,child in enumerate(self.wordList):
            for parent in self.wordList:
                if child.HEAD!=0:
                    if child.HEAD==parent.ID:                       
                        self.wordList[i].HEAD=parent
                        break
                else:
                    self.wordList[i].HEAD=Word(id=0,deprel=None,head=None,postag='root',lemma='##核心##')     
        
                    
    def getTencent(self,parse):
        '''
        # !!!腾讯的依存句法分析功能缺少词性字段,故本程序暂不实用腾讯自然语言出力API
        @description: 解析腾讯的输出格式,并转化为conll
        @param {parse=腾讯api client.DependencyParsing的返回结果}
        @return {None}
        '''
        
        ''' 将每一个词转为Word类型存储 '''
        for item in parse.DpTokens:
            word=Word(id=item.Id,lemma=item.Word,head=item.HeadId,deprel=item.Relation)
            self.wordList.append(word)
        
        # todo 补充POSTAG
        # for item in segment.PosTokens:
        #     self.wordList[item.BeginOffset].POSTAG=item.Pos
        
        # todo 补充NER
        # NERDict={'PER':'人名','LOC':'地名','ORG':'机构团体名','PRODUCTION':'产品名'}
        # for item in segment.NerTokens:
        #     self.wordList[item.BeginOffset].NER=NERDict[item.Type]

        ''' 修改HEAD属性,最后使得Word的HEAD属性存储其父节点的Word类型数据 '''
        for i,child in enumerate(self.wordList):
            for parent in self.wordList:
                if child.HEAD!=0:
                    if child.HEAD==parent.ID:                       
                        self.wordList[i].HEAD=parent
                        break
                else:
                    self.wordList[i].HEAD=Word(id=0,deprel=None,head=None,postag='root',lemma='##核心##')
        
    def getText(self):
        '''
        @description: 从conll中获取整个句子
        @param {None}
        @return {text=句子}
        '''
        text=''
        for item in self.wordList:
            text=text+item.LEMMA
        return text        
        
    def showTable(self):
        '''
        @description: 对conll属性以表格的形式进行可视化展示
        @param {None}
        @return {table=表格}
        '''
        ''' 表头 '''
        headers = ["ID", "LEMMA", "POSTAG", "HEAD","DEPREL","SQD","DED","SCORE"]
        ''' 字段 '''
        rows=[]
        for item in self.wordList:
            rows.append([item.ID,item.LEMMA,item.POSTAG,item.HEAD.ID,item.DEPREL,\
                item.SQD,item.DED,item.SCORE])
        ''' 副标题 '''
        # text=self.getText()
        
        return table(title='分析结果',headers=headers,rows=rows)
    
    def showTree(self):
        '''
        @description: 对conll存储的依存句法树以树的形式进行可视化展示
        @param {None}
        @return {tree=树}
        '''
        ''' JSON树 '''
        mytree=CONLL2Tree(self)
        myjson=[]
        Tree2JSON(myjson,mytree)
        return tree(myjson,title='依存句法树')
        
    def __str__(self):
        """返回conll的描述信息"""
        title='ID\t\tLEMMA\t\tPOSTAG\t\tHEAD\t\tDEPREL\t\tSQD\t\tDED\t\tSCORE\n'
        splitLine=120*'—'+'\n'
        result=splitLine+title+splitLine
        for item in self.wordList:
            result=result+str(item.ID)+'\t\t'+item.LEMMA+'\t\t'+item.POSTAG+\
                '\t\t'+str(item.HEAD.ID)+'\t\t'+item.DEPREL+'\t\t'+str(item.SQD)+\
                    '\t\t'+str(item.DED)+'\t\t'+str(format(item.SCORE,'.1f'))+'\n'
        result=result+splitLine
        return result[:-2]

'''
关系存储系列
'''
class SPO:
    ''' 三元组存储 '''
    def __init__(self,S='',P='',O=''):
        '''
        @description: 初始化三元组
        @param {S=主体,P=动作,O=客体}
            参数S和O为选填,即允许三元组中S与O的缺失\n
            #! 特别注意,参数P必填,不可缺失
        @return {*}
        '''
        self.S=S
        self.P=P
        self.O=O
    
    def __str__(self):
        return '('+self.S+','+self.P+','+self.O+')'
 
'''
栈数据结构系列
'''
class Stack:
    '''栈数据结构'''
    def __init__(self):
        '''初始化栈'''
        self.items=[]

    def isEmpty(self):
        '''
        @description: 是否栈空
        @param {None}
        @return {bool=True or False}
        '''
        return self.items==[]

    def push(self,item):
        '''
        @description: 入栈
        @param {item=待入栈的元素}
        @return {None}
        '''
        self.items.append(item)
    
    def pop(self):
        '''
        @description: 出栈
        @param {item=待出栈的元素}
        @return {item=出栈元素}
        '''
        return self.items.pop()

    def getTop(self):
        '''
        @description: 获取栈顶元素
        @param {None}
        @return {item=栈顶元素}
        '''
        return self.items[-1]

'''
树数据结构系列
'''   
def createTree(myTree,wordList):
    '''
    @description: 根据词列表递归生生成树
    @param {myTree=树,wordList=词列表}
    @return {None}
    '''
    root=myTree[0]
    for word in wordList:
        if(word.HEAD.ID==root.ID):
            child=[word]
            myTree.append(child)
    
    if(len(myTree)>1):
        for child in myTree[1:]:
            createTree(child,wordList)
    else:
        return

def getPath(conll,node):
    '''
    @description: 求依存树conll中某节点到根节点的最短路径
    @param {conll=conll类型数据,node=目标结点}
    @return {path=存储树中每个结点到目标结点的最短路径}
    '''
    path=[]
    for word in conll.wordList:
        if word.ID==node.ID:
            ''' 在词列表里找到这个结点 '''
            path.append(word)
            while(word.HEAD is not None):
                ''' 从这个结点一直追溯到树根,并记录下经过的每个结点'''
                path.append(word)
                word=word.HEAD
            break
    return path

''' 树的遍历 以及遍历过程中的操作'''
def visitNodeLEMMA(T,*args):
    '''
    @description: 打印结点存储的LEMMA,*args用于吸收多的参数
    @param {*}
    @return {*}
    '''
    print(T[0].LEMMA)

def findChild(T,*args):
    word=args[0]
    childTree=args[1]
    if T[0].ID==word.ID:
        childTree.append(T)

def saveChildWORD(T,*args):
    nodelist=args[0]
    nodelist.append(T[0])

def PreOrder(T,fun,*args):
    '''
    @description: 非递归先序遍历普通树
    @param {T=tree}
    @return {None}
    '''
    
    ''' 单独处理只有一个结点的树和空树 '''
    # ? 一般是只把空树单独拿出来进行考虑,这里可以考虑改进算法,减少代码行数
    if len(T)==1:
        ''' 如果是只有一个结点 '''
        # print(T[0].LEMMA)
        fun(T,*args)
        return
    elif len(T)==0:
        ''' 如果是空树 '''
        return
    else:
        pass
        
    '''
    Sp=孩子栈
    Si=索引栈
    Sr=父亲栈
    '''
    Sp=Stack()
    Si=Stack()
    Sr=Stack()
    p=T
    i=1
    while(True):
        if(len(p)>1 and i<len(p)):
            ''' 如果这个结点有孩子并且还有没有访问过的兄弟，那么孩子栈、索引栈和父亲栈均入栈,并重置索引 '''
            # print(p[0].LEMMA)
            fun(p,*args)
            Sr.push(p)
            Sp.push(p)
            p=p[i]
            Si.push(i)
            i=1
        else:
            ''' 如果没有孩子或者兄弟都已经访问过 '''
            if(Sr.getTop()==p):
                ''' 如果当前结点为子树的根,此子树已完成遍历,出栈 '''
                Sr.pop()
            else:
                ''' 如果当前结点不是子树的根,此子树为完成遍历,继续进行访问'''
                # print(p[0].LEMMA)
                fun(p,*args)
            if(Sp.isEmpty()==True):
                ''' 如果孩子栈空,则结束循环'''
                break
            
            ''' 孩子栈出栈,索引栈出栈,并且索引指向下一个孩子 '''           
            p=Sp.pop()
            i=Si.pop()
            i=i+1
        
            if(i<len(p)):
                ''' 如果该结点p还有没访问过孩子,则结点p再次入栈,索引栈入栈,并重置索引 '''
                Sp.push(p)
                p=p[i]
                Si.push(i)
                i=1

'''
数据结构转换系列
'''
def CONLL2Tree(conll):
    '''
    @description: CONLL转(列表)树结构
    @param {conll=conll数据结构}
    @return {tree=(列表)树数据结构}
    '''
    root=None
    ''' 找到树根 '''
    for word in conll.wordList:
        if(word.HEAD.ID==0):
            root=word
            break
    tree=[root]
    createTree(tree,conll.wordList)
    return tree

def Tree2JSON(myjson,tree):
    '''
    @description: (列表)树转JSON树<--递归
    @param {myjson=JSON树(空列表),tree=(列表)树}
    @return {None}
    '''
    nodeText=tree[0].LEMMA+'/'+tree[0].POSTAG
    myjson.append({'name':nodeText})
    if len(tree)>1:
        myjson[-1]['children']=[]
        for node in tree[1:]:
            Tree2JSON(myjson[-1]['children'],node)
    else:
        return
            
def Tree2Sentence(tree):
    nodelist=[]
    ''' 进行遍历,获取这棵树的所有结点 '''
    PreOrder(tree,saveChildWORD,nodelist)
    ''' 聚合句子 '''
    cmpfun = operator.attrgetter('ID')
    nodelist.sort(key=cmpfun)
    sentence=''
    for word in nodelist:
        sentence=sentence+word.LEMMA
    return sentence
    
