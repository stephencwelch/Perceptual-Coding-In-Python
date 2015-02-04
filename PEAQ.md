# PEAQ - Perceptual Evaluation of Audio Quality

Documentation by Matthew Cohen and Stephen Welch

###Introduction

PEAQ is a standardized algorithm used for objective measurements of *perceived* audio quality, and is based on generally accepted psychoacoustic principles. The method incorporates models of both the peripheral ear component as well as a cognitive component to account for the processes associated with quality judgments.

Given a processed signal and the time-aligned original signal, concurrent frames of the signals are mapped to a basilar membrane representation, and differences in these transformed frames are analyzed in both time and frequency domain by a cognitive model. The overall goal of this analysis is to obtain a quality measure similar to a Subjective Difference Grade (SDG) acquired from listening tests with human participants. This output is called the Objective Difference Grade (ODG).

The processing steps extract perceptual features, which are used for predicting the quality measure. These intermediate features, called **Model Output Variables (MOVs)**, provide potential insight into different psychoacoustic dimensions. The MOVs are combined together to produce the final score. There are two versions of PEAQ (Basic and Advanced), which make use of different number and type of MOV parameters. The Basic uses 11, whereas the Advanced uses only 5.

The motivation behind investing more time into PEAQ is as follows: other measures and cost functions do not take perceptual aspects into consideration, and are merely waveform/spectrum-based. Both the measurable similarity and the perceptual components are embodied in the MOVs - if these features possess and convey that much information about the overall quality difference between two signals, then perhaps their underlying models and computational processes can be used as more simple, yet potentially powerful, similarity measures/cost functions. This is what brought us here.

Since PEAQ is a standard, the algorithm is licensed and targeted more at telecommunication companies. However, various implementation attempts are floating around the Internet. One commonly mentioned one is by Peter Kabal of the Multimedia Signal Processing lab at McGill University. Kabal did an extensive examination and interpretation of PEAQ, which resulted in a report titled "An Examination and Interpretation of ITU-R BS.1387: Perceptual Evaluation of Audio Quality" and a MATLAB implementation library called PQevalAudio. This code can be found floating around on the Internet (we acquired it through a GitHub account for a CCRMA student). Our analyses and results below made use of this code.

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

