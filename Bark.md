# Bark Scale (Domain) for Perceptual Audio Evaluation and Filter Design

Documentation by Matthew Cohen and Stephen Welch

###Introduction

The Bark scale is a psychoacoustical scale used in audio applications that aims to employ more perceptually accurate representations of audio and speech signals. Traditionally, the Bark scale ranges from 1 to 24 Barks, corresponding to the first 24 critical bands of hearing. Critical bands are related to the bandwidth of auditory filters that the cochlea in the inner ear create; within a critical band, audio frequencies will interfere such that the perception of one tone could be masked by another tone. The Bark scale critical bands can be expressed by center frequencies and lower/upper cut-off frequencies, though the bandwidth of a critical band at a frequency can be used and is as important as precisely measured center and cut-off frequencies. The conversion from frequencies in Hertz to Barks involves nonlinear trigonometric transformations.

The importance of the Bark domain (we will refer to the Bark scale as the Bark domain, since we are treating it as a mathematical transform domain), and other related scales such as the Mel scale, is in how it models how the cochlea processes auditory signals. Mapping to the Bark domain provides a more perceptual representation than the Fourier (Hz) domain; this has allowed for both better evaluation of quality of signals through perceptual comparison of two signals. The scale was encountered when we delved in the Perceptual Evaluation of Audio Quality (PEAQ) standardized algorithm. Many of the Model Output Variables (MOVs), which represent important attributes of the signal and are used to compare signals, are computed from the Bark-domain representation of the signals. 

The intuition acquired from the PEAQ exploration was that the Bark domain could potentially be used as a metric or objective function in a learning algorithm, such as a Neural Network, or as a means of designing perceptual audio filters for improving audio quality. We decided to explore the Bark domain more to see how useful it could be as a tool for enhancing audio quality through filter design. The following sections detail this exploration process and what was learned from it.

###Bark Domain and Filter Design


###