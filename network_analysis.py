import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import box, LineString, Point, Polygon
import pyproj
from shapely.ops import transform

wgs84 = pyproj.CRS('EPSG:4326')


def create_network_from_place_name(place_name):
    graph = ox.graph_from_place(place_name, network_type='drive', simplify=False)
    graph_proj = ox.project_graph(graph)
    nodes_proj, edges_proj = ox.graph_to_gdfs(graph_proj, nodes=True, edges=True)
    bbox = box(*edges_proj.unary_union.bounds)
    origin = bbox.centroid
    nodes_proj['x'] = nodes_proj.x.astype(float)
    maxx = nodes_proj['x'].max()
    target_loc = nodes_proj.loc[nodes_proj['x'] == maxx, :]
    target_point = target_loc.geometry.values[0]

    origin_node = ox.nearest_nodes(graph_proj, origin.x, origin.y)
    target_node = ox.nearest_nodes(graph_proj, target_point.x, target_point.y)

    route = nx.shortest_path(G=graph_proj, source=origin_node, target=target_node, weight='length')
    route_nodes = nodes_proj.loc[route]
    route_line = LineString(list(route_nodes.geometry.values))
    project = pyproj.Transformer.from_crs(
        pyproj.CRS(f"EPSG:{edges_proj.crs.to_epsg()}"), wgs84, always_xy=True
    ).transform
    route_line = transform(project, route_line)
    return gpd.GeoSeries([route_line]).to_json()


def create_network_from_points(source: tuple, target: tuple) -> str:
    x, y = zip(*[source, target])
    # print(max(y), min(y), max(x), min(x))
    graph = ox.graph_from_bbox(max(y), min(y), max(x), min(x), network_type='drive', simplify=False)
    graph_proj = ox.project_graph(graph)
    nodes_proj, edges_proj = ox.graph_to_gdfs(graph_proj, nodes=True, edges=True)
    # origin_point = Point(source)
    # target_point = Point(target)
    # project = pyproj.Transformer.from_crs(
    #     wgs84, pyproj.CRS(f"EPSG:{edges_proj.crs.to_epsg()}"), always_xy=True
    # ).transform
    # origin_point_projected = transform(project, origin_point)
    # target_point_projected = transform(project, target_point)
    bbox = box(*edges_proj.unary_union.bounds)
    origin = bbox.centroid
    nodes_proj['x'] = nodes_proj.x.astype(float)
    maxx = nodes_proj['x'].max()
    target_loc = nodes_proj.loc[nodes_proj['x'] == maxx, :]
    target_point = target_loc.geometry.values[0]

    origin_node = ox.nearest_nodes(graph_proj, origin.x, origin.y)
    target_node = ox.nearest_nodes(graph_proj, target_point.x, target_point.y)

    route = nx.shortest_path(G=graph_proj, source=origin_node, target=target_node, weight='length')
    route_nodes = nodes_proj.loc[route]
    route_line = LineString(list(route_nodes.geometry.values))
    project = pyproj.Transformer.from_crs(
        pyproj.CRS(f"EPSG:{edges_proj.crs.to_epsg()}"), wgs84, always_xy=True
    ).transform
    route_line = transform(project, route_line)
    return gpd.GeoSeries([route_line]).to_json()


# print(create_network_from_place_name('Kamppi, Helsinki, Finland'))
# print(create_network_from_place_name('Rostock, Germany'))
# print(create_network_from_place_name('South C, Nairobi, Kenya'))
# Index(['y', 'x', 'street_count', 'lon', 'lat', 'highway', 'geometry'], dtype='object') route_nodes
# print(create_network_from_points(source=(37.6080, -0.3878), target=(37.0680, -1.0225)))
# print(create_network_from_points(source=(36.832288, -1.3210069999999998), target=(36.8445398, -1.3236085999999998)))
# print(create_network_from_points(source=(36.8323, -1.3210), target=(36.8445, -1.3236)))
# print(create_network_from_points(source=(12.1220594, 54.1471038), target=(12.226931400000002, 54.24146429999999)))
print(create_network_from_points(source=(36.806425874950364, -1.312341481037141), target=(36.815432987689015, -1.312700787235707)))
