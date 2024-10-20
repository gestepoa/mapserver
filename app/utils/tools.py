import cartopy.crs as ccrs
import numpy as np


# fill in color on countries
def loopFillColor(world, ax, countryList, color):
    for country in countryList:
        country_data = world[world['name'] == country]
        if not country_data.empty:
            country_data.plot(ax=ax, color=color, edgecolor='black', linewidth=0.3, transform=ccrs.PlateCarree())


# line with note words
def lineMark(ax, horizontal_length, angle, line_length, lon, lat, direction1, direction2, content):
    if direction1 == 1:
        end_lon = lon + horizontal_length
        end_lat = lat
        if direction2 == 1:
            final_lon = end_lon + line_length * np.cos(np.radians(angle))
            final_lat = end_lat + line_length * np.sin(np.radians(angle))
        elif direction2 == 0:
            final_lon = end_lon + line_length * np.cos(np.radians(angle))
            final_lat = end_lat - line_length * np.sin(np.radians(angle))
        else:
            print('direction2 type error')
        ax.scatter(lon, lat, edgecolor='black', facecolor='none', marker='o', s=100, linewidths=1, zorder=5, transform=ccrs.PlateCarree())
        ax.plot([lon, end_lon, final_lon], [lat, end_lat, final_lat], color='black', linewidth=1, transform=ccrs.PlateCarree(), zorder=4)
        ax.text(final_lon, final_lat, content, verticalalignment='bottom', horizontalalignment='left', transform=ccrs.PlateCarree(), fontsize=14)
    elif direction1 == 0:
        end_lon = lon - horizontal_length
        end_lat = lat
        if direction2 == 1:
            final_lon = end_lon - line_length * np.cos(np.radians(angle))
            final_lat = end_lat + line_length * np.sin(np.radians(angle))
        elif direction2 == 0:
            final_lon = end_lon - line_length * np.cos(np.radians(angle))
            final_lat = end_lat - line_length * np.sin(np.radians(angle))
        else:
            print('direction2 type error')
        ax.scatter(lon, lat, edgecolor='black', facecolor='none', marker='o', s=100, linewidths=1, zorder=5, transform=ccrs.PlateCarree())
        ax.plot([lon, end_lon, final_lon], [lat, end_lat, final_lat], color='black', linewidth=1, transform=ccrs.PlateCarree(), zorder=4)
        ax.text(final_lon, final_lat, content, verticalalignment='bottom', horizontalalignment='right', transform=ccrs.PlateCarree(), fontsize=14)
    else:
        print('direction1 type error')


