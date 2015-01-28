
import numpy as np

def makeToeplitz(inputVec, numColumns):
#Make Toeplitz Design Matrix
    from numpy import zeros
    toeplitzMatrix = zeros((len(inputVec)-numColumns+1, numColumns))
    for k in range(numColumns):
        toeplitzMatrix[:, k] = inputVec[k:(len(inputVec)-numColumns+k+1)]
    return toeplitzMatrix

from scipy.stats import pearsonr
import time


def checkTimeAlignmentAndPlot(input, output, exampleSize = 128, maxOffset = 200, stepSize = 5, \
							  numSamples = 17640, randomize = True, plot = True):

	randVec = np.arange(10*maxOffset, len(input)-10*maxOffset)

	numSamples = 17640

	if randomize:
		np.random.shuffle(randVec)

	trainingIndices = randVec[0:numSamples]
	testingIndices = randVec[numSamples:2*numSamples]

	#Make piezo audio into design matrix:
	designMatrix = makeToeplitz(input, 128)

	offsets, trainMSE, testMSE = timeShiftAndModel(exampleSize=exampleSize, maxOffset = maxOffset, \
													stepSize = stepSize, trainingIndices = trainingIndices, \
													testingIndices = testingIndices, \
													designMatrixOverall = designMatrix, targetSignal = output)


	offsets, correlations = timeShiftAndCorrelate(maxOffset = maxOffset, stepSize = 5, \
                                              testingIndices = testingIndices, inputSignal = input, \
                                              targetSignal = output)

	if plot:
		from matplotlib import pyplot
		fig = pyplot.figure(0, (12,6))

		fig.add_subplot(1,2,1)
		pyplot.plot(offsets, trainMSE)
		pyplot.plot(offsets, testMSE,'x')
		pyplot.grid(1)

		pyplot.xlabel('offset samples')
		pyplot.ylabel('MSE')
		pyplot.legend(['train Mic 1', 'test Mic 1'], loc=1)
		pyplot.title('OLS Model error')

		fig.add_subplot(1,2,2)
		pyplot.plot(offsets, correlations)
		pyplot.grid(1)

		pyplot.xlabel('offset samples')
		pyplot.ylabel('Correlation')
		pyplot.legend(['Correlation Mic 1'], loc=1)
		pyplot.title('Correlation')

	return offsets, trainMSE, testMSE, correlations


def timeShiftAndCorrelate(maxOffset, stepSize, testingIndices, inputSignal, targetSignal):
    offsetsToTest = range(-maxOffset, maxOffset, stepSize)
    correlations = np.zeros(len(offsetsToTest))
    
    startTime = time.clock()
    for index, offset in enumerate(offsetsToTest):
        x = inputSignal[testingIndices]
        y = targetSignal[testingIndices+offset]
        correlations[index] = pearsonr(x, y)[0]
        
    print 'Correlation Test Done! Time Elapsed = ' + str(time.clock()-startTime) + 's. '
        
    return offsetsToTest, correlations

#Compare Performance for various timeshifts:
from sklearn import linear_model

def timeShiftAndModel(exampleSize,  maxOffset, stepSize, trainingIndices, testingIndices, \
                      designMatrixOverall, targetSignal):    

    clf = linear_model.LinearRegression(fit_intercept=False)
    
    offsetsToTest = range(-maxOffset, maxOffset, stepSize)
    trainMSE = np.zeros(len(offsetsToTest))
    testMSE = np.zeros(len(offsetsToTest))

    startTime = time.clock()
    for index, offset in enumerate(offsetsToTest):
        
        #Train
        designMatrix = designMatrixOverall[trainingIndices+maxOffset,:]
        y = targetSignal[trainingIndices+exampleSize-1+maxOffset+offset]   
        clf.fit(designMatrix,y)
        yHat = clf.predict(designMatrix)
        trainMSE[index] = 0.5*sum((yHat-y)**2)/float(len(trainingIndices))

        # Test- just start testing vector right after training vector, may be good to randomize.
        designMatrix = designMatrixOverall[testingIndices+maxOffset,:]

        y = targetSignal[testingIndices+exampleSize-1+maxOffset+offset]
        yHat = clf.predict(designMatrix)
        testMSE[index] = 0.5*sum((yHat-y)**2)/float(len(testingIndices))


    print 'Modeling Test Done! Time Elapsed = ' + str(time.clock()-startTime) + 's. '
    
    return offsetsToTest, trainMSE, testMSE

