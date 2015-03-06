function x = PQgetData (WAV, i, N)
% Get data from internal buffer or file
% i - file position
% N - number of samples
% x - output data (scaled to the range -32768 to +32767)

% Only two files can be "active" at a time.
% N = 0 resets the buffer


% P. Kabal $Revision: 1.1 $  $Date: 2003/12/07 13:34:10 $

persistent Buff

iB = WAV.iB + 1;
if (N == 0)
    Buff(iB).N = 20 * 1024;     % Fixed size
    Buff(iB).x = PQ_ReadWAV (WAV, i, Buff(iB).N);
    Buff(iB).i = i;
end

if (N > Buff(iB).N)
    error ('>>> PQgetData: Request exceeds buffer size');
end

% Check if requested data is not already in the buffer
is = i - Buff(iB).i;
if (is < 0 | is + N - 1 > Buff(iB).N - 1)
    Buff(iB).x = PQ_ReadWAV (WAV, i, Buff(iB).N);
    Buff(iB).i = i;
end

% Copy the data
Nchan = WAV.Nchan;
is = i - Buff(iB).i;
x = Buff(iB).x(1:Nchan,is+1:is+N-1+1);

%------
function x = PQ_ReadWAV (WAV, i, N)
% This function considers the data to extended with zeros before and
% after the data in the file. If the starting offset i is negative,
% zeros are filled in before the data starts at offset 0. If the request
% extends beyond the end of data in the file, zeros are appended.

Amax = 32768;
Nchan = WAV.Nchan;

x = zeros (Nchan, N);

Nz = 0;
if (i < 0)
    Nz = min (-i, N);
    i = i + Nz;
end

Ns = min (N - Nz, WAV.Nframe - i);
if (i >= 0 & Ns > 0)
    x(1:Nchan,Nz+1:Nz+Ns-1+1) = Amax * (wavread (WAV.Fname, [i+1 i+Ns-1+1]))';
end
