#!/usr/bin/env python3
import torch

# If you want to use your GPU make sure MPS is working beforehand.
# Check if MPS is available
if torch.backends.mps.is_available():
    print("MPS is available.")
    try:
        # Simple tensor operation
        x = torch.ones(3, 3).to("mps")
        print("MPS computation successful:", x)
    except Exception as e:
        print("MPS computation failed:", e)
else:
    print("MPS is not available.")
