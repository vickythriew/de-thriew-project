import requests
import pandas as pd

url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
data = requests.get(url, timeout=30).json()

rows = []
for f in data ["features"]:
    p = f["properties"]
    rows.append({
        "place": p["place"],
        "magnitude": p["mag"],
        "time": pd.to_datetime(p["time"], unit="ms"),
    })
df = pd.DataFrame(rows)
'''
print(df.head(10))
print(f"Total rows: {len(df)}")
'''

#clean
df = df.dropna(subset=["magnitude"])  #remove rows
df = df.drop_duplicates()             #remove duplicate
df["place"] = df["place"].str.strip() #tidy text

# add a simple derived column
df["is_strong"] = df["magnitude"] >= 4.0

#save
df.to_csv("earthquakes.csv", index=False)

print(df.head(10))
print(f"saved {len(df)} rows to earthquakes.csv")
print(f"Strong earthquakes (>= 4.0): {df['is_strong'].sum()}")