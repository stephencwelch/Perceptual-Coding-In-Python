##Perceptual Coding Resources

##PEAQ MATLAB Implementation (on GitHub). 
Some time will need to be spent testing the code and seeing if it seems usable, accurate, and bug-free. The opensource code can be found here: https://github.com/jorgehatccrma/AudioMorphing/tree/master/Testing/PQevalAudio-v1r0

##EAQUAL 
Stands for Evaluation of Audio Quality; similar to PEAQ. 
Information about it, as well as source code, can be found at: http://kb.mpegforum.org/wiki/EAQUAL

###Description 
An objective audio quality measurement tool, used for coded/ decoded audio files. Currently the code is based on the ITU-R recommendation BS.1387. EAQUAL will not supersede listening tests, but can be a useful tool to support listening tests, categorize different coding algorithms and find bugs in algorithms. The more input files are taken for the analysis, the better the results of EAQUAL will fit the reality. 

###How To Use 
To use EAQUAL, you have to provide the reference file, which is the original PCM data (prefereably 16bit, 48kHz), and the test file, which is the coded and decoded audio file and has the *same* audio format. Invalid file formats are samplerates < 44100Hz or more than two channels. The most interesting output value of EAQUAL is the ODG (Objective Difference Grade). An ODG of –4 means a very annoying disturbance, while an ODG of 0 means that there is no perceptible difference.
Usage: EAQUAL [-options] -fref reference_file_path -ftest test_file_path

###Output: 
ODG Objective Difference Grade, a measure of quality comparable to the Subjective Difference Grade (SDG), which is calculated as the difference between the quality rating of the reference and the test signal. The quality ratings are measured with the five point scale defined in ITU-R BS.1116 and thus the SDG and ODG have a range of [-4;0] where –4 stands for very annoying difference and 0 stands for imperceptible difference between reference and test signal.
	

##ITU Standard
Peak Technology is recommended by ITU-R Rec. Bs. 1387: 
https://drive.google.com/file/d/0B3uG8y1SBWuQbWJhZXMycm9Dd0U/view?usp=sharing

##Peakb
Peakb is a c-implementation of PEAQ for educational use - it "accomplishes the same functions in a limited manner, and has not been validated with ITU data."
http://sourceforge.net/projects/peaqb/?source=typ_redirect
