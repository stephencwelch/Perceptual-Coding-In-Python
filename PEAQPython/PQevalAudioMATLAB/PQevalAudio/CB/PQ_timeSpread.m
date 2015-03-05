function [Ehs, Ef] = PQ_timeSpread (Es, Ef)
%% Seperate version added for testing for python comparison - SW.

persistent Nc a b

if (isempty (Nc))
    [Nc, fc] = PQCB ('Basic');
    Fs = 48000;
    NF = 2048;
    Nadv = NF / 2;
    Fss = Fs / Nadv;
    t100 = 0.030;
    tmin = 0.008;
    [a, b] = PQtConst (t100, tmin, fc, Fss);
end

% Allocate storage
Ehs = zeros (1, Nc);

% Time domain smoothing
for (m = 0:Nc-1)
    Ef(m+1) = a(m+1) * Ef(m+1) + b(m+1) * Es(m+1);
    Ehs(m+1) = max(Ef(m+1), Es(m+1));
end
