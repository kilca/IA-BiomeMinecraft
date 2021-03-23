import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import sklearn
import sklearn.svm

class DataTrainer():
	def __init__(self, X ,y):
		self.X = X
		self.y = y

	def plot(self):
		plt.scatter(self.suppVect[:,0],self.suppVect[:,1], c = 'green', s = self.size, marker='+')
		plt.show()
		plt.savefig('filename.svg')

	def plot_boundary(self):
		plt.ion()
		clf = self.clf
		self.X = X
		self.y = y
		x_min, x_max = X[:, 0].min() - .1, X[:, 0].max() + .1
		y_min, y_max = X[:, 1].min() - .1, X[:, 1].max() + .1
		Nbins = 300
		dx = max((x_max- x_min)/Nbins, (y_max- y_min)/Nbins) #  0.002 <--> Nbins=500 ## grid mesh size
		xx, yy = np.meshgrid(np.arange(x_min, x_max, dx),
							np.arange(y_min, y_max, dx))

		## prediction value by zone
		Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
		Z = Z.reshape(xx.shape)

		## crée une nouvelle figure (avec le numero suivant de la figure de numeor le plus grand)
		plt.figure(figsize=[5,5]) ## equal x and y lengths for a squared figure
		## plot du fond avec une couleur selon la valeur de Z(x,y)
		plt.contourf(xx, yy, Z, cmap=plt.cm.Paired, alpha=0.8)
		## plot des points de données ##
		plt.scatter(X[:, 0], X[:, 1], c=y, s = 100)
		## plot des vecteurs supports ##
		plt.scatter(clf.support_vectors_[:,0],clf.support_vectors_[:,1], c = 'green', s = 200, marker='+')
		plt.title('(training) "score" : ' + str(clf.score(X,y)))
		plt.xlabel('$x_1$')
		plt.ylabel('$x_2$')
		plt.legend("test")
		plt.xlim([0,1])
		plt.ylim([0,1])
	'''
	def make_separable_square(self,Nset, seed):
		np.random.seed(seed)
		X = np.random.random_sample( (Nset,2) )
		y = (X[:,0] > 0.5)
		return X,y
	'''

	def train(self,percent=80):
		X = self.X
		y = self.y
		N = int(len(X)*(percent/100))
		#Xval, yval = X[80:N] , y[80:N] ## TODO : générer un validation set adéquat.
		#X, y       = X[0:80] , y[0:80]  #slices 
		Xval, yval = X[N:len(X)] , y[N:len(y)] ## TODO : générer un validation set adéquat.
		X, y       = X[0:N] , y[0:N]  #slices 
		#a = np.random.random((10,4))
		print("we begin to learn with size : ",len(X))
		clf = sklearn.svm.SVC(kernel='linear', C=1) ## TODO: lire la doc, pour comprendre quels arguments choisir !
		clf.fit(X,y)
		#y_pred = clf.predict(Xval)
		print("training score:",clf.score(X,y))
		print("validation score:",clf.score(Xval,yval))
		suppVect = clf.support_vectors_ ## TODO : recuperer les vecteurs supports, en utilisant l'objet "clf"
		size=100

		self.suppVect = suppVect
		self.size = size


