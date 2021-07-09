import math
import heapq
import numpy as np
from graphs import plotGraph
from scipy.sparse import csr_matrix as SparseMatrix


class TrustRank:
	"""TrustRank算法.


	Parameters
	----------
	beta : float
		随即跳转的概率.
	
	edges : collections.defaltdict(list)
		包含网络图中连接信息的邻接表.
	
	epsilon : float
		很小的常数.
	
	max_iterations : int
		最大迭代次数.
	
	node_num : int
		网络中的节点数.
	
	PageRank_vector : numpy.ndarray  [1-dimensional, dtype=float]
		包含网络图中每个节点的 PageRank.

	
	order : {'beta', 'edges', 'epsilon', 'max_iterations', 'node_num',
			'PageRank_vector'}
		参数严格遵循上述顺序.
		参数都不是可选的.
	
	Methods
	-------
	get_trustedPages(node_number_threshold=100)
		计算并返回可信的页面集，对应企业为违约的企业集.

	get_topicSpecificRank(teleport_set)
		以可信集（违约集合）`teleport_set`计算每个节点的TrustRank.
	
	trustRank()
		调用其他函数并返回rank vector.

	"""

	def __init__(self, beta, edges, epsilon, max_iterations, node_num,
		PageRank_vector,cash,defaultnode):
		self.beta = beta
		self.edges = edges
		self.epsilon = epsilon
		self.node_num = node_num
		self.PageRank_vector = PageRank_vector
		self.MAX_ITERATIONS = max_iterations
		self.cash=cash
		self.defaultnode=defaultnode

		
	def get_trustedPages(self, node_number_threshold=100):
		"""计算并返回可信的页面集，对应企业为违约的企业集.

		
		Parameters
		----------
		node_number_threshold : int, optional
			根据 node_num 是否更大来定义可信的大小.
			或低于阈值．
			Default value : 100

		
		Returns
		-------
		trusted_pages : list of int
			由节点号标识的受信任页面列表（违约率高的企业）.
			
		"""

		# set number of trusted pages
		if self.node_num < node_number_threshold:
			ratio = 0.2
		else:
			ratio = 0.0002
		trusted_set_size = int(math.ceil(self.node_num * ratio))
		
		# set and return trusted pages
		heaped_ranks = [(rank, node) for (node, rank) in 
			enumerate(self.PageRank_vector)]
		heapq._heapify_max(heaped_ranks)
		trusted_pages = [heapq._heappop_max(heaped_ranks)[1] 
			for _ in range(trusted_set_size)]
		
		return trusted_pages

	def get_topicSpecificRank(self, teleport_set):
		"""以可信集（违约集合）`teleport_set`计算每个节点的TrustRank.

		
		Parameters
		----------
		teleport_set : list of int
			网络图中随机游走可以访问的页面列表传送.
			在 TrustRank 中，该集合对应于受信任的页面.
			在企业支付网络中，对应于违约的企业

		
		Returns
		-------
		final_rank_vector : numpy.ndarray  [1-dimensional, dtype=float]
			包含网络图中每个节点的 TrustRank.

		"""

		diff = math.inf
		iterations = 0
		teleport_set_size = len(teleport_set)

		pg = plotGraph(self.edges, interval=3000)

		final_rank_vector = np.zeros(self.node_num)
		initial_rank_vector = np.fromiter(
			[1/teleport_set_size if node in teleport_set else 0 for node in
				range(self.node_num)], dtype='float')
		
		while(iterations < self.MAX_ITERATIONS and diff > self.epsilon):
			new_rank_vector = np.zeros(self.node_num)
			for parent in self.edges:
				cnt=0
				for child in self.edges[parent]:
					#parent的 rank分给child 按交易金额占总支出占比
					new_rank_vector[child] += (initial_rank_vector[parent] /
						len(self.edges[parent]))*(self.cash[parent][cnt] /sum(self.cash[parent]))
					# new_rank_vector[child] += (initial_rank_vector[parent] /
					# 	len(self.edges[parent]))
					cnt=cnt+1

			leaked_rank = (1 - sum(new_rank_vector)) / teleport_set_size
			leaked_rank_vector = np.array([leaked_rank if node in teleport_set
				else 0 for node in range(self.node_num)])
			
			final_rank_vector = new_rank_vector + leaked_rank_vector
			diff = sum(abs(final_rank_vector - initial_rank_vector))
			initial_rank_vector = final_rank_vector
			
			iterations += 1
			print("TrustRank iteration: " + str(iterations))
			print(final_rank_vector)
			pg.plot(9, final_rank_vector)

		return final_rank_vector

	def trustRank(self):
		"""以特定顺序调用其他函数的实用函数.

		
		Parameters
		----------
		None

		
		Returns
		-------
		final_rank_vector : numpy.ndarray  [1-dimensional, dtype=float]
			包含网络图中每个节点的 TrustRank.
		
		"""

		# trusted_pages = self.get_trustedPages()
		trusted_pages=self.defaultnode
		print("got seed set...")
		final_rank_vector = self.get_topicSpecificRank(trusted_pages)
		
		return final_rank_vector