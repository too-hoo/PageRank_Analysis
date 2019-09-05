# -*- coding:utf-8 -*-
# 用PageRank挖掘希拉里邮件中的重要人物关系
import pandas as pd
import networkx as nx
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

# 写博客：消除警告（版本问题）
# A collection of utility functions and classes. 
# Originally, many (but not all) were from the Python Cookbook -- hence the name cbook.
# import warnings
# import matplotlib.cbook  
# warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

# 数据加载
emails = pd.read_csv("./input/Emails.csv")
# 读取别名文件
file = pd.read_csv("./input/Aliases.csv")
aliases = {}
for index, row in file.iterrows():
    aliases[row['Alias']] = row['PersonId']
# 读取人名文件
file = pd.read_csv("./input/Persons.csv")
persons = {}
for index, row in file.iterrows():
    persons[row['Id']] = row['Name']
# 针对别名进行转换
def unify_name(name):
    # 姓名统一小写
    name = str(name).lower()
    # 去掉,和 @后面的内容
    name = name.replace(",","").split("@")[0]
    # 别名转换
    if name in aliases.keys():
        return persons[aliases[name]]
    return name
# 画出网络图
def show_graph(graph, layout='spring_layout'):
    # 使用Spring Layout 布局，类似中心放射状
    if layout == 'circular_layout':
        positions=nx.circular_layout(graph)
    else:
        positions=nx.spring_layout(graph)
    # 设置网络图中的结点大小，大小与PageRank值相关，因为PageRank值很小所以需要*20000
    nodesize = [x['pagerank']*20000 for v,x in graph.nodes(data=True)]
    # 设置网络图中的边长度
    edgesize = [np.sqrt(e[2]['weight']) for e in graph.edges(data=True)]
    # 绘制节点
    nx.draw_networkx_nodes(graph, positions, node_size = nodesize, alpha=0.4)
    # 绘制边
    nx.draw_networkx_edges(graph, positions, edge_size = edgesize, alpha=0.2)
    # 绘制节点的label
    nx.draw_networkx_labels(graph, positions, font_size=10)
    # 输出希拉里邮件中的所有的人物的关系图
    plt.show()
# 将寄件人与收件人的姓名进行规范化
emails.MetadataFrom = emails.MetadataFrom.apply(unify_name)
emails.MetadataTo = emails.MetadataTo.apply(unify_name)
# 设置边的权重等于发邮件的次数（计算边的权值）
edges_weights_temp = defaultdict(list)
# 遍历从数据集中查询的对应的值，如果不存在边就赋值为1，否则就累加1
for row in zip(emails.MetadataFrom, emails.MetadataTo, emails.RawText):
    temp = (row[0], row[1])
    if temp not in edges_weights_temp:
        # 没有时就创建一个赋值为1，代表通信1次
        edges_weights_temp[temp] = 1
    else:
        # 如果存在就找出当时的次数再加 1
        edges_weights_temp[temp] = edges_weights_temp[temp] + 1
# print(edges_weights_temp)
# 转化格式(from, to), weight => from, to, weight
# 这个是一个三元数组edges_weights
edges_weights = [(key[0], key[1], val) for key, val in edges_weights_temp.items()]
# 创建一个有向图
graph = nx.DiGraph()
# 设置有向图中的路径以及权重(from, to, weight)，add_weighted_edges_from接收的是一个三元数组
graph.add_weighted_edges_from(edges_weights)
# 计算每个节点（人）的PR值，并作为结点的Pagerank属性
pagerank = nx.pagerank(graph)
# 将 pagerank 数值作为结点的属性
nx.set_node_attributes(graph, name = 'pagerank', values=pagerank)
# 画网络图
show_graph(graph)

# 将完整的图谱进行精简
# 设置PR的值的阈值，筛选大于阈值的重要核心结点
pagerank_threshold = 0.005
# 复制一份计算好的网络图
small_graph = graph.copy()
# 剪掉PR值小于pagerank_threshold的结点
for n, p_rank in graph.nodes(data=True):
    if p_rank['pagerank'] < pagerank_threshold:
        small_graph.remove_node(n)
# 画出网络图，采用的是circular_layout布局让筛选出来的点组成一个圆
show_graph(small_graph, 'circular_layout')