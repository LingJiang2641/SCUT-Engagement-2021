import heapq
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict


class getGraph:
	"""将edges从文本文件转换为邻接表.
	...

	Parameters
	----------
	edge_file : string
		存储网络图的edges的文件路径.

	
	Methods
	-------
	get_connections()
		从 edge_file 中读取边并将其保存在邻接列表中（内存）.

	"""

	def __init__(self, edge_file):
		self.edge_file = edge_file

	def get_connections(self):
		"""从 edge_file 中读取边并将其保存在邻接列表中（内存）.

		Parameters
		----------
		None

		
		Returns
		-------
		edges : collections.defaltdict(list)
			包含网络图中连接信息的邻接表.

		"""

		edge_list = []
		edges = defaultdict(list)
		cash=defaultdict(list)
		defaultnodes=defaultdict(list)

		with open (self.edge_file, 'r') as e_file:
			edge_list = e_file.readlines()
		
		# for edge in edge_list:
		# 	from_, to_ = edge.split('\t')
		# 	from_, to_ = int(from_), int(to_[:-1])
		# 	edges[from_].append(to_)
		for edge in edge_list:
			from_, to_ ,amount,defaultnode= edge.split('\t')
			from_, to_,amount,defaultnode = int(from_), int(to_),int(amount),int(defaultnode[:-1])
			edges[from_].append(to_)
			cash[from_].append(amount)
			defaultnodes[from_].append(defaultnode)
		print(defaultnodes)
		
		return edges,defaultnodes,cash


