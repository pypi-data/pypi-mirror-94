"""
Small script to produce map of ECO_CODE_X to MRGID
by merging Eco-regions with other shapefiles.
"""

import pandas as pd
import shapely.geometry as sh_geo
import numpy as np
# TODO fix the import issue
from regions import read_gisd_worms_link, read_shapefile, SHAPE_NAME


def ecocode_to_mrgid():
    meow = pd.DataFrame(read_shapefile(SHAPE_NAME[0]))

    def match(row):
        if pd.isna(row['geometry']):
            return np.nan

        intersection = []

        for area in range(1, 4):
            polys = []
            meow = read_shapefile(SHAPE_NAME[area])
            try:
                if type(row['geometry']) == sh_geo.MultiPolygon:
                    polys = sh_geo.MultiPolygon(row['geometry'])
                else:
                    polys.append(sh_geo.Polygon(row['geometry']))
            except Exception as e:
                print(e)
            try:
                for item in meow.iterrows():
                    polys_meow = []
                    if type(item[1]['geometry']) == sh_geo.MultiPolygon:
                        polys_meow = sh_geo.MultiPolygon(item[1]['geometry'])
                    else:
                        polys_meow.append(sh_geo.Polygon(item[1]['geometry']))
                    for poly in polys:
                        for poly_meow in polys_meow:
                            if poly.intersects(poly_meow):
                                intersection.append(item[1]['MRGID'])
            except Exception as e:
                print(e)

        retval = list(set(intersection))

        try:
            r = ','.join(map(str, retval))
        except Exception as e:
            print(e)

        return r

    meow['MRGID'] = meow.apply(lambda x: match(x), axis=1)

    meow['MRGID'] = meow['MRGID'].astype('str', inplace=True)
    meow_split = pd.concat([pd.Series(row['ECO_CODE'], row['MRGID'].split(','))
                            for _, row in meow.iterrows()]).reset_index()
    meow_split.columns = ['MRGID', 'ECO_CODE']

    meow_all = meow.merge(meow_split, on='ECO_CODE')
    meow_all.drop(['MRGID_x'], axis=1, inplace=True)
    meow_all['MRGID'] = meow_all['MRGID_y']
    meow_all.drop(['MRGID_y'], axis=1, inplace=True)

    return meow_all


df = ecocode_to_mrgid()

out = []
for area in range(1, 4):
    meow = read_shapefile(SHAPE_NAME[area])
    out.append(pd.DataFrame(meow))
sh = pd.concat(out)

df['MRGID'] = df['MRGID'].astype('int64')
res = df.merge(sh, on='MRGID')
res['geometry'] = res['geometry_x']
res.drop(columns=['geometry_x', 'geometry_y'], inplace=True)
res.to_hdf('eco_mrgid.h5', key='eco_mrgid')

print('Done')
