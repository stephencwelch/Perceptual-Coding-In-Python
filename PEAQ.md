# PEAQ - Perceptual Evaluation of Audio Quality

Documentation by Matthew Cohen and Stephen Welch

###Introduction

PEAQ is a standardized algorithm used for objective measurements of *perceived* audio quality, and is based on generally accepted psychoacoustic principles. The method incorporates models of both the peripheral ear component as well as a cognitive component to account for the processes associated with quality judgments.

Given a processed signal and the time-aligned original signal, concurrent frames of the signals are mapped to a basilar membrane representation, and differences in these transformed frames are analyzed in both time and frequency domain by a cognitive model. The overall goal of this analysis is to obtain a quality measure similar to a Subjective Difference Grade (SDG) acquired from listening tests with human participants. This output is called the Objective Difference Grade (ODG).

The processing steps extract perceptual features, which are used for predicting the quality measure. These intermediate features, called **Model Output Variables (MOVs)**, provide potential insight into different psychoacoustic dimensions. The MOVs are combined together to produce the final score. There are two versions of PEAQ (Basic and Advanced), which make use of different number and type of MOV parameters. The Basic uses 11, whereas the Advanced uses only 5.

The motivation behind investing more time into PEAQ is as follows: other measures and cost functions do not take perceptual aspects into consideration, and are merely waveform/spectrum-based. Both the measurable similarity and the perceptual components are embodied in the MOVs - if these features possess and convey that much information about the overall quality difference between two signals, then perhaps their underlying models and computational processes can be used as more simple, yet potentially powerful, similarity measures/cost functions. This is what brought us here.

Since PEAQ is a standard, the algorithm is licensed and targeted more at telecommunication companies. However, various implementation attempts are floating around the Internet. One commonly mentioned one is by Peter Kabal of the Multimedia Signal Processing lab at McGill University. Kabal did an extensive examination and interpretation of PEAQ, which resulted in a report titled "An Examination and Interpretation of ITU-R BS.1387: Perceptual Evaluation of Audio Quality" and a MATLAB implementation library called PQevalAudio. This code can be found floating around on the Internet (we acquired it through a GitHub account for a CCRMA student). Our analyses and results below made use of this code.

###Model Output Variable (MOV) Overview

###How to Use the PEAQ Code

The PEAQ code is contained in a directory called PQevalAudio, with the following structure:

Testing/
	PQevalAudio_fn.m
	/* Testing scripts, files, and audio samples */
	PQevalAudio-v1r0/
		PQevalAudio/
			PQevalAudio.m
			PQnNet.m
			CB/
			Misc/
			MOV/

The subfolders contain supporting functions to accomplish the various computations. Keeping PQevalAudio folder below the testing allows us to separate the testing material separate, keeping the main folders clean. The file of importance here is **PQevalAudio_fn.m**, which is the function that computes the ODG value. It operates exactly the same as /Testing/PQevalAudio-v1r0/PQevalAudio.m, except that it has been modified to output the MOVs vector.

Using **PQevalAudio_fn.m** is very easy. The function syntax is as follows:

function [ODG,MOVB] = PQevalAudio_fn(Fref, Ftest, StartS, EndS)

where Fref and Ftest are the filenames storing the reference and test signals, respectively; StartS and EndS are optional input arguments that specify the starting and ending samples. The outputs are the score, ODG, and the 11-dimensional MOV vector MOVB, where the B stands for "Basic Version." 

(**NOTE** : At this point, only the basic version of PEAQ has been used, with uncertainty as to whether or not the advanced version has been implemented in the code.)

###Test/Data Collecting Scripts

###Results and Analysis

Testing was done using four acoustic guitar signal files, with the files corresponding the the same recording done with four different sources: three microphones and a piezo pickup. The naming convention is as follows: mic1, mic2, mic3, and piezo. Three different time durations were used: 1 second, 10 seconds, and 25 seconds. For each duration set, the signals were normalized and time-aligned. The final file format used is as follows: "timeAligned_<source>_Xsec.wav" (for example, "timeAligned_mic1_10sec.wav"). The files are stored in the exports folder.

