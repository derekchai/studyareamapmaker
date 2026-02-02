import matplotlib.pyplot as plt
import numpy as np
import math
from fastapi import FastAPI, Response, File, UploadFile
from io import BytesIO
from typing import Annotated
from matplotlib.image import imread

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

@app.post("/identity",
          responses={
              200: { "content": { "image/png": {} } }
          })
async def get_identity(file: UploadFile):
    file_contents = await file.read()
    image = imread(BytesIO(file_contents))

    plt.figure()
    plt.imshow(image)

    buffer = BytesIO()
    plt.savefig(buffer, format="png")

    plt.close()

    return Response(content=buffer.getvalue(), media_type="image/png")
