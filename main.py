from pathlib import Path

import geopandas as gpd
import pandas as pd


DATA_DIR = (Path('') / 'data').absolute()
OUTPUT_DIR = (Path('') / 'output').absolute()

buildings = pd.concat([
    gpd.read_file(f'zip://{shp_file}')
    for shp_file in (DATA_DIR / 'LoD2').iterdir()
], axis=0, ignore_index=True)
buildings['geometry'] = buildings.make_valid().buffer(0)
lots = gpd.read_file(DATA_DIR / 'sehnde/sehnde.shp')
part = lots.loc[lots['gid'] == 16966199, 'geometry'].iloc[0]
buildings = buildings.loc[buildings.intersects(part)]


def save_buildings(min_area=200):
    min_area_buildings: gpd.GeoDataFrame = buildings.loc[buildings.area >= min_area]
    min_area_buildings.to_csv(OUTPUT_DIR / 'buildings.csv')


save_buildings()
