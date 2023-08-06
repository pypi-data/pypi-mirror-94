import pandas as pd
import seaborn as sns; sns.set_theme()
from sklearn.decomposition import PCA
import numpy as np

def plot_heatmap(data):
	ax = sns.heatmap(np.sum(data,0))
	
def dimension_reduction_pca(data, dimension):
	data_shape = data.shape
	if len(data_shape) > 2:
		reshape_val = 1;
		for i in range(1,len(data_shape)):
			reshape_val = reshape_val * data_shape[i]                
		data = data.reshape(data_shape[0],reshape_val)
				
	pca = PCA(n_components=dimension, svd_solver='full')
	pca.fit(data)
	
	dimension_PCAs = [];
	for i in range(1, dimension+1):
		dimension_PCAs.append('PC-' + str(i))
		
	print(f"Explained Variance: {pca.explained_variance_}")
	
	print(pd.DataFrame(pca.components_,columns=list(range(0, data.shape[1])),index = dimension_PCAs))
                
        