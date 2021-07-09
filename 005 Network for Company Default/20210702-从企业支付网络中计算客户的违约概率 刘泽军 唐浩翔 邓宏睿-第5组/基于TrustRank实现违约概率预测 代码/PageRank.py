import math
import numpy as np
from graphs import plotGraph

class PageRank:
	"""以图的形式显示PageRank值.


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

	
	order : {'beta', 'edges', 'epsilon', 'max_iterations', 'node_num'}
		参数严格遵循上述顺序.
		参数都不是可选的.

	
	Methods
	-------
	pageRank()
		计算网络图中所有节点的 PageRank.

	"""

	def __init__(self, beta, edges, epsilon, max_iterations, node_num):
		self.beta = beta
		self.edges = edges
		self.epsilon = epsilon
		self.node_num = node_num
		self.MAX_ITERATIONS = max_iterations


	def pageRank(self):
		"""网络图中所有节点的 PageRank.

	
		Parameters
		----------
		None

		
		Returns
		-------
		final_rank_vector : numpy.ndarray [1-dimensional, dtype=float]
			包含网络图中每个节点的 PageRank.

		"""

		final_rank_vector = np.zeros(self.node_num)
		#初始等权重
		initial_rank_vector = np.fromiter(
			[1 / self.node_num for _ in range(self.node_num)], dtype='float')

		iterations = 0
		diff = math.inf

		pg = plotGraph(self.edges, interval=3000)

		while(iterations < self.MAX_ITERATIONS and diff > self.epsilon):
			new_rank_vector = np.zeros(self.node_num)
			for parent in self.edges:
				for child in self.edges[parent]:
					#等权重传递
					new_rank_vector[child] += (initial_rank_vector[parent] /
					len(self.edges[parent]))
			#添加缺失值
			leaked_rank = (1-sum(new_rank_vector))/self.node_num
			final_rank_vector = new_rank_vector + leaked_rank
			#迭代到新旧排名无较大变化时停止
			diff = sum(abs(final_rank_vector - initial_rank_vector))
			initial_rank_vector = final_rank_vector
			iterations += 1
			print("PageRank iteration: " + str(iterations))

			pg.plot(9, final_rank_vector)
			# print(final_rank_vector)
			# print('\n')

		return final_rank_vector