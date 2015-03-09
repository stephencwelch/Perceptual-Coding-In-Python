% Globals (to save on copying in/out of functions)
global MOVC PQopt

% Analysis parameters
NF = 2048;
Nadv = NF / 2;
Version = 'Basic';

% Options
PQopt.ClipMOV = 0;
PQopt.PCinit = 0;
PQopt.PDfactor = 1;
PQopt.Ni = 1;
PQopt.DelayOverlap = 1;
PQopt.DataBounds = 1;
PQopt.EndMin = NF / 2;

addpath ('CB', 'MOV', 'Misc', 'Patt');

Fref = 'timeAligned_mic1_10sec.wav';
Ftest = 'timeAligned_piezo_10sec.wav';

% Get the number of samples and channels for each file
WAV(1) = PQwavFilePar (Fref);
WAV(2) = PQwavFilePar (Ftest);

StartS = [0,0];
EndS = [];

% Data boundaries
Nchan = WAV(1).Nchan;
[StartS, Fstart, Fend] = PQ_Bounds (WAV, Nchan, StartS, EndS, PQopt);

% Number of PEAQ frames
Np = Fend - Fstart + 1;
if (PQopt.Ni < 0)
    PQopt.Ni = ceil (Np / abs(PQopt.Ni));
end

% Initialize the MOV structure
MOVC = PQ_InitMOVC (Nchan, Np);

% Initialize the filter memory
Nc = PQCB (Version);
for (j = 0:Nchan-1)
    Fmem(j+1) = PQinitFMem (Nc, PQopt.PCinit);
end

is = 0;
% for (i = -Fstart:Np-1)

is = 0;
for (i = 0:5) %-Fstart:Np-1)

    % Read a frame of data
    xR = PQgetData (WAV(1), StartS(1) + is, NF);    % Reference file
    xT = PQgetData (WAV(2), StartS(2) + is, NF);    % Test file
    is = is + Nadv;

    % Process a frame
    for (j = 0:Nchan-1)
        [MOVI(j+1), Fmem(j+1)] = PQeval (xR(j+1,:), xT(j+1,:), Fmem(j+1));
    end

    if (i >= 0)
        % Move the MOV precursors into a new structure
        PQframeMOV (i, MOVI);   % Output is in global MOVC

        % Print the MOV precursors
        if (PQopt.Ni ~= 0 & mod (i, PQopt.Ni) == 0)
            PQprtMOVCi (Nchan, i, MOVC);
        end
    end
end

