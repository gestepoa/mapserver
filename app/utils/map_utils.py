# geodesy about...
import geopandas as gpd
from geopy.distance import geodesic
from shapely.geometry import Point
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
import json
# utils about...
from app.schemas.schemas import CircleMap, FillinMap, PointQuery, SeparateMap
from app.utils.tools import loopFillColor, lineMark, loopFillColor, drawIslandCountry, loopFillColorShp
# database about...
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.model import MapPoint, POI
from sqlalchemy.future import select
from sqlalchemy import case

matplotlib.use('Agg')
target_country_list = [
    '库克群岛','佛得角','格林纳达','多米尼克','所罗门群岛','密克罗尼西亚','帕劳','萨摩亚','圣马力诺','圣多美和普林西比','汤加','瓦努阿图',
    '安道尔','库拉索','马尔代夫','马绍尔群岛','圣文森特和格林纳丁斯','塞舌尔','新加坡','圣基茨和尼维斯','科摩罗','图瓦卢', '特立尼达和多巴哥', 
    "巴巴多斯", "巴哈马", "斐济", "毛里求斯", "安提瓜和巴布达", "摩纳哥", "梵蒂冈", "马耳他", "列支敦士登", "阿鲁巴", "巴林", "百慕大", "英属维尔京群岛", 
    "美属维尔京群岛", "开曼群岛", "关岛", "香港", "澳门", "北马里亚纳群岛", "波多黎各", "圣卢西亚", "圣马丁", "特克斯和凯科斯群岛"
]
area_dict = {
    "欧洲": [45, -25, 33, 68],
    "亚洲": [25, 155, -12, 65]
}


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

    world = gpd.read_file('./data/worldmap/world.json')
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
    
    output_path = os.path.join('./result', 'Nightshade.jpg').replace("\\", "/")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

    return output_path


def generate_circle_image(lon1, lat1, lon2, lat2):
    world = gpd.read_file('./data/worldmap/world.json')
    world = world.to_crs(ccrs.PlateCarree())

    fig, ax = plt.subplots(1, 1, figsize=(15, 10), subplot_kw={'projection': ccrs.Miller(central_longitude=150)})
    world.plot(ax=ax, color='none', edgecolor='black', linewidth=0.3, transform=ccrs.PlateCarree())

    # 定义点P1和点P2的经纬度
    # longitude1, latitude1 = 82.8083, 25.2167
    # longitude2, latitude2 = -165.658, -61.5917
    points = [Point(lon1, lat1), Point(lon2, lat2)]
    gdf = gpd.GeoDataFrame(index=[0, 1], crs=ccrs.PlateCarree(), geometry=points)

    # 绘制点P1和点P2
    gdf.plot(ax=ax, color='red', markersize=30, transform=ccrs.PlateCarree())
    lats = np.linspace(-90, 90, 300)
    lons = np.linspace(-180, 180, 600)
    lon_grid, lat_grid = np.meshgrid(lons, lats)
    distance_diff1 = np.zeros(lon_grid.shape)
    distance_diff2 = np.zeros(lon_grid.shape)

    # 计算每个网格点到目标点的球面距离
    for i in range(lon_grid.shape[0]):
        for j in range(lon_grid.shape[1]):
            point = (lat_grid[i, j], lon_grid[i, j])
            distance_diff1[i, j] = geodesic(point, (lat1, lon1)).kilometers
            distance_diff2[i, j] = geodesic(point, (lat2, lon2)).kilometers

    # 绘制等高线填充颜色
    ax.contourf(lon_grid, lat_grid, distance_diff1, levels=[-1e10, 705, 1e10], colors=['lightgreen', 'none'], transform=ccrs.PlateCarree(), zorder=0)
    ax.contour(lon_grid, lat_grid, distance_diff1, levels=[705], colors='green', transform=ccrs.PlateCarree(), zorder=3)
    ax.contourf(lon_grid, lat_grid, distance_diff2, levels=[-1e10, 10505, 1e10], colors=['lightblue', 'none'], transform=ccrs.PlateCarree(), zorder=0)
    ax.contour(lon_grid, lat_grid, distance_diff2, levels=[10505], colors='green', transform=ccrs.PlateCarree(), zorder=3)

    ax.set_extent([180, -180, -80, 80], crs=ccrs.PlateCarree())
    ax.tick_params(axis='both', which='both', length=0, labelsize=0)
    output_path = os.path.join('./result', 'BillionPopulationCircle.jpg').replace("\\", "/")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

    return output_path


