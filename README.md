# OptimisationFiscale

## Installation (in progress)
1. cloner le repo ``` git clone https://github.com/t-morvan/OptimisationFiscale.git ```
2. installer poetry https://python-poetry.org/docs/
3. faire ``` poetry install ```

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

## Données

Nous avons principalement utilisé des données démographiques issues du recensement de l'Insee ainsi que la base des quartiers politique de la ville.
L'ensemble des sources, url et licences utilisées sont rassemblées [ici](URLS.yaml).

## Outils
