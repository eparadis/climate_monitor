
def vpd_psi(temp_F, rh_pct):
  from math import log, exp
  A = -1.0440397e4
  B = -11.29465
  C = -2.7022355e-2
  D = 1.289036e-5
  E = -2.4780681e-9
  F = 6.5459673
  T = temp_F + 459.67
  vpsat_psi = exp( A/T + B + C * T + D * T * T + E * T * T * T + F * log(T))
  vpd_psi = vpsat_psi * (1 - rh_pct / 100.0)
  return vpd_psi

def vpd_kpa(temp_F, rh_pct):
  return vpd_psi(temp_F, rh_pct) * 6.89476

