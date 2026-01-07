import pandas as pd
import glob
import geopandas as gpd

data_set = "../data/clean-gun-violence-data.csv"
df = pd.read_csv(data_set)

# tract map section
files = glob.glob("../data/census_tracts/*.zip")
gdfs = []
for f in files:
  temp_gdf = gpd.read_file(f)
  gdfs.append(temp_gdf)
national_tract_map = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))
national_tract_map = national_tract_map.to_crs("EPSG:4326")

gdf_incidents = gpd.GeoDataFrame(df, 
                                 geometry=gpd.points_from_xy(df.longitude, df.latitude), crs="EPSG:4326" )
gdf_incidents = gdf_incidents.to_crs(national_tract_map.crs)

income_df = pd.read_csv('../data/ACSDT5Y2017.B19013-Data.csv', skiprows=[1])
income_df['GEOID'] = income_df['GEO_ID'].str[-11:]

gdf_with_geoid = gpd.sjoin(gdf_incidents, national_tract_map[['geometry', 'GEOID']], how='left', predicate='within')
final_df = gdf_with_geoid.merge(income_df[['GEOID', 'B19013_001E']], on='GEOID', how='left')
final_df['median_income'] = pd.to_numeric(final_df['B19013_001E'], errors='coerce')

final_df = final_df.drop(columns=['GEOID', 'B19013_001E', 'index_right', 'geometry'])
final_df.to_csv('../data/data_with_income.csv', index=False)

# uncomment to recreate 'map.html'
# gdf_incidents.plot(markersize=0.5, color='red', alpha=0.5)
# m = gdf_incidents.head(61725).explore()

# m.save("map.html")
