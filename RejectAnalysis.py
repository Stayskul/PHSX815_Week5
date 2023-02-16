import numpy as np
import sys
import matplotlib.pyplot as plt

sys.path.append(".")
from Extras.Random import Random


bin_width = 0.
Xmin = 0.
Xmax = 1.
random=Random()
#my target function f(x)== semi circle, r=0.5, centered at x=0.5
def SemiCirc(x):
    return np.sqrt((0.5**2-(x-0.5)**2))
#g(x)
def Flat(x):
    return 0.5

# factor of (0.0125/0.005) is added so that the plots scale correctly, and match the histogram
def PlotFlat(x,ben_width):
	return (0.0125/0.005)*bin_width*0.5
	
def PlotCirc(x,bin_width):
	return (0.0125/0.005)*bin_width*SemiCirc(x)

# Get a random X value according to a flat distribution
def SampleFlat():
	return Xmin + (Xmax-Xmin)*random.rand()
#main function
if __name__ == "__main__":


	# default number of samples
	Nsample = 100

	# read the user-provided seed from the command line (if there)
	if '-Nsample' in sys.argv:
		p = sys.argv.index('-Nsample')
		Nsample = int(sys.argv[p+1])
	if '-range' in sys.argv:
		p = sys.argv.index('-range')
		Xmax = float(sys.argv[p+1])
		Xmin = -float(sys.argv[p+1])
	if '-h' in sys.argv or '--help' in sys.argv:
		print ("Usage: %s [-Nsample] number [-range] Xmax [--log] [--expo] " % sys.argv[0])
		print
		sys.exit(1)  


	data = []
	Ntrial = 0.
	i = 0.
	while i < Nsample:
		Ntrial += 1
	
		X = SampleFlat()
		R = SemiCirc(X)
		rand = random.rand()
		if(rand > R): #reject if outside
			continue
		else: #accept if inside
			data.append(X)
			i += 1 #increase i and continue
	
	if Ntrial > 0:
		print("Efficiency was",float(Nsample)/float(Ntrial))

	#normalizing Data
	weights = np.ones_like(data) / len(data)
	n = plt.hist(data,weights=weights,alpha=0.3,label="samples from f(x)",bins=100)
	plt.ylabel("Probability / bin")
	plt.xlabel("x")
	bin_width = n[1][1] - n[1][0]
	hist_max = max(n[0])
	
	plt.ylim(min(bin_width*SemiCirc(Xmax),1./float(Nsample+1)),
	1.5*max(hist_max,bin_width*SemiCirc(0)))

	#f(x) and g(x) plots
	x = np.arange(Xmin,Xmax,0.001)
	
	y_norm = list(map(PlotCirc,x,np.ones_like(x)*bin_width))
	
	plt.plot(x,y_norm,color='green',label='target f(x)')

	y_flat = list(map(PlotFlat,x,np.ones_like(x)*bin_width))
	
	plt.plot(x,y_flat,color='red',label='proposal g(x)')
	
	plt.title("Density estimation with Monte Carlo")

	plt.legend()
	plt.show()
