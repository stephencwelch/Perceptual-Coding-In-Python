## PQEval.py
## The PQEval class corresponds to Kabal's Matab function PQeval.m, which operates 
## on single frames of data at at time. See Explor PEAQ for lots more information.
##
##
## Matthew Cohen and Stephen Welch
## Version 1.0

import numpy as np

class PQEval(object):
	def __init__(self, Amax = 1, Fs= 48000, NF= 2048):
		# Amax is maximum signal amplitude, Fs is sampling frequency
		#Setup parameters and precompute quantities we'll need.
		self.Fs = Fs
		self.NF = NF

		#Hardcode the louness scalling params:
		fcLoudness = 1019.5
		Lp = 92

		#Set up the window (including all gains)
		self.GL = self.PQ_GL(NF= self.NF, Amax = Amax, fcN = fcLoudness/self.Fs, Lp = Lp)

		#Precompute hann window:
		self.hw = self.GL*self.PQHannWin(self.NF)

		#Precompute frequency vector:
		self.f = np.linspace (0, self.Fs/2, self.NF/2+1)

		#Outer and middle ear weighting:
		self.W2 = self.PQWOME (self.f)

		#Critical band constants:
		self.Nc, self.fc, self.fl, self.fu, self.dz = self.PQCB()

		#Internal Noise:
		self.EIN = self.PQIntNoise(self.fc)

		#Precompute normalization for frequency spreading:
		self.Bs = self.PQ_SpreadCB(np.ones(self.Nc), np.ones(self.Nc))

		# Allocate storage
		self.Eb = np.zeros((2, self.Nc))
		self.Xw2 = np.zeros((2, self.NF/2+1))
		self.XwN2 = np.zeros(self.NF/2+1)
		self.E = np.zeros(self.Eb.shape)
		self.Es = np.zeros((2, self.Nc))

		#Precompute for PQ Group:
		self.df = float(self.Fs) / self.NF
		self.Emin = 1e-12
		
		self.U = np.zeros((self.NF/2+1, self.Nc))

		for k in range(self.NF/2+1):
			for i in range(self.Nc):
				temp = (np.amin([self.fu[i], (k+0.5)*self.df]) - np.amax([self.fl[i], (k-0.5)*self.df])) / self.df
				self.U[k, i] = np.amax([0, temp])
				

		print "Everything Precomputed, ready to go!"

	def PQDFTFrame(self, x):
		# Window the data
		xw = self.hw * x

		# DFT (output is real followed by imaginary)
		X = self.PQRFFT(xw, self.NF, 1)

		# Squared magnitude
		X2 = self.PQRFFTMSq(X, self.NF)
		
		return X2

	def PQ_excitCB(self, X2):
		# Critical band grouping and frequency spreading

		# Outer and middle ear filtering
		self.Xw2[0,:] = self.W2 * X2[0,0:self.NF/2+1]
		self.Xw2[1,:] = self.W2 * X2[1,0:self.NF/2+1]

		# Form the difference magnitude signal
		self.XwN2 = self.Xw2[0,:] - 2*np.sqrt(self.Xw2[0,:]*self.Xw2[1,:]) + self.Xw2[1,:]
		
		# Group into partial critical bands
		self.Eb[0,:] = self.PQgroupCB(self.Xw2[0,:])
		self.Eb[1,:] = self.PQgroupCB(self.Xw2[1,:])
		self.EbN     = self.PQgroupCB(self.XwN2)

		# Add the internal noise term => "Pitch patterns"
		self.E[0,:] = self.Eb[0,:] + self.EIN
		self.E[1,:] = self.Eb[1,:] + self.EIN

		# Critical band spreading => "Unsmeared (in time) excitation patterns"
		self.Es[0,:] = self.PQspreadCB(self.E[0,:])
		self.Es[1,:] = self.PQspreadCB(self.E[1,:])
		
		return self.EbN, self.Es

	def PQgroupCB(self, X2):
		# Group a DFT energy vector into critical bands
		# X2 - Squared-magnitude vector (DFT bins)
		# Eb - Excitation vector (fractional critical bands)

		Eb = np.dot(X2,self.U)
		Eb[Eb<self.Emin] = self.Emin
		
		return Eb

	def PQspreadCB(self, E):
		# Spread an excitation vector (pitch pattern) - FFT model
		# Both E and Es are powers	    
		Es = self.PQ_SpreadCB(E, self.Bs)
		
		return Es

	def PQ_SpreadCB(self, E, Bs):
		
		e = 0.4 # Commonly used power value
		
		# Initialize arrays for storage. These values are used
		# in each iteration (summed over, multiplied, raised to
		# powers, etc.) when computing the spread Bark-domain
		# energy Es.
		#
		# aUCEe is for the product of bin-dependent (index l)
		# term aC, energy-dependent (E) term aE, and
		# term aU.
		#
		# Ene is (E[l]/A(l,E[l]))^e, stored for each index l
		#
		# Es is the overall spread Bark-domain energy
		#

		aUCEe = np.zeros(self.Nc)
		Ene = np.zeros(self.Nc)
		Es = np.zeros(self.Nc)
		
		# Calculate energy-dependent terms
		aL = 10**(2.7*self.dz)

		for l in xrange(self.Nc):
			aUC = 10**((-2.4 - 23/self.fc[l])*self.dz)
			aUCE = aUC * (E[l]**(0.2*self.dz))
			gIL = (1 - aL**(-1*(l+1))) / (1 - aL**(-1))
			gIU = (1 - (aUCE)**(self.Nc-l)) / (1 - aUCE)
			En = E[l] / (gIL + gIU - 1)
			aUCEe[l] = aUCE**(e)
			Ene[l] = En**(e)
		
		# Lower spreading
		Es[self.Nc-1] = Ene[self.Nc-1]
		aLe = aL**(-1*e)
		for i in xrange((self.Nc-2),-1,-1):
			Es[i] = aLe*Es[i+1] + Ene[i]
		
		
		# Upper spreading (i > m)
		for i in xrange(0,(self.Nc-1)):
			r = Ene[i]
			a = aUCEe[i]
			for l in xrange((i+1),self.Nc):
				r = r*a
				Es[l] = Es[l] + r
				
		# Normalize the values by the normalization factor
		for i in xrange(0,self.Nc):
			Es[i] = (Es[i]**(1/e)) / Bs[i]
			
		return Es

	def PQ_timeSpread(self, Es, Ef):
		
		Nadv = self.NF/2
		Fss = float(self.Fs)/Nadv
		tau_100 = 0.030
		tau_min = 0.008
		alpha = self.PQtConst(tau_100, tau_min, self.fc, Fss)
		
		# Allocate storage
		Ehs = np.zeros(self.Nc)
		
		# Time domain smoothing
		for i in xrange(self.Nc):
			Ef[i] = alpha[i]*Ef[i] + (1-alpha[i])*Es[i]
			Ehs[i] = max(Ef[i],Es[i])
		   
		return Ehs, Ef

	def PQtConst(self, tau_100, tau_min, fc, Fss):
		# Tau values in units of seconds
		#tau_100 = 0.030
		#tau_min = 0.008
		
		tau = np.zeros(len(fc))
		alpha = np.zeros(len(fc))
		
		tau = tau_min + (np.divide(float(100),fc))*(tau_100 - tau_min)
		alpha = np.exp(np.divide(-1./Fss,tau))
		
		return alpha

	#Internal noise:
	def PQIntNoise (self, f):
		INdB = 1.456 * (f / 1000.)**(-0.8)
		EIN = 10**(INdB / 10.)
		return EIN

	#Method to make hanning window, given lenth of window:	
	def PQHannWin(self, NF):
		n = np.arange(0, NF)
		hw = 0.5*(1-np.cos(2*np.pi*n/(NF-1)))
		return hw 

	def PQRFFT (self, x, N, ifn):
		# Calculate the DFT of a real N-point sequence or the inverse
		# DFT corresponding to a real N-point sequence.
		# ifn > 0, forward transform
		#          input x(n)  - N real values
		#          output X(k) - The first N/2+1 points are the real
		#            parts of the transform, the next N/2-1 points
		#            are the imaginary parts of the transform. However
		#            the imaginary part for the first point and the
		#            middle point which are known to be zero are not
		#            stored.
		# ifn < 0, inverse transform
		#          input X(k) - The first N/2+1 points are the real
		#            parts of the transform, the next N/2-1 points
		#            are the imaginary parts of the transform. However
		#            the imaginary part for the first point and the
		#            middle point which are known to be zero are not
		#            stored. 
		#          output x(n) - N real values


		if (ifn > 0):
			X = np.fft.fft (x, N)
			XR = np.real(X[0:N/2+1])
			XI = np.imag(X[1:N/2-1+1])
			X = np.concatenate([XR, XI])
			return X
		else:
			raise Exception('ifft Not Implemented Yet -SW')

	def PQRFFTMSq(self, X, N):
		# Calculate the magnitude squared frequency response from the
		# DFT values corresponding to a real signal (assumes N is even)

		X2 = np.zeros(N/2+1)

		X2[0] = X[0]**2
		for k in range(N/2-1):
			X2[k+1] = X[k+1]**2 + X[N/2+k+1]**2

		X2[N/2] = X[N/2]**2
		return X2

	def PQ_GL(self, NF=2048, Amax=1, fcN=1019.5/48000., Lp=92.):
		#Scaled Hann window, including loudness scaling
		# Calculate the gain for the Hann Window
		#  - level Lp (SPL) corresponds to a sine with normalized frequency
		#    fcN and a peak value of Amax
		
		W = NF-1
		gp = self.PQ_gp(fcN, NF, W)
		GL = 10**(Lp/20.) / (gp *Amax/4 *W)
		return GL
		
	def PQ_gp(self, fcN, NF, W):
		# Calculate the peak factor. The signal is a sinusoid windowed with
		# a Hann window. The sinusoid frequency falls between DFT bins. The
		# peak of the frequency response (on a continuous frequency scale) falls
		# between DFT bins. The largest DFT bin value is the peak factor times
		# the peak of the continuous response.
		# fcN - Normalized sinusoid frequency (0-1)
		# NF  - Frame (DFT) length samples
		# NW  - Window length samples

		#Distance to the nearest DFT bin
		df = 1./NF
		k = np.floor(fcN/df)
		dfN = np.amin([(k+1)*df - fcN, fcN -k*df])
		
		dfW = dfN*W
		gp = np.sin(np.pi*dfW) / (np.pi*dfW*(1-dfW**2))
		return gp

	def PQWOME(self, f):
		# Generate the weighting for the outer & middle ear filtering
		# Note: The output is a magnitude-squared vector
		
		N = len(f)
		W2 = np.zeros(N)
		
		for k in range(N-1):
			fkHz = float(f[k+1])/1000
			AdB = -2.184 * fkHz**(-0.8) + 6.5 * np.exp(-0.6 * (fkHz - 3.3)**2) - 0.001 * fkHz**(3.6)
			W2[k+1] = 10**(AdB / 10);
		
		return W2

	def PQCB(self):
		#Critical band parameters for the FFT model, for Basic Version:
		dz = 1./4
		
		#I don't see why we can't hardcode this:
		Nc = 109

		fl = np.array([  80.000,   103.445,   127.023,   150.762,   174.694, \
			   198.849,   223.257,   247.950,   272.959,   298.317, \
			   324.055,   350.207,   376.805,   403.884,   431.478, \
			   459.622,   488.353,   517.707,   547.721,   578.434, \
			   609.885,   642.114,   675.161,   709.071,   743.884, \
			   779.647,   816.404,   854.203,   893.091,   933.119, \
			   974.336,  1016.797,  1060.555,  1105.666,  1152.187, \
			  1200.178,  1249.700,  1300.816,  1353.592,  1408.094, \
			  1464.392,  1522.559,  1582.668,  1644.795,  1709.021, \
			  1775.427,  1844.098,  1915.121,  1988.587,  2064.590, \
			  2143.227,  2224.597,  2308.806,  2395.959,  2486.169, \
			  2579.551,  2676.223,  2776.309,  2879.937,  2987.238, \
			  3098.350,  3213.415,  3332.579,  3455.993,  3583.817, \
			  3716.212,  3853.817,  3995.399,  4142.547,  4294.979, \
			  4452.890,  4616.482,  4785.962,  4961.548,  5143.463, \
			  5331.939,  5527.217,  5729.545,  5939.183,  6156.396, \
			  6381.463,  6614.671,  6856.316,  7106.708,  7366.166, \
			  7635.020,  7913.614,  8202.302,  8501.454,  8811.450, \
			  9132.688,  9465.574,  9810.536, 10168.013, 10538.460, \
			 10922.351, 11320.175, 11732.438, 12159.670, 12602.412, \
			 13061.229, 13536.710, 14029.458, 14540.103, 15069.295, \
			 15617.710, 16186.049, 16775.035, 17385.420 ])
		fc = np.array([  91.708,   115.216,   138.870,   162.702,   186.742, \
			   211.019,   235.566,   260.413,   285.593,   311.136, \
			   337.077,   363.448,   390.282,   417.614,   445.479, \
			   473.912,   502.950,   532.629,   562.988,   594.065, \
			   625.899,   658.533,   692.006,   726.362,   761.644, \
			   797.898,   835.170,   873.508,   912.959,   953.576, \
			   995.408,  1038.511,  1082.938,  1128.746,  1175.995, \
			  1224.744,  1275.055,  1326.992,  1380.623,  1436.014, \
			  1493.237,  1552.366,  1613.474,  1676.641,  1741.946, \
			  1809.474,  1879.310,  1951.543,  2026.266,  2103.573, \
			  2183.564,  2266.340,  2352.008,  2440.675,  2532.456, \
			  2627.468,  2725.832,  2827.672,  2933.120,  3042.309, \
			  3155.379,  3272.475,  3393.745,  3519.344,  3649.432, \
			  3784.176,  3923.748,  4068.324,  4218.090,  4373.237, \
			  4533.963,  4700.473,  4872.978,  5051.700,  5236.866, \
			  5428.712,  5627.484,  5833.434,  6046.825,  6267.931, \
			  6497.031,  6734.420,  6980.399,  7235.284,  7499.397, \
			  7773.077,  8056.673,  8350.547,  8655.072,  8970.639, \
			  9297.648,  9636.520,  9987.683, 10351.586, 10728.695, \
			 11119.490, 11524.470, 11944.149, 12379.066, 12829.775, \
			 13294.850, 13780.887, 14282.503, 14802.338, 15341.057, \
			 15899.345, 16477.914, 17077.504, 17690.045 ])
		fu = np.array([ 103.445,   127.023,   150.762,   174.694,   198.849, \
			   223.257,   247.950,   272.959,   298.317,   324.055, \
			   350.207,   376.805,   403.884,   431.478,   459.622, \
			   488.353,   517.707,   547.721,   578.434,   609.885, \
			   642.114,   675.161,   709.071,   743.884,   779.647, \
			   816.404,   854.203,   893.091,   933.113,   974.336, \
			  1016.797,  1060.555,  1105.666,  1152.187,  1200.178, \
			  1249.700,  1300.816,  1353.592,  1408.094,  1464.392, \
			  1522.559,  1582.668,  1644.795,  1709.021,  1775.427, \
			  1844.098,  1915.121,  1988.587,  2064.590,  2143.227, \
			  2224.597,  2308.806,  2395.959,  2486.169,  2579.551, \
			  2676.223,  2776.309,  2879.937,  2987.238,  3098.350, \
			  3213.415,  3332.579,  3455.993,  3583.817,  3716.212, \
			  3853.348,  3995.399,  4142.547,  4294.979,  4452.890, \
			  4643.482,  4785.962,  4961.548,  5143.463,  5331.939, \
			  5527.217,  5729.545,  5939.183,  6156.396,  6381.463, \
			  6614.671,  6856.316,  7106.708,  7366.166,  7635.020, \
			  7913.614,  8202.302,  8501.454,  8811.450,  9132.688, \
			  9465.574,  9810.536, 10168.013, 10538.460, 10922.351, \
			 11320.175, 11732.438, 12159.670, 12602.412, 13061.229, \
			 13536.710, 14029.458, 14540.103, 15069.295, 15617.710, \
			 16186.049, 16775.035, 17385.420, 18000.000 ])
		
		return Nc, fc, fl, fu, dz
