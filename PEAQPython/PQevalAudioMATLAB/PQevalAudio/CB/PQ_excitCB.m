%--------------------
function [EbN, Es] = PQ_excitCB (X2)

persistent W2 EIN

NF = 2048;
Version = 'Basic';
if (isempty (W2))
    Fs = 48000;
    f = linspace (0, Fs/2, NF/2+1);
    W2 = PQWOME (f);
    [Nc, fc] = PQCB (Version);
    EIN = PQIntNoise (fc);
end

% Allocate storage
XwN2 = zeros (1, NF/2+1);

% Outer and middle ear filtering
Xw2(1,:) = W2 .* X2(1,1:NF/2+1);
Xw2(2,:) = W2 .* X2(2,1:NF/2+1);

% Form the difference magnitude signal
for (k = 0:NF/2)
    XwN2(k+1) = (Xw2(1,k+1) - 2 * sqrt (Xw2(1,k+1) * Xw2(2,k+1)) ...
               + Xw2(2,k+1));
end

% Group into partial critical bands
Eb(1,:) = PQgroupCB (Xw2(1,:), Version);
Eb(2,:) = PQgroupCB (Xw2(2,:), Version);
EbN     = PQgroupCB (XwN2, Version);

% Add the internal noise term => "Pitch patterns"
E(1,:) = Eb(1,:) + EIN;
E(2,:) = Eb(2,:) + EIN;

% Critical band spreading => "Unsmeared excitation patterns"
Es(1,:) = PQspreadCB (E(1,:), Version);
Es(2,:) = PQspreadCB (E(2,:), Version);