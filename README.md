# 面向台风灾害的信息抽取

## 项目目的

实现基于文本的台风灾害信息自动化抽取

## 测试数据

data_mini.xlsx

## 模块说明

### Baidu.py

 Baidu包用于调用百度的自然语言处理API，需要使用者完善百度云服务的APP_ID、API_KEY及SECRET_KEY

### dataStructure.py

dataStructure包主要用于管理数据结构

### Extraction.py

Extraction包用于关系抽取的一系列操作

### hanlp.py

调用hanlp 1.X版本的自然语言处理基本功能

### IO.py

 文件读取与预处理

### Tencent.py

 Tencent包用于腾讯自然语言处理API的调用

### Visualization.py

Visualization包基于pyecharts来提供可视化功能

## 可运行程序

### batch_operation.ipynb

针对data_mini.xlsx数据进行批量信息抽取

### demo.ipynb

用于对单个句子的测试，提供了友好的可视化图形