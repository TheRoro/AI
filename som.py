from sklearn_som.som import SOM
from sklearn import datasets

iris = datasets.load_iris()
iris_data = iris.data[:, :2]
iris_label = iris.target
print(iris_data)
iris_som = SOM(m=3, n=1, dim=2)
iris_som.fit(iris_data)
predictions = iris_som.predict(iris_data)
