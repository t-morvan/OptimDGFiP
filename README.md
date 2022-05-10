# OptimisationFiscale

## Installation (in progress)
1. cloner le repo ``` git clone https://github.com/t-morvan/OptimisationFiscale.git ```
2. installer poetry https://python-poetry.org/docs/
3. faire ``` poetry install ```

4. optionnel (pour utiliser le backend vectorisé pygeos avec geopandas) : 
```poetry export --without-hashes --format requirements.txt --output requirements.txt
sed -i -e 's/^-e //g' requirements.txt
python -m pip install \
    --force-reinstall \
    --no-binary pygeos,shapely,rasterio,pyproj \
    -r requirements.txt
 ```  
(cf https://github.com/python-poetry/poetry/issues/365)

## Données

### Données socio-économiques

- Recensensement de population (à l'Iris) : https://www.insee.fr/fr/statistiques/4799309
- Revenus, pauvreté et niveau de vie en 2019 (à l'Iris) : https://www.insee.fr/fr/statistiques/6049648#dictionnaire
- Population couverte par au moins une prestation de la CAF (par commune)  http://data.caf.fr/dataset/population-des-foyers-allocataires-par-commune

### Données géographiques 
- Structures DGFIP : https://data.economie.gouv.fr/explore/dataset/coordonnees-des-structures-dgfip/table/?disjunctive.type_de_service&disjunctive.departement&disjunctive.dep_name&disjunctive.reg_name&disjunctive.public&disjunctive.service
- IRIS : https://www.geoportail.gouv.fr/donnees/iris
- Quartiers prioritaires de la politique de la ville (QPV) :  https://www.data.gouv.fr/en/datasets/quartiers-prioritaires-de-la-politique-de-la-ville-qpv/


## Outils

- Calcul de temps de trajets en voiture : https://github.com/gis-ops/routing-py
- Carte d'accessbilité : https://nbviewer.org/github/pysal/access/blob/master/notebooks/How%20to%20Use%20access%20to%20Compute%20Access%20Scores%20to%20Resources%20Given%20XY%20Coordinates%20Joined%20to%20Census%20Tracts.ipynb
