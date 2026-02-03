import geopandas as gpd
import matplotlib.pyplot as plt
from io import BytesIO
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.ticker import FuncFormatter, MultipleLocator
from matplotlib_map_utils.core import north_arrow, scale_bar
from .study_map import StudyMap
from shapely.geometry import box

_WGS84 = "EPSG:4326"

def generate_study_area_map(shapefile_path: str,
                            map: StudyMap) -> bytes:
    shape: gpd.GeoDataFrame = gpd.read_file(shapefile_path)

    fig, ax = plt.subplots(figsize=(9, 9))

    _plot_study_regions(ax, map, shape)
    _plot_inset_map(ax, shape, map)

    ax.set_title(map.title)
    ax.set_facecolor("lightblue")
    
    if not map.show_axis_ticks:
        ax.set_xticks([])
        ax.set_yticks([])

    if map.show_north_arrow:
        north_arrow(ax, location="upper left", 
                    rotation={ "crs": shape.crs, "reference": "center" })
    
    if map.show_scale:
        scale_bar(ax, location="lower left", bar={ "projection": shape.crs }, 
                  labels={ "style": "first_last" })

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    return buffer.getvalue()

def _deg_min_formatter(x, pos):
    sign = "−" if x < 0 else ""
    x = abs(x)
    deg = int(x)
    minutes = (x - deg) * 60
    return f"{sign}{deg}°{minutes:.0f}′"

def _plot_study_regions(ax: plt.Axes, 
                        map: StudyMap, 
                        base_shape: gpd.GeoDataFrame):
    base_shape.plot(ax=ax, linewidth=1, edgecolor="k", facecolor="w")

    if map.get_study_regions_data_frame_wgs84().empty:
        return

    data_frame = map.get_study_regions_data_frame_wgs84().to_crs(base_shape.crs)
    data_frame.plot(ax=ax, linewidth=1, alpha=0.3, column="name", cmap="Paired", 
                    legend=True, legend_kwds={ "loc": "lower right" })
    
    min_x, min_y, max_x, max_y = data_frame.total_bounds
    height = max_y - min_y
    width = max_x - min_x

    t, b = map.pad_top_factor, map.pad_bottom_factor, 
    l, r = map.pad_left_factor, map.pad_right_factor

    ax.set_xlim(min_x - l * width, max_x + r * width)
    ax.set_ylim(min_y - b * height, max_y + t * height)


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

    if map.get_study_regions_data_frame_wgs84().empty:
        return

    map.get_study_regions_data_frame_wgs84().set_geometry("centroid").plot(ax=inset, color="red")
