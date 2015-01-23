# Perceptual Coding In Python

Created by Stephen Welch and Matthew Cohen

###Research Question: How do we measure how similar two signals sound?

###Introduction

Quantifying human perceptions of physical phenomena is a complex task that covers various disciplines. Speech and image recognition are relatively mature fields that have seen particular progress in the last few years through training deep neural networks on large labeled datasets. Notably for both speech and image recognition, hand-engineered features such as SIFT and MFCC are quickly being replaced by learned features. It is difficult to say if the deep learning paradigm will replace, augment, or provide more insight into other relevant fields concerned with quantifying the perception of sounds. We believe relevant work can be divided broadly into the following areas: Audio Compression and Perceptual Coding, Music Information Retrieval, Machine Learning, and Measures of Audio Quality.

###Audio Compression
	
Audio compression technologies have been incredibly successful at achieving excellent quality at high compression rates. Mp3 and AAC algorithms are at a high-level described by an international standard, but in implementation are largely heuristics driven. There are a number of open source implementation available, but the best and most used implementations are patented and proprietary. It seems like “good enough” compression solutions we’re largely reached in the 1990s, and not much has changed since then. 

###Machine Learning

Machine learning, specifically through deep neural networks, offers excellent performance on speech recognition in noisy environments and other audio classification tasks. In this framework, expert knowledge is spent on setting up clever training and data structures, rather than hand engineering features. Similar to audio compression, the progress in this area made by machine learning can be largely heuristic at times, and tends to produce best results when developed by an expert in the field or sub-field.

###Psychoacoustics/Perceptual Coding
	
Psychoacoustics and perceptual processing has received focus by researchers, telecommunication companies, and other groups hoping to develop algorithms for objectively measuring perceived audio quality. These algorithms simulate perceptual properties of the human ear and apply computer models of the auditory signal processing in order to estimate the perceived similarity between two audio signals. Some examples of these algorithms include PEAQ (Perceptual Evaluation of Audio Quality), a standardized algorithm; PEMO-Q (PErception MOdel-based Quality estimation); PESQ (Perceptual Evaluation of Speech Quality); and EAQUAL (Evaluation of Audio Quality). 

These algorithms incorporate strong understanding of the perceptual processes involved in hearing and auditory processing, and make use of in-depth DSP stages. The downside with many of these algorithms is that they are patented and licensed, mostly to companies due to the high costs for licenses. Over the years, students and academia professionals have attempted to implement some of these algorithms for open-source usage; however, the precision and accuracy of these seem variable, and available implementations are scarce. EAQUAL’s source code is made available to the public, but has not been extensively tested.

