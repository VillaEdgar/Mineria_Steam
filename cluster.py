import numpy as np
from numpy import unique
from numpy import where

import pandas as pd

import scipy
from scipy.cluster.hierarchy import dendrogram,linkage
from scipy.cluster.hierarchy import fcluster
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist

import matplotlib.pyplot as plt
from pylab import rcParams
import seaborn as sb

import sklearn
from sklearn.cluster import AgglomerativeClustering
import sklearn.metrics as sm
from sklearn.preprocessing import scale
from sklearn.preprocessing import OrdinalEncoder

#configurar el arreglo numpy para utilizar hasta 4 puntos flotantes
np.set_printoptions(precision=4,suppress=True)
rcParams["figure.figsize"] =20,10
sb.set_style("whitegrid")

##Se abren los conjuntos de datos 
steam_csv = "./archive/steam.csv"
req_csv = "./archive/steam_requirements_data.csv"
steam_df = pd.read_csv(steam_csv)
req_df = pd.read_csv(req_csv)

##Union de los conjuntos de datos
df_completo = pd.merge(left=steam_df,right=req_df, 
                       left_on='appid', right_on='steam_appid')

##Limpieza de columnas nulas
df_completo.drop(['minimum', 'recommended'], axis='columns',inplace=True)
df_completo = df_completo.head(n=100)

#conversion de pandas dataframe a numpy array
generos_array = df_completo[['genres']].copy()
enc = OrdinalEncoder()
generos_transformed = enc.fit_transform(generos_array)

#obtencion de variable de entrada(data) y obtencion de variable de salida(target)
data = scale(generos_transformed)
target = df_completo['genres']
nombres_variables = generos_array.values
nombres_variables = nombres_variables.tolist()

#Dibujo del dendograma
z = linkage(generos_transformed,"ward")
#generación del dendrograma
dendrogram(z,truncate_mode= "lastp", p =12, leaf_rotation=45,leaf_font_size=15, show_contracted=True)
plt.title("Truncated Hierachial Clustering Dendrogram")
plt.xlabel("Cluster Size")
plt.ylabel("Distance")
#division del cluster
plt.axhline(y=15)
plt.axhline(5)
plt.axhline(10)
plt.show()
#Generacion de los clusters jerarquicos
 
k = 2 
#construcción del modelo
HClustering = AgglomerativeClustering(n_clusters=k , affinity="euclidean",
                                      linkage="ward")
#acomodar el modelo con el dataset
fit = HClustering.fit(generos_transformed)
#presición del modelo
print(sm.accuracy_score(target,HClustering.labels_))

clusters = unique(fit)
# creación del grafico de dispersión
for cluster in clusters:
	# obtenemos los indices de las filas 
	row_ix = where(fit == cluster)
	# creación de las dispersiones de las muestras 
	plt.scatter(generos_transformed[row_ix, 0], generos_transformed[row_ix, 0])
# muestra la grafica
plt.show()
#$print(generos_inverted.ndim)
#print(df_completo.isnull().any())
##print(req_df.dtypes)