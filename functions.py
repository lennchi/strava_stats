import pandas as pd
import gpxpy


def read_strava_data(activities_file):
    """Read the Strava CSV, remove columns we don't need, return a dataframe"""

    # Open the file
    df = pd.read_csv(activities_file)

    # # See what columns we have here
    # print(df.columns)

    # Split date and time into 2 columns
    df['Activity Date'] = pd.to_datetime(df['Activity Date'], format="%b %d, %Y, %I:%M:%S %p")
    df['Date'] = df['Activity Date'].dt.date
    df['Time'] = df['Activity Date'].dt.time
    df.drop(columns=['Activity Date'], inplace=True)

    # Order the columns and only keep the ones we need
    df = df[['Activity ID', 'Date', 'Time', 'Activity Type', 'Activity Name', 'Elapsed Time', 'Moving Time',
             'Distance', 'Average Speed', 'Elevation Gain', 'Elevation Loss', 'Elevation Low', 'Elevation High',
             'Max Grade', 'Average Grade']]

    # Rename some columns
    df.rename(columns={'Activity ID': 'ID', 'Activity Type': 'Type', 'Activity Name': 'Name'}, inplace=True)

    return df


def get_coordinates(df):
    """Extract latitude and longitude from GPX files for individual activities (walks, hikes, and rides)
     in the dataframe by activity ID"""

    coordinates = []

    for index, row in df.iterrows():

        activity_id = row['ID']
        activity_type = row['Type']
        activity_date = row['Date']
        activity_name = row['Name']
        distance = row['Distance']

        # Check if the activity is a hike or a bike ride
        if row['Type'] in ('Hike', 'Ride'):
            # Extract route coordinates from the corresponding gpx file
            try:
                with open(f"data/activities/{activity_id}.gpx", 'r', encoding='utf-8') as f:
                    gpx = gpxpy.parse(f)
            except FileNotFoundError:
                continue

            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        # print(point.latitude, point.longitude)
                        coordinates.append((activity_date, activity_type, activity_name, distance,
                                            round(point.latitude, 4), round(point.longitude, 4)))

    df_coordinates = pd.DataFrame(coordinates, columns=['Date', 'Type', 'Name', 'Distance', 'Latitude', 'Longitude'])
    return df_coordinates


def compress_coordinates(df):
    """Compress the coordinates file by only keeping every 10th record"""
    # Keep every 100th row for hikes and every 30th for bike rides
    df_compressed = df.iloc[::100, :]

    return df_compressed
