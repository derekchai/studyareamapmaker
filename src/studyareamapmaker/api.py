import matplotlib.pyplot as plt
import numpy as np
import math
from fastapi import FastAPI, Response
from io import BytesIO

app = FastAPI()

@app.get("/map",
         responses={
             200: { "content": { "image/png": {} } }
         })
async def get_map(start: float = 0,
                  stop: float = 2 * math.pi):
    x = np.arange(start, stop, 0.1)
    y = np.sin(x)
    plt.plot(x, y)
    
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    png = buffer.getvalue()
    
    return Response(content=png, media_type="image/png")