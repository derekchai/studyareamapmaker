import geopandas as gpd
import matplotlib.pyplot as plt
from io import BytesIO
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.ticker import FuncFormatter, MultipleLocator
from .study_map import StudyMap

_WGS84 = "EPSG:4326"

def generate_study_area_map(shapefile_path: str,
                            map: StudyMap) -> bytes:
    shape: gpd.GeoDataFrame = gpd.read_file(shapefile_path)

    fig, ax = plt.subplots(figsize=(9, 9))

    _plot_inset_map(ax, shape, map)

    ax.set_title("Shapefile")

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    return buffer.getvalue()

def _deg_min_formatter(x, pos):
    sign = "−" if x < 0 else ""
    x = abs(x)
    deg = int(x)
    minutes = (x - deg) * 60
    return f"{sign}{deg}°{minutes:.0f}′"

def _plot_inset_map(ax: plt.Axes, 
                    shape: gpd.GeoDataFrame,
                    map: StudyMap):
    width = f"{map.inset_width * 100}%"
    height = f"{map.inset_height * 100}%"
        
    inset: plt.Axes = inset_axes(ax, width=width, height=height)

    if not map.inset_show_background:
        inset.set_frame_on(False)  # remove border
        inset.set_axis_off()  # remove axis ticks, etc.
        inset.patch.set_alpha(0)  # set transparent background

    shape = shape.to_crs(_WGS84)
    shape.plot(ax=inset, linewidth=map.inset_line_width, edgecolor="k", facecolor="w")

    inset.xaxis.set_major_formatter(FuncFormatter(_deg_min_formatter))
    inset.yaxis.set_major_formatter(FuncFormatter(_deg_min_formatter))
    inset.xaxis.set_major_locator(MultipleLocator(0.5))
    inset.yaxis.set_major_locator(MultipleLocator(0.5))

    for label in inset.get_xticklabels(): label.set_fontsize("small")
    
    for label in inset.get_yticklabels():
        label.set_fontsize("small")
        label.set_rotation_mode("anchor")
        label.set_rotation("vertical")
        label.set_verticalalignment("center")
        label.set_horizontalalignment("center")
    
    inset.tick_params(axis="y", pad=7)