async def generate_separate_image(data: SeparateMap, db: AsyncSession):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    full_path = os.path.join('data', 'worldmap', 'world.json')
    world = gpd.read_file(full_path)
    world = world.to_crs(ccrs.PlateCarree())
    fig, ax = plt.subplots(1, 1, figsize=(15, 10), subplot_kw={'projection': ccrs.Miller(central_longitude=150)})
    world.plot(ax=ax, color='none', edgecolor='black', linewidth=0.3, transform=ccrs.PlateCarree())

    order_condition = case({name: index for index, name in enumerate(data.name)}, value=POI.name,)

    latList = []
    lonList = []
    coorList = []
    result = await db.execute(select(POI).where(POI.name.in_(data.name)).order_by(order_condition))
    points = result.scalars().all()
    if len(points) > 0:
        for point in points:
            latList.append(point.latitude)
            lonList.append(point.longitude)
            coorList.append((point.latitude, point.longitude))
            print([point.latitude, point.longitude])
    lats = np.linspace(-90, 90, 600)
    lons = np.linspace(-180, 180, 1200)
    lon_grid, lat_grid = np.meshgrid(lons, lats)
    nearest_city = np.zeros(lon_grid.shape)

    for i in range(lon_grid.shape[0]):
        for j in range(lon_grid.shape[1]):
            point = (lat_grid[i, j], lon_grid[i, j])
            distances = [geodesic(point, city).kilometers for city in coorList]
            nearest_city[i, j] = np.argmin(distances)
    
    colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 'lightpink', 'lightgray', 'lightcyan', 'green', 'cyan', 'deepskyblue', 'pink']
    contourf = ax.contourf(lon_grid, lat_grid, nearest_city, levels=np.arange(-0.5, len(data.name), 1), colors=colors, transform=ccrs.PlateCarree(), zorder=0)
    contour = ax.contour(lon_grid, lat_grid, nearest_city, levels=np.arange(0.5, 0.5+len(data.name)-1, 1), colors='k', transform=ccrs.PlateCarree())
    ax.scatter(lonList, latList, color='black', marker='o', zorder=5, transform=ccrs.PlateCarree())

    legend_elements = []
    for i in range(len(data.name)):
        legend_elements.append(Line2D([0], [0], marker='s', color='w', markerfacecolor=colors[i], markersize=15, label=data.name[i], linestyle='None'))
    legend = ax.legend(handles=legend_elements, loc='lower left', title='图例', ncol=1, handleheight=1.5, title_fontsize=16, prop={'size': 14})
    legend.get_frame().set_facecolor('lightgray')
    ax.set_extent([180, -180, -80, 80], crs=ccrs.PlateCarree())
    ax.tick_params(axis='both', which='both', length=0, labelsize=0)

    output_path = os.path.join('./result', 'separateMap.jpg').replace("\\", "/")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    return output_path


async def fillin_color_image(data: FillinMap, db: AsyncSession):
    plt.rcParams['font.sans-serif'] = ['SimHei','Times New Roman']
    plt.rcParams['axes.unicode_minus'] = False
    worldColor = data.worldColor if data.worldColor else 'darkgray'
    boderColor = data.boderColor if data.boderColor else 'black'
    lineWidth = data.boderWidth if data.boderWidth else 0.3
    legendTitle = data.legendTitle if data.legendTitle else '图例'
    world = gpd.read_file('./data/worldmap_shp/World_countries.shp')
    world = world.to_crs(ccrs.PlateCarree())
    fig, ax = plt.subplots(1, 1, figsize=(15, 10), subplot_kw={'projection': ccrs.Miller(central_longitude=0)})
    world.plot(ax=ax, color=worldColor, edgecolor=boderColor, linewidth=lineWidth, transform=ccrs.PlateCarree())

    legend_elements = []
    for single in data.countryList:
        # large country fillin color
        loopFillColorShp(ax, world, single.country, single.color)
        legend_elements.append(Line2D([0], [0], marker='s', color='w', markerfacecolor=single.color, markersize=15, label=single.note, linestyle='None'))
        #tiny country pointing
        spotList = []
        latList = []
        lonList = []
        for singleCountry in single.country:
            if singleCountry in target_country_list:
                spotList.append(singleCountry)
        if len(spotList) > 0:
            result = await db.execute(select(MapPoint).where(MapPoint.spot_name.in_(spotList)))
            points = result.scalars().all()
            if len(points) > 0:
                for point in points:
                    latList.append(point.latitude)
                    lonList.append(point.longitude)
        drawIslandCountry(ax, lonList, latList, single.color)
    legend_elements.append(Line2D([0], [0], marker='s', color='w', markerfacecolor='darkgray', markersize=15, label='no data', linestyle='None'))

    legend = ax.legend(handles=legend_elements, loc='lower left', title=legendTitle, ncol=1, handleheight=1.5, title_fontsize=16, prop={'size': 14})
    legend.get_frame().set_facecolor('lightgray')
    ax.tick_params(axis='both', which='both', length=0, labelsize=0)
    # range setting
    range = [45, -25, 33, 68] if data.range == '欧洲' else [180,-180,-85, 85]
    range = data.range if data.range else [180,-180,-85, 85]
    ax.set_extent(range, crs=ccrs.PlateCarree())
    output_path = os.path.join('./result', 'fillinColorMap.jpg').replace("\\", "/")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    return output_path


