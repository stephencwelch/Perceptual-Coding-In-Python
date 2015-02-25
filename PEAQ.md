# PEAQ - Perceptual Evaluation of Audio Quality

Documentation by Matthew Cohen and Stephen Welch

###Introduction

PEAQ is a standardized algorithm used for objective measurements of *perceived* audio quality, and is based on generally accepted psychoacoustic principles. The method incorporates models of both the peripheral ear component as well as a cognitive component to account for the processes associated with quality judgments.

Given a processed signal and the time-aligned original signal, concurrent frames of the signals are mapped to a basilar membrane representation, and differences in these transformed frames are analyzed in both time and frequency domain by a cognitive model. The overall goal of this analysis is to obtain a quality measure similar to a Subjective Difference Grade (SDG) acquired from listening tests with human participants. This output is called the Objective Difference Grade (ODG).

The processing steps extract perceptual features, which are used for predicting the quality measure. These intermediate features, called **Model Output Variables (MOVs)**, provide potential insight into different psychoacoustic dimensions. The MOVs are combined together to produce the final score. There are two versions of PEAQ (Basic and Advanced), which make use of different number and type of MOV parameters. The Basic uses 11, whereas the Advanced uses only 5 [1].

The motivation behind investing more time into PEAQ is as follows: other measures and cost functions do not take perceptual aspects into consideration, and are merely waveform/spectrum-based. Both the measurable similarity and the perceptual components are embodied in the MOVs - if these features possess and convey that much information about the overall quality difference between two signals, then perhaps their underlying models and computational processes can be used as more simple, yet potentially powerful, similarity measures/cost functions. This is what brought us here.

Since PEAQ is a standard, the algorithm is licensed and targeted more at telecommunication companies. However, various implementation attempts are floating around the Internet. One commonly mentioned one is by Peter Kabal of the Multimedia Signal Processing lab at McGill University. Kabal did an extensive examination and interpretation of PEAQ, which resulted in a report titled "An Examination and Interpretation of ITU-R BS.1387: Perceptual Evaluation of Audio Quality" and a MATLAB implementation library called PQevalAudio [2]. This code can be found floating around on the Internet (we acquired it through a GitHub account for a CCRMA student). Our analyses and results below made use of this code.

###Model Output Variable (MOV) Overview

The table below lists each of the 11 MOV parameters and provides a brief description of them.

|  **MOV** | **Description**  |
|:---:|:---:|
|  BandwidthRefB | Bandwidth of the reference signal |
|  BandwidthTestB | Bandwidth of the test signal |
|  Total NMRB | Logarithm of the averaged Total Noise-to-Mask Ratio |
|  WinModDiff1B | Windowed averaged difference in modulation (envelopes) between Reference Signal and Test Signal |
|  ADBB | Average Distorted Block (frame), taken as the logarithm of the ratio of the total distortion to the total number of severely distorted frames  |
|  EHSB | Harmonic structure of the error over time  |
|  AvgModDiff1B | Averaged modulation difference  |
|  AvgModDiff2B | Averaged modulation difference with emphasis on introduced modulations and modulation changes where the reference contains little or no modulations  |
|  RmsNoiseLoudB | RMS value of the averaged noise loudness with emphasis on introduced components  |
|  MFPDB | Maximum of the Probability of Detection after low-pass filtering |
|  RelDistFramesB | Relative fraction of frames for which at least one frequency band contains a significant noise component  |

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

The TotalNMRB is not quite invariant over changing time duration, but it appears to keep the same overall structure and trends. It is ***not symmetric*** (i.e. for ref-test ordering, Mic-Piezo does not equal Piezo-Mic values). For Piezo-Mic, the piezo-related values are significantly larger and positive, whereas for Mic-Piezo, the piezo-related values are significantly smaller in magnitude (take on positive and negative values). There is a nice, clear distinction between types, which is ideal for a metric for us.

#####Avg Mod Diff2B (1 second)
|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | 0  | 56.803  | 31.031  | 61.665  |
|  **Mic 2** | 64.328  | 0  | 62.957  | 62.48  |
|  **Mic 3** | 33.092  | 62.443  | 0  | 67.135  |
|  **Piezo** | 88.919  | 73.222  | 83.088  | 0  |


#####Avg Mod Diff2B (10 seconds)
|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | 0  | 59.727  | 26.161  | 54.943  |
|  **Mic 2** | 66.928  | 0  | 65.166  | 57.807  |
|  **Mic 3** | 28.588  | 60.963  | 0  | 56.218  |
|  **Piezo** | 134.88  | 106.39  | 130.05  | 0  |


