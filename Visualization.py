'''
Author: your name
Date: 2021-07-12 19:21:35
LastEditTime: 2021-07-12 19:24:54
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \EndGame\Visualization.py
'''
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
from pyecharts import options as opts
from pyecharts.charts import Tree


def table(headers,rows,title='Table',subtitle=''):
    '''
    @description: 利用pyecharts展示表格
    @param {headers=表头,rows=数据,title=标题(默认为Table),subtitle=副标题(默认为无)}
    @return {table=pyecharts内置类型表格}
    '''
    table = Table()
    table.add(headers, rows)
    table.set_global_opts(
        title_opts=ComponentTitleOpts(title,subtitle)
    )
    return table

def tree(data,title='Tree'):
    '''
    @description: 利用pyecharts展示树
    @param {data=JSON树,title=标题(默认为Tree)}
    @return {tree=pyecharts内置类型树}
    '''
    '''
    data数据结构类似于
        data = [
        {
            "children": [
                {"name": "B"},
                {
                    "children": [{"children": [{"name": "I"}], "name": "E"}, {"name": "F"}],
                    "name": "C",
                },
                {
                    "children": [
                        {"children": [{"name": "J"}, {"name": "K"}], "name": "G"},
                        {"name": "H"},
                    ],
                    "name": "D",
                },
            ],
            "name": "A",
        }
        ]
    '''
    c = (
        Tree()
        .add("", data)
        .set_global_opts(title_opts=opts.TitleOpts(title))
    )
    return c