async def fillin_color_image_pro(data: FillinMap, db: AsyncSession):
    plt.rcParams['font.sans-serif'] = ['SimHei','Times New Roman']
    plt.rcParams['axes.unicode_minus'] = False
    world = gpd.read_file('./data/worldmap/world_update.json')
    world = world.to_crs(ccrs.PlateCarree())
    fig, ax = plt.subplots(1, 1, figsize=(15, 10), subplot_kw={'projection': ccrs.Robinson(central_longitude=150)})
    world.plot(ax=ax, color='darkgray', edgecolor='white', linewidth=0.8, transform=ccrs.PlateCarree())

    legend_elements = []
    for single in data.countryList:
        # large country fillin color
        loopFillColor(ax, world, single.country, single.color)
        legend_elements.append(Line2D([0], [0], marker='s', color='w', markerfacecolor=single.color, markersize=15, label=single.note, linestyle='None'))
        #tiny country pointing
        spotList = []
        latList = []
        lonList = []
        for singleCountry in single.country:
            if singleCountry in target_country_list:
                spotList.append(singleCountry)
        if len(spotList) > 0:
            # points = db.query(MapPoint).filter(MapPoint.spot_name.in_(spotList)).all()
            result = await db.execute(select(MapPoint).where(MapPoint.spot_name.in_(spotList)))
            points = result.scalars().all()
            if len(points) > 0:
                for point in points:
                    latList.append(point.latitude)
                    lonList.append(point.longitude)
        drawIslandCountry(ax, lonList, latList, single.color)

    legend = ax.legend(handles=legend_elements, loc='lower left', title='图例', title_fontsize='large', ncol=3, handleheight=1.5)
    legend.get_frame().set_facecolor('lightgray')
    ax.tick_params(axis='both', which='both', length=0, labelsize=0)
    areaPara = area_dict.get(data.area)
    if areaPara is not None:
        ax.set_extent(areaPara, crs=ccrs.PlateCarree())
    output_path = os.path.join('./result', 'fillinColorMap.jpg').replace("\\", "/")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    return output_path


async def draw_polyline(geojson_data):
    plt.rcParams['font.sans-serif'] = ['SimHei','Times New Roman']
    plt.rcParams['axes.unicode_minus'] = False
    world = gpd.read_file('./data/worldmap/world.json')
    world = world.to_crs(ccrs.PlateCarree())
    border = gpd.read_file(geojson_data)
    border = border.to_crs(ccrs.PlateCarree())

    fig, ax = plt.subplots(1, 1, figsize=(15, 10), subplot_kw={'projection': ccrs.Robinson(central_longitude=150)})
    world.plot(ax=ax, color='lightgray', edgecolor='black', linewidth=0.3, transform=ccrs.PlateCarree())
    border.plot(ax=ax, color='red', linewidth=0.8, transform=ccrs.PlateCarree())

    ax.tick_params(axis='both', which='both', length=0, labelsize=0)
    output_path = os.path.join('./result', 'boderMap.jpg').replace("\\", "/")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    return output_path


async def kml2geojson(geojson_data):
    plt.rcParams['font.sans-serif'] = ['SimHei','Times New Roman']
    plt.rcParams['axes.unicode_minus'] = False
    world = gpd.read_file('./data/worldmap/world.json')
    world = world.to_crs(ccrs.PlateCarree())
    border = gpd.read_file(geojson_data)
    border = border.to_crs(ccrs.PlateCarree())

    fig, ax = plt.subplots(1, 1, figsize=(15, 10), subplot_kw={'projection': ccrs.Robinson(central_longitude=150)})
    world.plot(ax=ax, color='lightgray', edgecolor='black', linewidth=0.3, transform=ccrs.PlateCarree())
    border.plot(ax=ax, color='red', linewidth=0.8, transform=ccrs.PlateCarree())

    ax.tick_params(axis='both', which='both', length=0, labelsize=0)
    output_path = os.path.join('./result', 'boderMap.jpg').replace("\\", "/")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    return output_path
