"""
Fonctions pour pré-traiter et lire les données
"""

from importlib import resources
from typing import Optional

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

from dgfip import paths


def get_structures(crs: Optional[str] = None):
    """
    Retourne les structures DFGIP

    Args:
        crs: conversion dans le référentiel donné

    Returns:
        geodataframe des structures
    """

    with resources.path("dgfip.data", paths.STRUCTURES) as file:
        structures = pd.read_csv(file, sep=";")

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


def get_qpv(compute_distance: bool = False) -> gpd.GeoDataFrame:
    """
    Retourne la base de données des QPV

    Args:
        compute_distance: si vrai, enrichit la base des distances aux structures DGFIP

    Returns:
        geodataframe des qpv

    """

    fs = resources.files("dgfip.data")
    qpv = gpd.read_file(fs.joinpath(paths.QPV), crs="2154")

    if compute_distance:
        qpv = add_distances(qpv)
    return qpv


def get_iris(compute_distance: Optional[bool] = False) -> gpd.GeoDataFrame:
    """
    Retourne les informations démographiques du recensement à l'IRIS

    Args:
        compute_distance: si vrai, ajoute les distances aux structures DGFIP
    Returns:
        geodataframe des iris
    """

    fs = resources.files("dgfip.data")
    iris = gpd.read_file(fs.joinpath(paths.IRIS))
    rec = pd.read_csv(
        fs.joinpath(paths.RECENSEMENT),
        sep=";",
        dtype={"IRIS": str, "COM": str, "LAB_IRIS": str},
    )

    # convert to str before merging
    rec["IRIS"] = rec["IRIS"].str.ljust(9, fillchar="0")

    iris = iris.drop(columns="IRIS")
    iris_enrichi = iris.merge(rec, left_on="CODE_IRIS", right_on="IRIS")

    if compute_distance:
        iris_enrichi = add_distances(iris_enrichi)

    return iris_enrichi


def get_com(compute_distance: Optional[bool] = False) -> gpd.GeoDataFrame:
    """
    Retourne les communes enrichies des informations du recensement et de Filosofi

    Args:
        compute_distance: si vrai, ajoute les distances aux structures DGFIP
    Returns:
        geodataframe des communes
    """

    fs = resources.files("dgfip.data")
    com = gpd.read_file(fs.joinpath(paths.COM))
    rec = pd.read_csv(
        fs.joinpath(paths.RECENSEMENT_COM), sep=";", dtype={"CODGEO": str}
    )
    rev = pd.read_csv(
        fs.joinpath(paths.REVENUS_COM),
        sep=";",
        dtype={"CODGEO": str},
        usecols=["CODGEO", "MED17"],
    )

    base = com.merge(rec, left_on="code_commune_insee", right_on="CODGEO")
    base = base.merge(rev, on="CODGEO")
    base = base[base.CODGEO.str.slice(0, 2) != "97"]

    if compute_distance:
        base = add_distances(base, inside=False)

    return base


def extract_coord(coords: str) -> Point:
    """
    Parsing des coordonnées

    Args:
        coords: coordonnées au format lon,lat

    Returns:
        Point au format Shapely
    """
    lon, lat = coords.split(",")
    return Point(float(lat), float(lon))


def add_distances(
    sources: gpd.GeoDataFrame, inside: None | bool = True, public: str | None = None
) -> gpd.GeoDataFrame:
    """
    Calcule la distance (km) à la structure DGFIP la plus proche, pour chaque source et type de service.
    Rajoute les colonnes correspondantes.

    Args:
        sources: geodataframe des sources
        inside: si vrai, rajoute pour chaque source si elle contient une structure DGFIP

    Returns:
        le geodataframe enrichi des distances
    """

    # conversion en Lambert 93 pour le calcul des distances
    if sources.crs.to_epsg() != "2154":
        sources = sources.to_crs("2154")

    structures = get_structures(crs="2154")
    # selection du public si précisé
    if public is not None:
        if public not in {"particuliers", "professionnels"}:
            raise ValueError(
                "Public prend les valeurs 'particuliers' ou 'professionnels' "
            )
        structures = structures[structures["public"].str.contains(public, na=False)]

    # par type de service
    for name, service in structures.groupby("TYPE DE SERVICE"):
        sources[f"distance {name}"] = (
            service.sindex.nearest(
                sources.geometry, return_distance=True, return_all=False
            )[1]
            / 1000
        )
        if inside:
            sources[f"intersect {name}"] = sources[f"distance {name}"].eq(0)

    # service autre que buralistes
    nonburalistes = structures[structures["TYPE DE SERVICE"] != "Buralistes"]
    sources["distance non Buralistes"] = (
        nonburalistes.sindex.nearest(
            sources.geometry, return_distance=True, return_all=False
        )[1]
        / 1000
    )
    if inside:
        sources["intersect non Buralistes"] = sources["distance non Buralistes"].eq(0)

    return sources


def get_dep(crs: Optional[bool] = None) -> gpd.GeoDataFrame:
    """
    Retourne le contour des départements

    Args:
        crs: si fourni, convertion dans le référentiel donné

    Returns:
        geodataframe des départements
    """

    with resources.path("dgfip.data", paths.DEP) as file:
        dep = gpd.read_file(file, crs="4236")

    if crs is not None:
        dep = dep.to_crs(crs)
    return dep
