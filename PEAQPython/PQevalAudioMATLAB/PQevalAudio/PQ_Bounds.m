function [StartS, Fstart, Fend] = PQ_Bounds (WAV, Nchan, StartS, EndS, PQopt)

PQ_NF = 2048;
PQ_NADV = (PQ_NF / 2);

if (isempty (StartS))
    StartS(1) = 0;
    StartS(2) = 0;
elseif (length (StartS) == 1)
    StartS(2) = StartS(1);
end
Ns = WAV(1).Nframe;

% Data boundaries (determined from the reference file)
if (PQopt.DataBounds)
    Lim = PQdataBoundary (WAV(1), Nchan, StartS(1), Ns);
    fprintf ('PEAQ Data Boundaries: %ld (%.3f s) - %ld (%.3f s)\n', ...
             Lim(1), Lim(1)/WAV(1).Fs, Lim(2), Lim(2)/WAV(1).Fs);
else
    Lim = [Starts(1), StartS(1) + Ns - 1];
end
         
% Start frame number
Fstart = floor ((Lim(1) - StartS(1)) / PQ_NADV);

% End frame number
Fend = floor ((Lim(2) - StartS(1) + 1 - PQopt.EndMin) / PQ_NADV);