class plotGraph:
	"""在屏幕上以图形方式绘制网络图.

	...

	Parameters
	----------
	edges : collections.defaltdict(list)
		包含网络图中连接信息的邻接表.
	
	interval : int, optional
		图形显示在屏幕上的时间（以毫秒为单位）
		Default value: 5000
	
	
	Methods
	-------
	get_KMaxRankNodes(number_of_nodes, rank_vector)
		计算并返回在 `rank_vector` 中具有最高值的 `number_of_nodes`.

	get_edgesConnectedToTopK(rank_vector, topK, ranks)
		计算并返回顶部 `k` 个节点的子节点列表.

	get_EdgesToDrawWithRanks(drawing_list, ranks)
		返回要在图形上显示的边列表和节点等级.

	draw(edge_list, nodes_to_draw)
		在屏幕上绘制节点大小等于节点等级的有向图.

	plot(number_of_nodes, rank_vector)
		调用函数，以适当的顺序调用其他函数来绘制图形.

	"""
	def __init__(self, edges, interval=5000):
		self.edges = edges
		self.interval = interval


	def get_KMaxRankNodes(self, number_of_nodes, rank_vector):
		"""计算并返回在 `rank_vector` 中具有最高值的 `number_of_nodes`.

		
		Parameters
		----------
		number_of_nodes : int
			包含要选取的节点数.

		rank_vector	: numpy.ndarray [1-dimensional, dtype=float]
			包含网络图中每个节点的 PageRank.

		
		Returns
		-------
		topK : list of tuple [(int, double), (int, double), ...]
			包含top的 `number_of_nodes` 的节点和排名.

		"""
		heaped_ranks = [(rank, node) for (node, rank) in 
			enumerate(rank_vector)]
		heapq._heapify_max(heaped_ranks)
		topK = [heapq._heappop_max(heaped_ranks)
			for _ in range(number_of_nodes)]

		return topK


	def get_edgesConnectedToTopK(self, rank_vector, topK, ranks):
		"""计算并返回顶部 `k` 个节点的子节点列表.


		Parameters
		----------
		rank_vector	: numpy.ndarray [1-dimensional, dtype=float]
			包含网络图中每个节点的 PageRank.

		topK : list of tuple [(int, double), (int, double), ...]
			包含top的 `number_of_nodes` 的节点和排名`.

		ranks : dict {int: double, int: double}
			包含网络图中节点的排名.

		
		Returns
		-------
		weighted_edges : defaultdict(list) 
			{
				(int, double): [(int, double), (int, double), ...],
				(int, double): [(int, double), (int, double), ...],
				(int, double): [(int, double), (int, double), ...],
				... 
			}
			(int, double) : (node: rank) 
			按照排名前k的节点列表.
			包含top的 `number_of_nodes` 的节点和排名`.

		"""

		weighed_edges = defaultdict(list)
		
		for couple in topK:
			weighed_edges[(couple[1], couple[0])] = [(node, ranks[node]) 
				for node in self.edges[couple[1]]]

		return weighed_edges


	def get_EdgesToDrawWithRanks(self, drawing_list, ranks):
		"""返回要在图形上显示的边列表和节点等级.

		
		Parameters
		----------
		drawing_list : defaultdict(list)
		{
			(int, double): [(int, double), (int, double), ...],
			(int, double): [(int, double), (int, double), ...],
			(int, double): [(int, double), (int, double), ...],
			... 
		}
		(int, double) : (node: rank) 
		按照排名前k的节点列表.
		包含top的 `number_of_nodes` 的节点和排名`.

		ranks : dict {int: double, int: double}
			包含网络图中节点的排名.

		
		Returns
		-------
		edge_list : list of tuple [(int, int), (int, int), ...]
			(int, int) : (node1, node2)
			符号化从node1到node2的有向边.

		nodes_to_draw : list of tuple [(int, double), (int, double), ...]
			(int, double) : (node, rank)
			节点属于要在图上绘制的一组节点.

		"""
		edge_list=[]
		to_draw_node_set = set();
		for (node, rank) in drawing_list:
			to_draw_node_set.add(node)
			for child in drawing_list[(node, rank)]:
				to_draw_node_set.add(child[0])
				edge_list.append((node, child[0]))

		nodes_to_draw = [(node, ranks[node]) for node in to_draw_node_set]
		return (edge_list, nodes_to_draw)

	
	def draw(self, edge_list, nodes_to_draw):
		"""在屏幕上绘制节点大小等于节点等级的有向图.


		Parameters
		----------
		edge_list : list of tuple [(int, int), (int, int), ...]
			(int, int) : (node1, node2)
			符号化从node1到node2的有向边.

		nodes_to_draw : list of tuple [(int, double), (int, double), ...]
			(int, double) : (node, rank)
			节点属于要在图上绘制的一组节点.

		
		Returns
		-------
		None

		"""
		Graph = nx.DiGraph()
		Graph.add_edges_from(sorted(edge_list))
		print(sorted(edge_list))
		
		fig = plt.figure()
		timer = fig.canvas.new_timer(self.interval)
		timer.add_callback(plt.close)

		# pos = nx.spring_layout(Graph)
		pos = nx.shell_layout(Graph)
		nx.draw_networkx_nodes(Graph, 
				pos, 
				cmap=plt.get_cmap('jet'), 
				node_size=[node[1]*10000 for node in nodes_to_draw])
		nx.draw_networkx_labels(Graph, pos, labels={node[0]: node[0] for node in nodes_to_draw})
		nx.draw_networkx_edges(Graph, pos, arrows=True)
		timer.start()
		plt.show()

	
	def plot(self, number_of_nodes, rank_vector):
		"""调用函数，以适当的顺序调用其他函数来绘制图形.

		Parameters
		----------
		number_of_nodes : int
			包含要选取的节点数.

		rank_vector	: numpy.ndarray [1-dimensional, dtype=float]
			包含网络图中每个节点的 PageRank.

		Returns
		-------
		None	
	
		"""
		ranks = {node: rank for (node, rank) in enumerate(rank_vector)}
		topK = self.get_KMaxRankNodes(number_of_nodes, rank_vector)
		drawing_list = self.get_edgesConnectedToTopK(rank_vector, topK, ranks)
		(edge_list, nodes_to_draw) = self.get_EdgesToDrawWithRanks(
														drawing_list, ranks)
		self.draw(edge_list, nodes_to_draw)