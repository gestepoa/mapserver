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
# utils about...
from app.utils.tools import loopFillColor, lineMark, loopFillColor, drawIslandCountry

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


def fillin_color_image():
    plt.rcParams['font.sans-serif'] = ['SimHei','Times New Roman']
    plt.rcParams['axes.unicode_minus'] = False
    world = gpd.read_file('./data/worldmap/world.json')
    world = world.to_crs(ccrs.PlateCarree())
    fig, ax = plt.subplots(1, 1, figsize=(15, 10), subplot_kw={'projection': ccrs.Robinson(central_longitude=150)})
    world.plot(ax=ax, color='lightgray', edgecolor='black', linewidth=0.3, transform=ccrs.PlateCarree())

    countries_to_fill1 = ['阿尔及利亚','安哥拉','阿塞拜疆','布基纳法索','喀麦隆','中非','智利','古巴','吉布提','刚果金','埃塞俄比亚','加纳','几内亚比绍','以色列','约旦',
                        '利比里亚','利比亚','马来西亚','马绍尔群岛','毛里塔尼亚','摩洛哥','莫桑比克','缅甸','纳米比亚','瑙鲁','朝鲜','巴基斯坦','巴拉圭','刚果布','塞内加尔',
                        '索马里','南苏丹','苏里南','东帝汶','多哥','突尼斯','土耳其','越南','西撒哈拉','津巴布韦']
    loopFillColor(ax, world, countries_to_fill1, '#FF5733')

    countries_to_fill2 = ['库拉索','巴拿马','圣基茨和尼维斯','圣多美和普林西比','叙利亚']
    loopFillColor(ax, world, countries_to_fill2, '#33FF57')

    countries_to_fill3 = ['布隆迪','菲律宾','斯洛文尼亚']
    loopFillColor(ax, world, countries_to_fill3, 'darkblue')

    countries_to_fill4 = ['科摩罗','密克罗尼西亚','新西兰']
    loopFillColor(ax, world, countries_to_fill4, 'pink')

    countries_to_fill5 = ['中国','洪都拉斯','巴布亚新几内亚','萨摩亚','新加坡','所罗门群岛','土库曼斯坦']
    loopFillColor(ax, world, countries_to_fill5, '#33FFF0')

    countries_to_fill6 = ['澳大利亚','赤道几内亚']
    loopFillColor(ax, world, countries_to_fill6, '#FFD133')

    countries_to_fill7 = ['格林纳达','塔吉克斯坦']
    loopFillColor(ax, world, countries_to_fill7, 'yellow')

    countries_to_fill8 = ['委内瑞拉']
    loopFillColor(ax, world, countries_to_fill8, 'darkgreen')

    countries_to_fill9 = ['波黑','图瓦卢']
    loopFillColor(ax, world, countries_to_fill9, '#8F33FF')

    countries_to_fill10 = ['佛得角','多米尼克']
    loopFillColor(ax, world, countries_to_fill10, '#FF8F33')

    countries_to_fill12 = ['乌兹别克斯坦']
    loopFillColor(ax, world, countries_to_fill12, '#33A6FF')

    countries_to_fill15 = ['库克群岛']
    loopFillColor(ax, world, countries_to_fill15, '#FF3333')

    countries_to_fill27 = ['巴西']
    loopFillColor(ax, world, countries_to_fill27, '#A6FF33')

    countries_to_fill50 = ['美国']
    loopFillColor(ax, world, countries_to_fill50, '#F033FF')

    island_country = {
        '库克群岛':[-21.235266662743765, -159.77640155811218],
        '佛得角':[15.075660583762867, -23.627715927228998],
        '格林纳达':[12.122113862228266, -61.673334467952486],
        '多米尼克':[15.436902727777584, -61.338979738651105],
        '所罗门群岛':[-9.486442050187662, 160.17259557318891],
        '密克罗尼西亚':[6.8825268898632785, 158.2282088017763],
        '帕劳':[7.488356129903986, 134.5573641315517],
        '萨摩亚':[-13.591478417872379, -172.43533122131976],
        '圣马力诺':[43.93792627533375, 12.46592907646659],
        '圣多美和普林西比':[0.29971313113035536, 6.607277730117537],
        '汤加':[-21.192247250489682, -175.19411004288972],
        '瓦努阿图':[-15.327100601044503, 166.91994719767138],
        '安道尔':[42.55533690684225, 1.5678292672253036],
        '库拉索':[12.128071224145407, -68.9315771483982],
        '马尔代夫':[4.1742945500092015, 73.51053025602174],
        '马绍尔群岛':[5.921044683397229, 169.64306302946653],
        '圣文森特和格林纳丁斯':[13.26438672030793, -61.183523116508844],
        '塞舌尔':[-4.658958934603441, 55.45762756344232],
        '新加坡':[1.3620466932996915, 103.80715635526157],
        '圣基茨和尼维斯':[17.344593346604913, -62.79068450811422],
        '科摩罗':[-11.714088255340494, 43.3312097402893],
        '图瓦卢':[-8.520739400898155, 179.19928447986726]
        }

    drawIslandCountry(ax, island_country, countries_to_fill1, '#FF5733')
    drawIslandCountry(ax, island_country, countries_to_fill2, '#33FF57')
    drawIslandCountry(ax, island_country, countries_to_fill4, 'pink')
    drawIslandCountry(ax, island_country, countries_to_fill5, '#33FFF0')
    drawIslandCountry(ax, island_country, countries_to_fill7, 'yellow')
    drawIslandCountry(ax, island_country, countries_to_fill9, '#8F33FF')
    drawIslandCountry(ax, island_country, countries_to_fill10, '#FF8F33')
    drawIslandCountry(ax, island_country, countries_to_fill15, '#FF3333')


    legend_elements = [
        Line2D([0], [0], marker='s', color='w', markerfacecolor='#F033FF', markersize=15, label='50', linestyle='None'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='#A6FF33', markersize=15, label='27', linestyle='None'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='#FF3333', markersize=15, label='15', linestyle='None'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='#33A6FF', markersize=15, label='12', linestyle='None'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='#FF8F33', markersize=15, label='10', linestyle='None'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='#8F33FF', markersize=15, label='9', linestyle='None'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='darkgreen', markersize=15, label='8', linestyle='None'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='yellow', markersize=15, label='7', linestyle='None'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='#FFD133', markersize=15, label='6', linestyle='None'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='#33FFF0', markersize=15, label='5', linestyle='None'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='pink', markersize=15, label='4', linestyle='None'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='darkblue', markersize=15, label='3', linestyle='None'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='#33FF57', markersize=15, label='2', linestyle='None'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='#FF5733', markersize=15, label='1', linestyle='None')
    ]

    legend = ax.legend(handles=legend_elements, loc='lower left', title='国旗中星星数量', title_fontsize='large', ncol=3, handleheight=1.5)
    legend.get_frame().set_facecolor('lightgray')
    ax.tick_params(axis='both', which='both', length=0, labelsize=0)
    output_path = os.path.join('./result', 'fillinColorMap.jpg').replace("\\", "/")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    return output_path
