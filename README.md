# OptimisationFiscale

## Installation  :wrench:
1. cloner le repo ``` git clone https://github.com/t-morvan/OptimisationFiscale.git ```
2. installer poetry https://python-poetry.org/docs/
3. ```cd``` dans le repo et faire ``` poetry install ```

4. optionnel (pour utiliser le backend vectorisé pygeos avec geopandas) : 
    ```
    poetry export --without-hashes --format requirements.txt --output requirements.txt
    sed -i -e 's/^-e //g' requirements.txt
    python -m pip install \
        --force-reinstall \
        --no-binary pygeos,shapely,rasterio,pyproj \
        -r requirements.txt
     ```  
    (cf https://github.com/python-poetry/poetry/issues/365)


5. lancer ```download.py```pour télécharger les fichiers
6. décompresser le shapefile des IRIS (avec 7zip par exemple)

## Données :floppy_disk:

Nous avons principalement utilisé des données démographiques issues du recensement de l'Insee ainsi que la base des quartiers politique de la ville.
L'ensemble des sources, url et licences utilisées sont rassemblées [ici](URLS.yaml).

## Outils :hammer:

### Calcul des distances et plus proches voisins
Nous avons utilisé le pendant spatial de pandas, [geopandas](https://geopandas.org/en/stable/), pour les manipulations spatiales. La volumétrie étant assez importante (>40 000 "quartiers" IRIS), nous avons eu recours à [pygeos](https://pygeos.readthedocs.io/en/stable/) pour vectoriser les opérations de géometrie. Nous avons pris le soin de convertir les données en projection [Lambert 93 ](https://fr.wikipedia.org/wiki/Projection_conique_conforme_de_Lambert) afin d'assurer la précision des calculs de distances et d'aires. 

### Calcul des zones d'influences

### Statistiques descriptives (non spatiales)

### Optimisation de l'implantation des centres

### Isochrones :blue_car:

