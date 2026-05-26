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
# Apply the mask to filter the data
freq = freq[mask]
Z_real = Z_real[mask]
Z_imag = Z_imag[mask]

def randles_impedance(freq, RS, RCT, CDL, sigma):
    # Convert frequency to angular frequency
    omega = 2 * np.pi * freq
    
    # Warburg impedance
    Z_warburg = (sigma / np.sqrt(omega)) * (1 - 1j)
    
    # Parallel combination of RCT and CDL
    Z_parallel = RCT / (1 + 1j * omega * CDL * RCT)
    
    # Total impedance
    Z_total = RS + Z_parallel + Z_warburg
    
    return Z_total


# Initial parameter guesses based on looking at the plot
RS_guess = 0.0045
RCT_guess = 0.0020
CDL_guess = 0.5
sigma_guess = 0.0009

# Calculate simulated impedance
Z_sim = randles_impedance(freq, RS_guess, RCT_guess, CDL_guess, sigma_guess)

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
def randles_flat(freq, RS, RCT, CDL, sigma):
    Z = randles_impedance(freq, RS, RCT, CDL, sigma)
    return np.concatenate([Z.real, -Z.imag])

p0 = [RS_guess, RCT_guess, CDL_guess, sigma_guess]

# Run the fit
params, _ = curve_fit(randles_flat, freq, Z_measured, p0=p0,bounds = ([0, 0, 0, 0], [np.inf, np.inf, np.inf, np.inf]), maxfev=100000)

# Extract fitted values
RS_fit, RCT_fit, CDL_fit, sigma_fit = params

# Print results
print(f"RS  = {RS_fit:.6f} Ohms")
print(f"RCT = {RCT_fit:.6f} Ohms")
print(f"CDL = {CDL_fit:.6f} F")
print(f"sigma = {sigma_fit:.6f}")

randles_fit = randles_impedance(freq, RS_fit, RCT_fit, CDL_fit, sigma_fit)
plt.plot(Z_real, Z_imag, 'o-', label='Experimental Data')
plt.plot(randles_fit.real, -randles_fit.imag, 'r--', linewidth = 2, label='Fitted Randles Model')
plt.xlabel('Real Part of Z')
plt.ylabel('Imaginary Part of Z')
plt.title('Nyquist Plot of EIS Data with Fitted Randles Model')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.legend()
plt.show()