from functions import read_strava_data, get_coordinates, compress_coordinates

# Write clean activity data to a new CSV
df = read_strava_data('data/activities.csv')
df.to_csv('data/clean_strava_stats.csv', index=False)

# Write extracted coordinates for hikes and bike rides to a CSV
extracted_coors = get_coordinates(df)
extracted_coors.to_csv('data/coordinates.csv', index=False)

# Compress the coordinates CSV by keeping every 100th row
compressed_coors = compress_coordinates(extracted_coors)
compressed_coors.to_csv('data/coordinates_compressed.csv', index=False)
