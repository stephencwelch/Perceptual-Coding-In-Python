## PEAQ.py
##  
## PEAQ.py is our overall class implementation of the PEAQ algorihtm. We are leaving big parts 
## out, and taking a significanly different appraoch to overall architechture than Kabal 2002.
##
## Matthew Cohen and Stephen Welch
## Version 1.0

import numpy as np
from PQEval import PQEval

class PEAQ(object):
	def __init__(self, Amax = 1, Fs = 48000, NF = 2048):
		# Amax = maximum signal amplitude
		# Fs = sampling frequency
		# NF = Length of analysis window

		self.NF = NF
		self.Fs = Fs
		self.Amax = Amax

		#Step forward in half window lengths:
		Nadv = self.NF / 2

		#Number of critical bands:
		self.Nc = 109

	def process(self, sigR, sigT):
		#Preform basic procssing (Section 2 in Kabal.)
		# sigR = reference signal	
		# sigT = test signal

		#Number of frames:
		self.Np = np.floor(len(sigR)/Nadv)
		
		#Scale audio:
		if np.amax(abs(sigR)) != self.Amax:
			sigRS = self.Amax*sigR/float(np.amax(abs(sigR)))
			sigTS = self.Amax*sigT/float(np.amax(abs(sigT)))
			print 'Signals scaled, max reference value = ' + str(np.amax(abs(sigRS))) + ','
			print 'and max test value = ' + str(np.amax(abs(sigTS))) +'.'

		#Instantiate Object to process single frames of data:
		self.PQE = PQEval(Amax = self.Amax, Fs = self.Fs, NF = self.NF)

		#Create empty matrices:
		X2 = np.zeros((2,self.NF/2+1))

		self.X2MatR = np.zeros((self.Np, self.NF/2+1))
		self.X2MatT = np.zeros((self.Np, self.NF/2+1))

		self.EbNMat = np.zeros((self.Np, self.Nc))
		self.EsMatR = np.zeros((self.Np, self.Nc))
		self.EsMatT = np.zeros((self.Np, self.Nc))

		self.EhsR = np.zeros((self.Np, self.Nc))
		self.EhsT = np.zeros((self.Np, self.Nc))

		previousFrameR = np.zeros(self.Nc)
		previousFrameT = np.zeros(self.Nc)

		startS = 0

		#Iterate through frames: 
		for i in range(self.Np):
		    xR = sigRS[startS:self.NF+startS]
		    xT = sigTS[startS:self.NF+startS]
		    startS = startS+Nadv
		    
		    #Process Frame: 
		    X2[0,:] = self.PQE.PQDFTFrame(xR)
		    X2[1,:] = self.PQE.PQDFTFrame(xT)
		    
		    self.X2MatR[i,:] = X2[0,:]
		    self.X2MatT[i,:] = X2[1,:]
		    
		    # Critical band grouping and frequency spreading
		    self.EbN, self.Es = PQE.PQ_excitCB(X2)
		    
		    self.EbNMat[i,:] = self.EbN
		    self.EsMatR[i,:] = self.Es[0,:]
		    self.EsMatT[i,:] = self.Es[1,:]
		    
		    #Time domain spreading
		    #Can't time-spread on first frame:
		    if i > 0:
		        self.EhsR[i,:], previousFrameR = self.PQE.PQ_timeSpread(self.EsMatR[i,:], previousFrameR)
		        self.EhsT[i,:], previousFrameT = self.PQE.PQ_timeSpread(self.EsMatT[i,:], previousFrameT)
		    else:
		        #First Iteration:
		        previousFrameR = self.EsMatR[i,:]
		        previousFrameT =self.EsMatT[i,:]

	#def computeBW




