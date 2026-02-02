import geopandas as gpd
import matplotlib.pyplot as plt
from io import BytesIO

def get_map(shapefile_path: str) -> bytes:
    shape: gpd.GeoDataFrame = gpd.read_file(shapefile_path)

    fig, ax = plt.subplots(figsize=(9, 9))

    shape.plot(ax=ax, linewidth=1, edgecolor="k", facecolor="w")

    ax.set_title("Shapefile")

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    return buffer.getvalue()
