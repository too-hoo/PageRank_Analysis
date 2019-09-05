# PageRank：分析希拉里邮件中的人物关系


## 总结

1、使用PageRank算法，可以通过矩阵乘法求得网页的权重，同时也可以使用Python的NetworkX得到相同的结果。

2、根据上面的实践结果可以将一张复杂的网络图，通过PR值的计算、筛选，最终得到一张精简的网络图。其中使用了Python的NetworkX工具，包括创建图、结点、边以及PR值的计算。

3、实际上掌握了PageRank的理论之后，在实战的时候往往就是一行代码的事情。但是项目与理论不同，项目中涉及的理论数据量比较大，需要会花费大量的时间在预处理过程中，比如上面的项目中，需要对别名进行了统一，对边的权重进行了计算，同时还需要把计算好的结果以可视化的方式呈现。

4、PageRank实战
- 数据集
    - 希拉里邮件数据集，513个人名，9306封邮件，人名存在别名的情况
    - 目标：计算不同的人在邮件数据集中的权重，筛选重要的人物，绘制网络图
- networkx使用
    - 图创建
        - 无向图：nx.Graph()
        - 有向图：nx.DiGraph()
    - 结点操作
        - 增加：G.add_node()和G.add_nodes_from()
        - 删除：remove_node()和remove_nodes_from()
        - 查询：nodes()得到所有的结点，number_of_nodes()得到节点的个数
    - 边操作
        - 增加：add_edge(),add_edges_from(),add_weighted_edges_from()
        - 删除：remove_edge()和remove_adges_from()
        - 查询：edges()访问图中所有的边，number_of_edges()得到边的个数
- 项目流程
    - 准备阶段：数据探索、数据清洗、特征选择
    - 挖掘阶段：PR值计算、PR值筛选、可视化
    - 掌握使用NetworkX计算PR值以及网络图的可视化

