%% Test 1 - Sinusoid of single frequency (1kHz)

% Define test signal parameters
fs = 48000;
f = 1000;
num_samps = 2048;
t = 0:1/fs:num_samps/fs;
A = 1;
y = A*sin(2*pi*f*t);

nfft = 2048;
Y = fft(y,nfft);
Y_sub = Y(1:nfft/2);
Y_abs = abs(Y_sub);
Y_abs = Y_abs';

%plot(Y_abs)

% Construct the weight matrix
nfilts = 109;

wts = fft2barkmx(nfft, fs, nfilts);

figure
imshow(flipud(wts(:,1:size(wts,2)/2)))

% Apply Bark domain weights matrix to test signal
[nfreqs,nframes] = size(Y_abs);
wts_short = wts(:, 1:nfreqs);

bark_spectrum = wts_short * (Y_abs.^2);

figure
plot(bark_spectrum./max(bark_spectrum),'r')
hold on
plot(Y_abs./max(Y_abs),'b')
% figure
% semilogx(bark_spectrum./max(bark_spectrum),'r')
% hold on
% semilogx(Y_abs./max(Y_abs),'b')

% figure
% semilogx(bark_spectrum)

% Now, attempt to map from Bark domain back to Fourier freq. domain

% Just transpose, fix up 
ww = wts_short'*wts_short;
iwts = wts_short'./(repmat(max(mean(diag(ww))/100, sum(ww))',1,nfilts));

Y_hat = iwts * bark_spectrum;

% figure
% semilogx(Y_abs,'b')
% hold on
% semilogx(Y_hat,'r')
% 
% figure
% semilogy(Y_abs,'b')
% hold on
% semilogy(Y_hat,'r')

figure
plot(Y_abs./max(Y_abs),'b')
hold on
plot(Y_hat./max(Y_hat),'r')

%% Test 2 - Sinusoid of Two Frequencies (500Hz and 10kHz)

% Define test signal parameters
f1 = 500;
f2 = 10000;
y2 = A*sin(2*pi*f1*t) + A*sin(2*pi*f2*t);

Y2 = fft(y2,nfft);
Y2_sub = Y2(1:nfft/2);
Y2_abs = abs(Y2_sub);
Y2_abs = Y2_abs';

plot(Y2_abs)

bark_spectrum2 = wts_short * (Y2_abs.^2);

figure
plot(bark_spectrum2./max(bark_spectrum2),'r')
hold on
plot(Y2_abs./max(Y2_abs),'b')
% figure
% semilogx(bark_spectrum./max(bark_spectrum),'r')
% hold on
% semilogx(Y_abs./max(Y_abs),'b')

% figure
% semilogx(bark_spectrum)

% Now, attempt to map from Bark domain back to Fourier freq. domain

% Just transpose, fix up 

Y2_hat = iwts * bark_spectrum2;

% figure
% semilogx(Y_abs,'b')
% hold on
% semilogx(Y_hat,'r')
% 
% figure
% semilogy(Y_abs,'b')
% hold on
% semilogy(Y_hat,'r')

figure
plot(Y2_abs./max(Y2_abs),'b')
hold on
plot(Y2_hat./max(Y2_hat),'r')

