import geopandas as gpd
import matplotlib.pyplot as plt
from io import BytesIO
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

def generate_study_area_map(shapefile_path: str) -> bytes:
    shape: gpd.GeoDataFrame = gpd.read_file(shapefile_path)

    fig, ax = plt.subplots(figsize=(9, 9))

    _plot_inset_map(ax, shape)

    ax.set_title("Shapefile")

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    return buffer.getvalue()

def _plot_inset_map(ax: plt.Axes, shape: gpd.GeoDataFrame):
    inset: plt.Axes = inset_axes(ax, width="30%", height="30%")

    inset.set_frame_on(False)  # remove border
    inset.set_axis_off()  # remove axis ticks, etc.
    inset.patch.set_alpha(0)  # set transparent background

    shape.plot(ax=inset, linewidth=1, edgecolor="k", facecolor="w")