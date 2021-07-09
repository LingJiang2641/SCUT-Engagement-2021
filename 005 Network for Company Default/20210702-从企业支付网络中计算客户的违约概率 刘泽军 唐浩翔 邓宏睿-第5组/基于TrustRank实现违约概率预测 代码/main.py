from graphs import getGraph
from PageRank import PageRank
from TrustRank import TrustRank
import pandas as pd

def run(edge_file, node_num, beta=0.85, epsilon=1e-6, max_iterations=20):
	"""调用排名函数并运行，打印出rank_vectors.


	Parameters
	----------
	edge_file : string
		存储网络图的edges的文件路径.

	node_num : int
		网络图中的节点数.
	
	beta : float, optional
		随即跳转的概率（常数，用于解决等级泄露和等级沉没的问题）.
		Default value : 0.85
	
	epsilon : float, optional
		秩中的小值和总误差应小于 epsilon，很小的常数.
		Default value : 1e-6
	
	max_iterations : int, optional
		最大迭代次数.
		Default value : 20

	
	Returns
	-------
	None
	"""

	gg = getGraph(edge_file)
	edges,defaultnodes,cash = gg.get_connections()
	#选出违约结点

	defu=[]
	for parent in defaultnodes:
				for default in defaultnodes[parent]:
					if default==1:
						defu.append(parent)
						break
	defu=list(set(defu))

	print("got edges...")

#PageRank结果

	pr = PageRank(beta, edges, epsilon, max_iterations, node_num)
	PageRank_vector = pr.pageRank()
	print(PageRank_vector, sum(PageRank_vector))
	PageRank_df=pd.DataFrame(PageRank_vector)
	PageRank_df.to_csv('./result/PageRank.csv')

#TrustRank结果

	tr = TrustRank(beta, edges, epsilon, max_iterations, node_num,
		PageRank_vector,cash,defu)
	TrustRank_vector = tr.trustRank()
	print(TrustRank_vector, sum(TrustRank_vector))
	TrustRank_df=pd.DataFrame(TrustRank_vector)
	TrustRank_df.to_csv('./result/TrustRank.csv')


if __name__ == '__main__':
	# location_of_the_edge_file = "./data/test" 测试
	# number_of_nodes_in_web_graph = 9

	location_of_the_edge_file = "./data/traderandom.txt" #运行模拟数据
	number_of_nodes_in_web_graph = 2394385
	run(location_of_the_edge_file, number_of_nodes_in_web_graph)