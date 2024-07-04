import pandas as pd

# DOC Campsites dataset described in [data.govt.nz](https://catalogue.data.govt.nz/dataset/doc-campsites4)
# Get data in CSV from DOC:
# curl -L https://doc-deptconservation.opendata.arcgis.com/api/download/v1/items/c417dcd7c9fb47b489df1f9f0a673190/csv?layers=0 > data.csv

data = pd.read_csv('data.csv', header = 0, usecols =
                   ['Region',
                    'Number of powered sites',
                    'Number of unpowered sites'
                    ])

print("Campsites by region")
print("-------------------")
campsites_by_region = data.groupby('Region').Region.count()
print(campsites_by_region)

print("")
print("Site types per region")
print("---------------------")
site_types_per_region = data.groupby('Region').sum()
print(site_types_per_region)
