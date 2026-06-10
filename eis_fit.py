import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

data = loadmat('data/SampleEISData.mat')

# Access the nested struct
eis = data['SampleEISData']

# Extract the arrays and filtering inductance data


    
freq = eis['Frequency'][0, 0].flatten()
Z_real = eis['Re'][0, 0].flatten()
Z_imag = eis['mIm'][0, 0].flatten()

mask = Z_imag >= 0

freq = freq[mask]
Z_real = Z_real[mask]
Z_imag = Z_imag[mask]

def randles_impedance(freq, RS, RCT, Q, A_w, n_w, alp):
    
    omega = 2 * np.pi * freq
    
    # Warburg impedance
    Z_warburg = A_w / (1j * omega)**n_w    
    
    Z_series = Z_warburg + RCT
    
    Z_cpe = 1 / (((1j * omega)**alp) * Q)

    Z_parallel = (Z_series * Z_cpe) / (Z_series + Z_cpe)


    Z_total = RS + Z_parallel
    
    return Z_total


# Initial parameter guesses based on looking at the plot
RS_guess = 0.0049
RCT_guess = 0.00144
Q_guess = 2.0
alpha_guess = 0.8
nw_guess = 0.5
aw_guess = 0.01

# Calculate simulated impedance
Z_sim = randles_impedance(freq, RS_guess, RCT_guess, Q_guess, aw_guess, nw_guess, alpha_guess)

plt.figure(figsize=(8, 6))
plt.plot(Z_real, Z_imag, 'o-', label='Experimental Data')
plt.plot(Z_sim.real, -Z_sim.imag, 'r--', linewidth = 2, label = 'Randles Model Fit')
plt.xlabel('Real Part of Z')
plt.ylabel('Imaginary Part of Z')
plt.title('Nyquist Plot of EIS Data')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.legend()
plt.show()

Z_measured = np.concatenate([Z_real, Z_imag])

# Wrapper function that returns stacked real+imaginary output
def randles_flat(freq, RS, RCT, Q, aw, nw, alpha):
    Z = randles_impedance(freq, RS, RCT, Q, aw, nw, alpha)
    return np.concatenate([Z.real, -Z.imag])

p0 = [RS_guess, RCT_guess, Q_guess, aw_guess, nw_guess, alpha_guess]

# Run the fit
params, _ = curve_fit(randles_flat, freq, Z_measured, p0=p0,bounds = ([0, 0, 0, 0, 0.3, 0.5],
 [0.01, 0.01, 10, 10, 0.7, 1.0]), maxfev=100000)

# Extract fitted values
RS_fit, RCT_fit, Q_fit, aw_fit, nw_fit, alpha_fit = params

# Print results
print(f"RS  = {RS_fit:.6f} Ohms")
print(f"RCT = {RCT_fit:.6f} Ohms")
print(f"Q = {Q_fit:.6f} F")
print(f"Aw = {aw_fit:.6f}")
print(f"Nw = {nw_fit:.6f}")
print(f"Alpha = {alpha_fit:.6f}")

randles_fit = randles_impedance(freq, RS_fit, RCT_fit, Q_fit, aw_fit, nw_fit, alpha_fit)
plt.plot(Z_real, Z_imag, 'o-', label='Experimental Data')
plt.plot(randles_fit.real, -randles_fit.imag, 'r--', linewidth = 2, label='Fitted Randles Model')
plt.xlabel('Real Part of Z')
plt.ylabel('Imaginary Part of Z')
plt.title('Nyquist Plot of EIS Data with Fitted Randles Model')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.legend()
plt.show()