#####Avg Mod Diff2B (25 seconds)
|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | 0  | 62.312  | 27.392  | 56.145  |
|  **Mic 2** | 67.966  | 0  | 66.779  | 58.944  |
|  **Mic 3** | 28.46  | 61.674  | 0  | 55.913  |
|  **Piezo** | 124.58  | 98.896  | 122.98  | 0  |

There does appear to be a clear distinction between values for case of Piezo-Mic values; however, an asymmetry exists and appears to be non-ideal, in that the Mic-Piezo values are not distinctive. This could make this parameter a non-ideal metric, because we will not always have control over ordering of reference and test signals.

#####Bandwidth RefB (1 second)
|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | 706.83  | 811.67  | 646.52  | 873.04  |
|  **Mic 2** | 692.57  | 728.61  | 615.17  | 772.93  |
|  **Mic 3** | 791.83  | 861.52  | 679.76  | 909.54  |
|  **Piezo** | 543.49  | 615.84  | 499.08  | 697.41  |


#####Bandwidth RefB (10 seconds)
|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | 637.06  | 792.03  | 595.65  | 873.64  |
|  **Mic 2** | 622.64  | 665.84  | 585.14  | 694.13  |
|  **Mic 3** | 692.14  | 768.74  | 626.87  | 866.43  |
|  **Piezo** | 551.62  | 600.03  | 505.31  | 631.73  |


#####Bandwidth RefB (25 seconds)
|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | 657.77  | 787.18  | 601.17  | 866.59  |
|  **Mic 2** | 639.28  | 680.03  | 591.38  | 715.73  |
|  **Mic 3** | 724.93  | 794.60  | 644.65  | 875.24  |
|  **Piezo** | 555.67  | 602.00  | 502.50  | 650.67  |

The BandwidthRefB is also asymmetrical, but not in a bad way. The piezo-related values are noticeably smaller for the Piezo-Mic ordering, and noticeably larger for the Mic-Piezo ordering. Based on the table values, this parameter has the potential to be a decent metric.

Some of the parameters that appear to be bad metric include: 
* MFPDB - pretty much all values are equal
* RelDistFramesB - also mostly all equal values
* ADBB - not much difference between mic-mic and mic-piezo comparisons

Other parameters possess qualities that might make them bad metrics:
* EHSB - differences seem to decrease as the time duration increases, which is not desirable
* RmsNoiseLoudB - not much distinction between mic-mic and mic-piezo comparisons, and is invariant over changing time duration

Certain other parameters could potentially be decent metrics but would need to be looked at further with additional test data. These include:
* AvgModDiff1B / WinModDiff1B - these two parameters produce nearly identical values with each time duration; invariant over time but do not show the most clear distinction

###MOV Experiments

Additional tests and experiments were conducted to explore and better understand the MOV parameters in different contexts, mainly for piezo vs. mic signals, as well as for for transient vs. sustain segments.

Instead of simply analyzing the final output MOV values in a table form, as done above, we wanted to look at time-dependent behaviors and trends, i.e. how the MOV values change over time. One particular thing of interest to us was how these time plots of MOVs behaved in comparison to the signal spectrograms. For example, do certain parameters appear to behave in some consistent, predictable way in the event of transients (vertical striations on spectrograms) or sustain regions? Are there noticeable differences between MOV time plots for mic signals versus for piezo signals? What more can potentially be ascertained from these MOV plots? With these questions in mind, we set out to create plots and visualizations to display this information.

In the end, we decided on three different ways of looking at the data: 

* 1. A grid of MOV/spectrogram plots
* 2. Stacked plots of single spectrogram and MOV curves (all MOV curves in one plot, with different colors for mic-mic and mic-piezo comparisons)
* 3. MOV output value tables for specific input types: signals with only sustain portions, with only transient portions, and with only transient portions and silence removed.

#####1. Grid Plots - MOVs and Spectrograms

The layout for the grid plots is as follows, for a specfic MOV variable: spectrograms (mic1, mic2, mic3, piezo) in first row; then a 4x4 grid of MOV time-plot curves, where the (m,n) entry corresponds to reference signal mic_m and test signal mic_n (4 == piezo). For example, grid entry (2,4) is mic2 - piezo comparison, entry (3,1) is mic3 - mic1, etc.

The variables displayed here are the BandwidthRef and NMR(avg) variables. These are intermediate values that eventually map to final output variables (NRM(avg) maps to TotalNMR). There are plots for both 1 second and 10 seconds of audio. 

