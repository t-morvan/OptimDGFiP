"""
Lecture du fichier des structures DGFIP
"""

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

from dgfip import paths


def extract_coord(coords: str) -> Point:
    """
    Parsing des coordonnées
    :arg coords: coordonnées au format lon,lat
    """
    lon, lat = coords.split(",")
    return Point(float(lat), float(lon))


def get_structures(crs: str | None = None):
    """
    Retourne les structures DFGIP

    :arg crs: conversion dans le référentiel donné
    :returns: geodataframe des structures
    """
    structures = pd.read_csv(f"../data/{paths.STRUCTURES}", sep=";")

    # ne garde que la France métropolitaine et les structures géocodées
    geo_struct = structures[
        structures.geocodage.str.contains(",", na=False)
        & (structures["DEPARTEMENT"].str.len() == 2)
    ]
    geo_struct = geo_struct.assign(geometry=geo_struct.geocodage.apply(extract_coord))
    geo_struct = gpd.GeoDataFrame(geo_struct, crs="4326")

    if crs is not None:
        geo_struct = geo_struct.to_crs(crs)

    return geo_struct


def add_distances(
    sources: gpd.GeoDataFrame, inside: None | bool = True
) -> gpd.GeoDataFrame:
    """
    Calcule la distance (km) à la structure DGFIP la plus proche, pour chaque source et type de service.
    Rajoute in-place les colonnes correspondantes.

    :arg sources: geodataframe des sources
    :arg inside: si vrai, rajoute pour chaque source si elle contient une structure DGFIP
    """

    # conversion en Lambert 93 pour le calcul des distances
    if sources.crs.to_epsg() != "2154":
        sources = sources.to_crs("2154")

    structures = get_structures(crs="2154")
    for name, service in structures.groupby("TYPE DE SERVICE"):
        sources[f"distance {name}"] = (
            service.sindex.nearest(
                sources.geometry, return_distance=True, return_all=False
            )[1]
            / 1000
        )
        if inside:
            sources[f"intersect {name}"] = sources[f"distance {name}"].eq(0)

    return sources
