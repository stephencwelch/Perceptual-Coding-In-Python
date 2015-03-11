## PEAQ.py
##  
## PEAQ.py is our overall class implementation of the PEAQ algorihtm. We are leaving big parts 
## out, and taking a significanly different appraoch to overall architechture than Kabal 2002.
##
## Matthew Cohen and Stephen Welch
## Version 1.0

import numpy as np
from PQEval import PQEval
import time

class PEAQ(object):
	def __init__(self, Amax = 1, Fs = 48000, NF = 2048):
		# Amax = maximum signal amplitude
		# Fs = sampling frequency
		# NF = Length of analysis window

		self.NF = NF
		self.Fs = Fs
		self.Amax = Amax

		#Step forward in half window lengths:
		self.Nadv = self.NF / 2

		#Number of critical bands:
		self.Nc = 109

	def process(self, sigR, sigT):
		#Preform basic procssing (Section 2 in Kabal.)
		# sigR = reference signal	
		# sigT = test signal

		#Number of frames:
		self.Np = np.floor(len(sigR)/self.Nadv)-1
		
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

		print 'Processing Audio...'
		startTime = time.clock()

		for i in np.arange(self.Np):
		    xR = sigRS[startS:self.NF+startS]
		    xT = sigTS[startS:self.NF+startS]
		    startS = startS+self.Nadv
		    
		    #Process Frame: 
		    X2[0,:] = self.PQE.PQDFTFrame(xR)
		    X2[1,:] = self.PQE.PQDFTFrame(xT)
		    
		    self.X2MatR[i,:] = X2[0,:]
		    self.X2MatT[i,:] = X2[1,:]
		    
		    # Critical band grouping and frequency spreading
		    self.EbN, self.Es = self.PQE.PQ_excitCB(X2)
		    
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
		        previousFrameT = self.EsMatT[i,:]

		print 'Audio Processed! (Kabal, section 2), ' + str(self.Np) + ' windows processed ' + \
		  ' in ' + str(time.clock()-startTime) + ' seconds.'


	def computeBW(self, X2MatR, X2MatT):
		#Kabal Section 5.4
		BWRef = np.zeros(self.Np)
		BWTest = np.zeros(self.Np)

		for i in range(int(self.Np)):
			BWRef[i], BWTest[i] = self.PQmovBW(np.vstack((self.X2MatR[i,:], self.X2MatT[i,:])))

		return BWRef, BWTest

	def PQmovBW(self, X2):
	    # Bandwidth tests for a single frame of reference and test signal
	    # X2 must be of size 2xNF/2+1
	    
	    # fx and fl will always be the same values
	    fx = 21586
	    kx = int(round(self.NF * float(fx)/self.Fs)) # 921
	    fl = 8109
	    kl = int(round(self.NF * float(fl)/self.Fs)) # 346
	    FRdB = 10 # Ref. signal to exceed threshold level by 10dB
	    FR = 10**(FRdB/10.)
	    FTdB = 5 # Test signal to exceed threshold level by 5dB
	    FT = 10**(FTdB/10.)
	    N = self.NF/2
	    
	    # This is the method Kabal uses to find the threshold level.
	    # The for loop seems unneccessary and not as efficient as
	    # simply using a max operation on an array of the subset of DFT square mag.
	    # values above 21.6kHz.
	    
	    #Xth = X2[1,kx]
	    #for k in xrange(kx,N-1):
	    #    Xth = max(Xth, X2[1,k+1])
	        
	    # Using the max operation on the subset of array values.
	    # When tested, was about 0.1ms faster, produces same result,
	    # and is cleaner, so I'll stick with this version.
	    Xth = np.amax(X2[1,kx:N])
	    
	    # BWRef and BWTest remain negative if the BW of the test signal
	    # does not exceed FR * Xth for kx-1 <= k <= kl+1
	    BWRef = -1
	    XthR = FR * Xth # Reference signal threshold level
	    for k in xrange(kx-1,kl,-1):
	        if (X2[0,k+1] >= XthR):
	            BWRef = k+1
	            break
	            
	    BWTest = -1
	    XthT = FT * Xth # Test signal threshold level
	    for k in xrange(BWRef-1,-1,-1):
	        if (X2[1,k+1] >= XthT):
	            BWTest = k+1
	            break
	            
	    return BWRef, BWTest