#####BandwidthRef (1 second)
![Image](https://raw.githubusercontent.com/stephencwelch/Perceptual-Coding-In-Python/master/data/PEAQ_data/MOV_Spectrogram_Grid_Plots/1_Second/BW_Ref.jpg)

#####BandwidthRef (10 seconds)
![Image](https://raw.githubusercontent.com/stephencwelch/Perceptual-Coding-In-Python/master/data/PEAQ_data/MOV_Spectrogram_Grid_Plots/10_Seconds/BW_Ref.jpg)

#####NMR(avg) (1 second)
![Image](https://raw.githubusercontent.com/stephencwelch/Perceptual-Coding-In-Python/master/data/PEAQ_data/MOV_Spectrogram_Grid_Plots/1_Second/NMR_avg.jpg)

#####NMR(avg) (10 seconds)
![Image](https://raw.githubusercontent.com/stephencwelch/Perceptual-Coding-In-Python/master/data/PEAQ_data/MOV_Spectrogram_Grid_Plots/10_Seconds/NMR_avg.jpg)

The size and complexity of these plots make it a little difficult to extract meaningful results or information from, though it does appear there may be a relationship between strong vertical striations in the spectrogram and peaks/dips in some MOV curves.

#####2. Stacked Plots - MOVs and Spectrogram

The layout for the stacked plots is as follows, for a specfic MOV variable: the first row is a single spectrogram (for the mic 1 signal of the specified duration); the second row has a single plot with each MOV time-plot curve for the current MOV variable, with two colors depicting the type of comparison formed (either mic-to-mic or mic-to-piezo, with no self comparisons plotted). 

Like with the grid plots, the variables displayed here are the BandwidthRef and NMR(avg) variables. Again, there are plots for both 1 second and 10 seconds of audio. 

#####BandwidthRef (1 second)
![Image](https://raw.githubusercontent.com/stephencwelch/Perceptual-Coding-In-Python/master/data/PEAQ_data/MOV_Spectrogram_Stacked_Plots/1_Second_2_Transparency/BW_Ref.jpg)

#####BandwidthRef (10 seconds)
![Image](https://raw.githubusercontent.com/stephencwelch/Perceptual-Coding-In-Python/master/data/PEAQ_data/MOV_Spectrogram_Stacked_Plots/10_Seconds_2_Transparency/BW_Ref.jpg)

#####NMR(avg) (1 second)
![Image](https://raw.githubusercontent.com/stephencwelch/Perceptual-Coding-In-Python/master/data/PEAQ_data/MOV_Spectrogram_Stacked_Plots/1_Second_2_Transparency/NMR_avg.jpg)

#####NMR(avg) (10 seconds)
![Image](https://raw.githubusercontent.com/stephencwelch/Perceptual-Coding-In-Python/master/data/PEAQ_data/MOV_Spectrogram_Stacked_Plots/10_Seconds_2_Transparency/NMR_avg.jpg)

Again, like with the grid plots, the complexity of these plots make it a little difficult to extract meaningful results or information from.

#####3. Tables - Sustain vs. Transients

Part of these experiments involved analyzing how the MOV values vary between sustain and transient portions of signal. To do this, we first had to create signals with only sustain portion and others containing only transients. The procedure and data types are explained more in 'exports/transientsAndSustains/README.md,' but the overview is that a heuristic wavelet-based technique was used to divide a signal into transient and sustain portions; then, X samples of transients were removed to produce the sustain signals (here, X values of 256, 512, 1024, and 2048 were used). The removed portions constituted the transient signals; additionally, silence portions between transients were removed to also produce transients-with-no-silence signals. For each value of X, MOV output tables were produced by comparing signals of the same type; for example, the microphone and piezo signals with only sustain portions produced one table, like are shown in the Testing section above, etc. These tables were computed for each MOV parameter.

Shown below are the tables for the two parameters that we found to be most promising: BandwidthRef and TotalNMRB.

####512 Sample Transients

#####TotalNMRB (Sustain only)
|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | -128.55  | -1.56  | -5.53  | -0.69  |
|  **Mic 2** | 3.26  | -127.23  | 2.69  | 0.54  |
|  **Mic 3** | -4.89  | -1.67  | -128.33  | -0.73  |
|  **Piezo** | 12.63  | 7.14  | 11.87 | -124.57  |

#####TotalNMRB (Transients only)
|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | -118.80  | -9.94 | -14.19  | -8.91  |
|  **Mic 2** | -2.42  | -118.55  | -3.69  | -8.38  |
|  **Mic 3** | -12.61  | -9.94  | -118.76  | -8.90  |
|  **Piezo** | 8.18  | 1.12  | 6.76  | -118.28  |

#####TotalNMRB (Transients only, no silence)
|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | -147.91  | -2.74 | -7.08  | -1.51  |
|  **Mic 2** | 4.61  | -143.10  | 3.29  | -1.14  |
|  **Mic 3** | -5.48  | -2.79  | -147.95  | -1.51  |
|  **Piezo** | 15.88  | 8.51  | 14.35  | -133.65  |

#####Bandwidth RefB (Sustain only)
|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | 649.38  | 784.08  | 601.92  | 863.01  |
|  **Mic 2** | 631.41  | 670.73  | 589.57  | 709.14  |
|  **Mic 3** | 710.89  | 781.73  | 640.67  | 872.03  |
|  **Piezo** | 546.45  | 590.95  | 496.25  | 632.63  |

#####Bandwidth RefB (Transients only)
|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | 875.39  | 889.08  | 854.41  | 897.00 |
|  **Mic 2** | 866.01  | 874.68  | 864.40  | 883.39  |
|  **Mic 3** | 895.42  | 903.76  | 862.72  | 906.98  |
|  **Piezo** | 884.84  | 872.62  | 902.65  | 872.41  |

#####Bandwidth RefB (Transients only, no silence)
|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | 697.76  | 782.92  | 563.86  | 840.34  |
|  **Mic 2** | 622.53  | 696.38  | 504.47  | 751.52  |
|  **Mic 3** | 834.94  | 881.44  | 573.60  | 889.74  |
|  **Piezo** | 441.73  | 495.00  | 371.00  | 583.04  |

####2048 Sample Transients

#####TotalNMRB (Sustain only)
|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | -128.37  | -1.56  | -5.51  | -0.69  |
|  **Mic 2** | 3.24  | -127.08  | 2.65  | 0.51  |
|  **Mic 3** | -4.86  | -1.67  | -128.15  | -0.72  |
|  **Piezo** | 12.57  | 7.10  | 11.80 | -124.43  |

#####TotalNMRB (Transients only)
|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | -119.01  | -7.72 | -12.92  | -6.87  |
|  **Mic 2** | -5.73  | -118.92  | -6.26  | -6.41  |
|  **Mic 3** | -12.21  | -7.84  | -118.99  | -7.06  |
|  **Piezo** | 3.46  | 0.07  | 2.64  | -118.68  |

#####TotalNMRB (Transients only, no silence)
|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | -135.79  | -1.45 | -6.60  | -0.74  |
|  **Mic 2** | 0.81  | -135.15  | 0.25  | -0.08  |
|  **Mic 3** | -5.85  | -1.61  | -136.03  | -0.95  |
|  **Piezo** | 10.33  | 6.72  | 9.52  | -129.76  |

#####Bandwidth RefB (Sustain only)
|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | 643.48  | 777.89  | 598.12  | 857.30  |
|  **Mic 2** | 627.93  | 665.45  | 589.22  | 704.70  |
|  **Mic 3** | 703.31  | 774.54  | 634.19  | 864.38  |
|  **Piezo** | 540.71  | 588.30  | 497.91  | 627.79  |

#####Bandwidth RefB (Transients only)
|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | 851.60  | 858.99  | 822.53  | 862.72  |
|  **Mic 2** | 851.65  | 852.48  | 829.51  | 857.67  |
|  **Mic 3** | 884.45  | 884.30  | 838.71  | 888.77  |
|  **Piezo** | 843.84  | 843.81  | 862.24  | 848.22  |

#####Bandwidth RefB (Transients only, no silence)
|   | **Mic 1**  |  **Mic 2** | **Mic 3**  | **Piezo**  |
|:---:|:---:|:---:|:---:|:---:|
|  **Mic 1** | 728.63  | 748.04  | 601.20  | 764.07  |
|  **Mic 2** | 714.62  | 724.74  | 599.24  | 742.52  |
|  **Mic 3** | 854.75  | 853.29  | 652.67  | 869.42  |
|  **Piezo** | 641.29  | 642.68  | 535.11  | 665.06  |

These tables do little to provide any additional information about these parameters outside of the conclusions that were already reached from above results. All of the results point towards TotalNMRB and BandwidthRefB as being potentially useful MOVs/measures for future use.

######***References***
[1] T. Thiede, et. al., "PEAQ - The ITU Standard for Objective Measurement of Perceived Audio Quality", J. Audio Eng. Soc., Vol. 48, No 1/2, January/February 2000.

[2] P. Kabal, "An Examination and Interpretation of ITU-R BS.1387:
 Perceptual Evaluation of Audio Quality", TSP Lab Technical Report,
 Dept. Electrical & Computer Engineering, McGill University, May 2002. 