function WAV = PQwavFilePar (File)
% Print a WAVE file header, pick up the file parameters

% P. Kabal $Revision: 1.1 $  $Date: 2003/12/07 13:34:11 $

persistent iB

if (isempty (iB))
    iB = 0;
else
    iB = mod (iB + 1, 2);   % Only two files can be "active" at a time
end

[size WAV.Fs Nbit] = wavread (File, 'size');
WAV.Fname = File;
WAV.Nframe = size(1);
WAV.Nchan = size(2);
WAV.iB = iB;   % Buffer number

% Initialize the buffer
PQgetData (WAV, 0, 0);

fprintf (' WAVE file: %s\n', File);
if (WAV.Nchan == 1)
    fprintf ('   Number of samples : %d (%.4g s)\n', WAV.Nframe, WAV.Nframe / WAV.Fs);
else
    fprintf ('   Number of frames  : %d (%.4g s)\n', WAV.Nframe, WAV.Nframe / WAV.Fs);
end
fprintf ('   Sampling frequency: %g\n', WAV.Fs);
fprintf ('   Number of channels: %d (%d-bit integer)\n', WAV.Nchan, Nbit);
