import pandas as pd
import numpy as np

from joblib import dump, load
from sklearn.feature_extraction.text import CountVectorizer
from scipy.linalg import norm
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = 'all'#默认为'last'

root = 'F:/大学/大三/大三下/机器学习/课设/intelligent_xiaokang/files_folder/'
path1 = '内科_new1.csv'
path2 = '外科_new1.csv'

for path in [path1,path2]:
    data = pd.read_csv(root+path,encoding='utf-8')
    data
    #构建模型
    cv = TfidfVectorizer(norm=None)
    #训练模型
    cv_idf = cv.fit(data['ask_clear_word'].values)
    #输出模型的一些结果
    len(cv.vocabulary_)
    print(cv.idf_)
    print(cv.vocabulary_)
    #保存模型
    dump(cv,path[:2]+'.joblib')
    #加载模型，验证模型的输出与前面训练好的模型的输出是否是一致的
    mm = load(path[:2]+'.joblib')
    len(mm.vocabulary_)