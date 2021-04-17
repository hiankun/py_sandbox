import geopandas

path_to_data = geopandas.datasets.get_path("nybb")
gdf = geopandas.read_file(path_to_data)
gdf["area"] = gdf.area

gdf.plot("area", legend=True)
import matplotlib.pyplot as plt
plt.show()
