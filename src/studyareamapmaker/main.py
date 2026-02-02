import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

def get_map():
    x = np.arange(0, 5, 0.1)
    y = np.sin(x)
    plt.plot(x, y)
    
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    return buffer.getvalue()