For each duration, PEAQ was applied to all permutations of signal orderings (for reference and test signals), resulting in 16 tests for each time duration. The resulting values for all 12 parameters (11 MOV parameters and the ODG value) were put into parameter-specific tables to aid in the analysis process.

The idea was to tabulate the resulting values and see if there were any discernable differences between microphone-to-microphone and microphone-to-piezo comparisons for each parameter. We were able to identify a handful of parameters that appeared to be promising metrics, in that there was a noticeable difference in magnitude of parameter value for these different scenarios. Tables for these parameter outputs are shown below (all of the .xlsx files containing tables for each parameter are stored in the /data/PEAQ_data folder).


#####Total NMRB (1 second)

|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | -135.0962  | -1.7464  | -5.3445  | -0.8371  |
|  **Mic 2** | 5.0941  | -132.6024  | 3.5502  | 0.8541  |
|  **Mic 3** | -4.019  | -1.7633  | -135.0105  | -0.5765  |
|  **Piezo** | 15.5656  | 9.2832  | 14.2897  | -127.1571  |


#####Total NMRB (10 seconds)
|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | -127.727  | -1.5176  | -5.1531  | -0.5891  |
|  **Mic 2** | 3.1955  | -126.5226  | 2.5799  | 0.7464  |
|  **Mic 3** | -4.7174  | -1.6902  | -127.554  | -0.6642  |
|  **Piezo** | 12.106  | 6.5834  | 11.5161  | -124.0896  |


#####Total NMRB (25 seconds)
|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | -128.6971  | -1.5266  | -5.5284  | -0.6219  |
|  **Mic 2** | 3.1294  | -127.4114  | 2.7351  | 0.6346  |
|  **Mic 3** | -5.073  | -1.6967  | -128.5289  | -0.7086  |
|  **Piezo** | 12.4067  | 7.1085  | 11.787  | -124.7092  |


#####(1 second)
|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | 0  | 0  | 0  | 0  |
|  **Mic 2** | 0  | 0  | 0  | 0  |
|  **Mic 3** | 0  | 0  | 0  | 0  |
|  **Piezo** | 0  | 0  | 0  | 0  |


#####(10 seconds)
|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | 0  | 0  | 0  | 0  |
|  **Mic 2** | 0  | 0  | 0  | 0  |
|  **Mic 3** | 0  | 0  | 0  | 0  |
|  **Piezo** | 0  | 0  | 0  | 0  |


#####(25 seconds)
|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | 0  | 0  | 0  | 0  |
|  **Mic 2** | 0  | 0  | 0  | 0  |
|  **Mic 3** | 0  | 0  | 0  | 0  |
|  **Piezo** | 0  | 0  | 0  | 0  |


#####(1 second)
|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | 0  | 0  | 0  | 0  |
|  **Mic 2** | 0  | 0  | 0  | 0  |
|  **Mic 3** | 0  | 0  | 0  | 0  |
|  **Piezo** | 0  | 0  | 0  | 0  |


#####(10 seconds))
|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | 0  | 0  | 0  | 0  |
|  **Mic 2** | 0  | 0  | 0  | 0  |
|  **Mic 3** | 0  | 0  | 0  | 0  |
|  **Piezo** | 0  | 0  | 0  | 0  |


#####(25 seconds))
|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | 0  | 0  | 0  | 0  |
|  **Mic 2** | 0  | 0  | 0  | 0  |
|  **Mic 3** | 0  | 0  | 0  | 0  |
|  **Piezo** | 0  | 0  | 0  | 0  |


Bad parameters: MFPDB (pretty much all values are equal), ADBB (not much difference between mic-mic and mic-piezo comparisons), 

Notes about parameters: EHSB (differences seem to decrease as the time duration increases - might not be a good metric)
