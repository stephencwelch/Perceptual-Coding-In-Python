function MOVC = PQ_InitMOVC (Nchan, Np)
MOVC.MDiff.Mt1B = zeros (Nchan, Np);
MOVC.MDiff.Mt2B = zeros (Nchan, Np);
MOVC.MDiff.Wt   = zeros (Nchan, Np);

MOVC.NLoud.NL   = zeros (Nchan, Np);

MOVC.Loud.NRef  = zeros (Nchan, Np);
MOVC.Loud.NTest = zeros (Nchan, Np);

MOVC.BW.BWRef  = zeros (Nchan, Np);
MOVC.BW.BWTest = zeros (Nchan, Np);

MOVC.NMR.NMRavg = zeros (Nchan, Np);
MOVC.NMR.NMRmax = zeros (Nchan, Np);

MOVC.PD.Pc = zeros (1, Np);
MOVC.PD.Qc = zeros (1, Np);

MOVC.EHS.EHS = zeros (Nchan, Np);
