import numpy as np
from scipy.io import loadmat

data = loadmat('data/SampleEISData.mat')

# Access the nested struct
eis = data['SampleEISData']

# Extract the arrays
freq = eis['Frequency'][0, 0].flatten()
Z_real = eis['Re'][0, 0].flatten()
Z_imag = eis['mIm'][0, 0].flatten()

# Print to verify
print("Frequencies:", freq)
print("Real Z:", Z_real)
print("Imaginary Z:", Z_imag)

