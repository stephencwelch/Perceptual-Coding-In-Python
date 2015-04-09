import numpy as np

class Bark:
    
    def __init__(self, nfft=2048, fs=48000, nfilts=109, version="rasta", width=1.0, minfreq=0, maxfreq=24000):
        
        self.nfft = nfft
        self.fs = fs
        self.nfilts = nfilts
        self.width = width
        self.min_freq = minfreq
        #self.max_freq = maxfreq
        self.max_freq = fs/2
        self.nfreqs = nfft/2
        self.version = version  # Transform type
        
        # Compute the forward Bark transform weight matrix
        # (i.e. the matrix that maps a signal from the Fourier
        # (FFT) frequency domain to the Bark domain).
        self.W = self.fft2barkmx(version)
        
        # Compute the backward Bark transform weight matrix
        # (i.e. the matrix that maps a signal from the Bark
        # domain back to the FFT domain).
        self.W_inv = self.bark2fftmx()
        
        print "The forward and backward Bark transform matrices have been precomputed - ready to go!"
        print "Bark Domain Transform Version: ", (self.version).upper()
        print "The transform is for ", self.nfilts, " filters, a sampling rate of ", self.fs, \
              " and FFT size of ", self.nfft
        
        
    def fft2barkmx(self, version):
        '''
        
        '''
        
        if version == 'rasta':
            W = self.fft2barkmx_rasta()
        elif version == 'peaq':
            W = self.fft2barkmx_peaq()
        else:
            print 'Invalid Transform Type'
            return
        
        return W
        
    
    
    def fft2barkmx_peaq(self):
        '''
        
        '''
        
        nfft = self.nfft
        nfilts  = self.nfilts
        fs = self.fs
        
        df = float(fs)/nfft
        
        fc, fl, fu = self.CB_filters()
        
        W = np.zeros((nfilts, nfft))

        for k in range(nfft/2+1):
            for i in range(nfilts):
                temp = (np.amin([fu[i], (k+0.5)*df]) - np.amax([fl[i], (k-0.5)*df])) / df
                #U[k, i] = np.amax([0, temp])
                W[i,k] = np.amax([0, temp])
                
        return W
        
    
    def fft2barkmx_rasta(self):
        '''
        
        '''
        
        #function wts = fft2barkmx(nfft, sr, nfilts, width, minfreq, maxfreq)
        # wts = fft2barkmx(nfft, sr, nfilts, width, minfreq, maxfreq)
        #      Generate a matrix of weights to combine FFT bins into Bark
        #      bins.  nfft defines the source FFT size at sampling rate sr.
        #      Optional nfilts specifies the number of output bands required 
        #      (else one per bark), and width is the constant width of each 
        #      band in Bark (default 1).
        #      While wts has nfft columns, the second half are all zero. 
        #      Hence, Bark spectrum is fft2barkmx(nfft,sr)*abs(fft(xincols,nfft));
        # 2004-09-05  dpwe@ee.columbia.edu  based on rastamat/audspec.m

        minfreq = self.min_freq
        maxfreq = self.max_freq
        nfilts = self.nfilts
        nfft = self.nfft
        fs = self.fs
        width = self.width
        
        min_bark = self.hz2bark(minfreq)
        nyqbark = self.hz2bark(maxfreq) - min_bark
        
        if (nfilts == 0):
          nfilts = np.ceil(nyqbark)+1

        W = np.zeros((nfilts, nfft))

        # bark per filt
        step_barks = nyqbark/(nfilts-1)

        # Frequency of each FFT bin in Bark
        binbarks = self.hz2bark(np.linspace(0,(nfft/2),(nfft/2)+1)*fs/nfft)

        for i in xrange(nfilts):
          f_bark_mid = min_bark + (i)*step_barks
          # Linear slopes in log-space (i.e. dB) intersect to trapezoidal window
          lof = np.add(binbarks, (-1*f_bark_mid - 0.5))
          hif = np.add(binbarks, (-1*f_bark_mid + 0.5))
          W[i,0:(nfft/2)+1] = 10**(np.minimum(0, np.minimum(np.divide(hif,width), np.multiply(lof,-2.5/width))))

        return W
        
    
    def bark2fftmx(self):
        
        # Now, attempt to map from Bark domain back to Fourier freq. domain
        
        # Fix up the weight matrix by transposing and "normalizing" 
        W_short = self.W[:,0:self.nfreqs]
        WW = np.dot(W_short.T,W_short)

        WW_mean_diag = np.maximum(np.mean(np.diag(WW))/100, np.sum(WW,1))
        WW_mean_diag = np.reshape(WW_mean_diag,(WW_mean_diag.shape[0],1))
        W_inv_denom = np.tile(WW_mean_diag,(1,self.nfilts))

        W_inv = np.divide(W_short.T, W_inv_denom)

        return W_inv

    def hz2bark(self, f):
        #       HZ2BARK         Converts frequencies Hertz (Hz) to Bark
        #
        z = 6 * np.arcsinh(f/600)
        return z
    
    
    def bark2hz(self, z):
        #       BARK2HZ         Converts frequencies Bark to Hertz (HZ)
        #
        f = 650*np.sinh(z/7)
        return f

    
    def CB_filters(self):
        #Critical band filters for creation of the PEAQ FFT model
        #(Basic Version) forward Bark domain transform weight matrix

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

        return fc, fl, fu
    
    
    def forward(self, spectrum):
        '''
        
        '''

        W_short = self.W[:,0:self.nfreqs]
        bark_spectrum = np.dot(W_short,spectrum) 
        
        return bark_spectrum
        
        
    def backward(self, bark_spectrum):
        '''
        
        '''
        
        spectrum_hat = np.dot(self.W_inv,bark_spectrum)
        
        return spectrum_hat
                 