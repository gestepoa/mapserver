# geodesy about...
import geopandas as gpd
from geopy.distance import geodesic
# cartopy about...
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.feature.nightshade import Nightshade
# matplotlib about...
import matplotlib
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
# system about...
import numpy as np
from io import BytesIO
import os
import datetime
# utils about...
from app.utils.tools import loopFillColor, lineMark

matplotlib.use('Agg')

def generate_poi_image():
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    full_path = os.path.join('data', 'worldmap', 'world.json')
    world = gpd.read_file(full_path)
    world = world.to_crs(ccrs.PlateCarree())

    fig, ax = plt.subplots(1, 1, figsize=(15, 10), subplot_kw={'projection': ccrs.Orthographic(central_longitude=-123, central_latitude=-48)})
    ax.add_feature(cfeature.OCEAN, color='lightblue')
    world.plot(ax=ax, color='lightgreen', edgecolor='black', linewidth=0.3, transform=ccrs.PlateCarree())

    longitude1, latitude1 = -123.385000, -48.868333
    lats = np.linspace(-90, 90, 300)
    lons = np.linspace(-180, 180, 600)
    lon_grid, lat_grid = np.meshgrid(lons, lats)
    distance_diff1 = np.zeros(lon_grid.shape)

    for i in range(lon_grid.shape[0]):
        for j in range(lon_grid.shape[1]):
            point = (lat_grid[i, j], lon_grid[i, j])
            distance_diff1[i, j] = geodesic(point, (latitude1, longitude1)).kilometers

    ax.contour(lon_grid, lat_grid, distance_diff1, levels=[2688], colors='red', transform=ccrs.PlateCarree(), zorder=3)
    ax.scatter([longitude1], [latitude1], color='green', marker='o', zorder=15, transform=ccrs.PlateCarree())

    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='海洋难抵极', linestyle='None'),
    ]
    legend = ax.legend(handles=legend_elements, loc='lower left', title='图例', title_fontsize='large')
    legend.get_frame().set_facecolor('lightgray')

    ax.tick_params(axis='both', which='both', length=0, labelsize=0)
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='jpg', dpi=300, bbox_inches='tight')
    img_buffer.seek(0)

    output_path = os.path.join('./result', 'output.jpg')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    return img_buffer


def generate_nightshade_image():
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    full_path = os.path.join('data', 'worldmap', 'world.json')
    world = gpd.read_file(full_path)
    world = world.to_crs(ccrs.PlateCarree())
    fig, ax = plt.subplots(1, 1, figsize=(15, 10), subplot_kw={'projection': ccrs.Miller(central_longitude=0)})
    world.plot(ax=ax, color='lightblue', edgecolor='black', linewidth=0.3, transform=ccrs.PlateCarree())
    ax.scatter([71.5], [-6], color='yellow', edgecolor='black', marker='o', zorder=15, transform=ccrs.PlateCarree())
    ax.scatter([57.60], [-20.24], color='blue', edgecolor='black', marker='o', zorder=15, transform=ccrs.PlateCarree())
    ax.scatter([-5.35, 33.78, -71.83, -36.56, -5.71, -128.32, -62.20, -81.22, -64.63, -64.76, -63.03, -14.38, -12.28], [36.14, 35.01, 21.77, -54.25, -15.97, -24.38, 16.73, 19.34, 18.43, 32.30, 18.23, -7.95, -37.11], color='red', edgecolor='black', marker='o', zorder=15, transform=ccrs.PlateCarree())
    lineMark(ax, 10, 60, 15, 71.5, -6, 1, 1, '查戈斯群岛')
    lineMark(ax, 10, 60, 15, 57.60, -20.24, 1, 0, '毛里求斯')

    countries_to_fill = ['英国']
    loopFillColor(world, ax, countries_to_fill, 'red')

    date = datetime.datetime(2024, 10, 9, 3, 00, 00)
    ax.add_feature(Nightshade(date, alpha=0.5))

    ax.set_title(f'晨昏线： {date}')
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=12, label='英国及其海外领地\n(不含争议及未获承认地区)', linestyle='None'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='yellow', markersize=12, label='查戈斯群岛(6.0S, 71.5E)', linestyle='None'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=12, label='毛里求斯', linestyle='None'),
    ]
    legend = ax.legend(handles=legend_elements, loc='lower left', title='图例', title_fontsize=16,prop={'size': 14})
    legend.get_frame().set_facecolor('lightgray')

    ax.set_extent([-180, 180, -80, 90], crs=ccrs.PlateCarree())
    
    output_path = os.path.join('./result', 'Nightshade.jpg')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

    return output_path
