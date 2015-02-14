##Transients and Sustains

Stephen Welch, February 14, 2015

This directory contains audio exported from the ipython notebook Transient Vs. Sustain.ipynb. Included are piezo and 3 microphone signals for roughly 20 seconds of audio, divided into transient and sustain portions, using a heuristic, wavelet-based technique outlined in the notebook. 

The data is organized by the assumed transient duration in samples. Switching is smooted with a simgoid function. Within each directory exists 3 types of files: 

###Sustain
Audio with X samples of transients removed. 

###Transient
The missing samples of of the sustain file, preserved in time.

###Transient No Silence
All the transients, with silences between them removed, may be helpful in analysis. 