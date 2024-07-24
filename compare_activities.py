# PROBLEM
# An activity ID showed up in the activities.csv file, but there's no  corresponding gpx file for it


import os
import pandas as pd

# Create a list of all file names in the ACTIVITIES dir (without extensions)

file_names = []

for root, dirs, files in os.walk("data/activities"):
    for file in files:
        file = file.strip(".gpx gz fit")
        file_names.append(file)

# Create a list of activity IDs
df = pd.read_csv("data/clean_strava_stats.csv")

activity_ids = df['ID'].tolist()

print(len(activity_ids))
print(len(file_names))

# # Check for activity IDs for which there are no corresponding GPX files
# orphan_ids = set(activity_ids) - set(file_names)
#
# print(len(orphan_ids))