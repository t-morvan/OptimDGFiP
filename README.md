# Hackathon Open Data de la DGFiP

> La couverture du territoire par les structures DGFiP est-elle optimale et assure-t-elle un égal accès de tous au service public ?

1. [Installation](https://github.com/t-morvan/OptimisationFiscale/edit/main/README.md#Installation--wrench)
2. [Données](https://github.com/t-morvan/OptimisationFiscale/edit/main/README.md#donn%C3%A9es)


## Installation  :wrench:
1. cloner le repo ``` git clone https://github.com/t-morvan/OptimisationFiscale.git ```
2. installer poetry https://python-poetry.org/docs/
3. ```cd``` dans le repo et faire ``` poetry install ```

4. optionnel (pour utiliser le backend vectorisé pygeos avec geopandas) : 
    ```
    poetry export --without-hashes --format requirements.txt --output requirements.txt
    sed -i -e 's/^-e //g' requirements.txt
    python3 -m pip install \
        --force-reinstall \
        --no-binary pygeos,shapely,rasterio,pyproj \
        -r requirements.txt
     ```  
    (cf https://github.com/python-poetry/poetry/issues/365)


5. lancer ```download.py``` pour télécharger les fichiers
6. décompresser le shapefile .7z001 des IRIS (avec 7zip par exemple)

## Données

Nous avons principalement utilisé des données démographiques issues du recensement de l'Insee ainsi que la base des quartiers politique de la ville.
L'ensemble des sources, url et licences utilisées sont rassemblées [ici](URLS.yaml).

## Outils

### Statistiques descriptives (non spatiales) :bar_chart:
Toutes les manipulations non spatiales ont été réalisées avec [```pandas```](https://pandas.pydata.org/).

### Calcul des distances et plus proches voisins 🗺️
Nous avons utilisé le pendant spatial de pandas, [```geopandas```](https://geopandas.org/en/stable/), pour les manipulations spatiales. La volumétrie étant assez importante (>40 000 "quartiers" IRIS), nous avons eu recours à [```pygeos```](https://pygeos.readthedocs.io/en/stable/) pour vectoriser les opérations de géometrie. Nous avons pris le soin de convertir les données en projection [Lambert 93 ](https://fr.wikipedia.org/wiki/Projection_conique_conforme_de_Lambert) afin d'assurer la précision des calculs de distances et d'aires. 

### Calcul des zones d'influences :high_brightness:
La partition en cellules de Voronoi a été réalisée à l'aide la librairie de statistiques spatiales [```libpysal```](https://pysal.org/libpysal/). Les données démographiques disponibles à l'IRIS ont ensuite été agrégées pour obtenir un indicateur par cellule.

### Optimisation de l'implantation des centres :round_pushpin:
L'optimisation de localisation des centres revenant à effectuer des kmeans pondérés, nous avons utilisé [```sklearn```](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html).

### Isochrones :blue_car:
Un calcul du temps de trajet aux structures DGFIP a été expérimenté avec le moteur open-source [Valhalla](https://github.com/valhalla/valhalla) et la lirbrairie [```routingpy```](https://routingpy.readthedocs.io/en/latest/). Nous avons utilisé l'[image Docker](https://github.com/gis-ops/docker-valhalla) mise à disposition par gis-op.
Monter un serveur de calcul sur un ordinateur personnel étant gourmand en ressources, nous nous sommes limités à la Bretagne. Ce choix est motivé par deux raisons, par chauvinisme mais aussi pour éviter les effets de bord : les Finistérois ne peuvent en effet accéder qu'aux structures DGFIP de la région Bretagne et aucune autre. 

