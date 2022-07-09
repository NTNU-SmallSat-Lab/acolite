## def copernicus_dem_lonlat
## returns Copernicus DEM data for given lon, lat grid
##
## Copernicus DEM GLO-30 and GLO-90 are provided by Copernicus and is reformatted to COG files by Amazon
## link to readme: https://copernicus-dem-30m.s3.amazonaws.com/readme.html
## link to public release: https://spacedata.copernicus.eu/blogs/-/blogs/copernicus-dem-30-meter-dataset-now-publicly-available
##
## function written by Quinten Vanhellemont, RBINS
## 2022-07-06
## modifications:

def copernicus_dem_lonlat(lon1, lat1, sea_level=0, source='copernicus30', nearest=False, dem_min = -500.0):

    import os
    import acolite as ac
    import numpy as np

    ## get limit based on lat lon and find and download DEM tiles
    limit = np.nanmin(lat1), np.nanmin(lon1), np.nanmax(lat1), np.nanmax(lon1)
    dem_tiles = ac.dem.copernicus_dem_find(limit, source = source)

    ## run through dem files and reproject data to target lat,lon
    for i, dem_tile in enumerate(dem_tiles):
        cdm = ac.shared.read_band(dem_tile)
        dct = ac.shared.projection_read(dem_tile)
        lon0, lat0 = ac.shared.projection_geo(dct)

        result = ac.shared.reproject2(cdm, lon0, lat0, lon1, lat1, nearest=nearest)
        if i == 0:
            dem = result
        else:
            dem[result > dem_min] = result[result > dem_min]

    dem[dem<=dem_min] = sea_level

    return(dem)