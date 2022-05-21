# Hackathon Open Data de la DGFiP

> La couverture du territoire par les structures DGFiP est-elle optimale et assure-t-elle un égal accès de tous au service public ?

A la première lecture de cette question, on peut se demander si l'implantation géographique des structures DGFiP importe encore à l'heure où l'accès au service public est de plus en plus en dématérialisé. 

Toutefois, l'idée selon laquelle *toutes les démarches* peuvent s'effectuer en ligne et *par tous* est à nuancer.
Le dernier [Insee focus](https://www.insee.fr/fr/statistiques/6438420) montre clairement qu'il existe une fracture numérique avec "un tiers des adultes [qui] ont renoncé à effectuer une démarche administrative en ligne en 2021". Concernant la DGFiP, même si le nombre de télé-déclarations des impôts a plus que doublé en dix ans, elles ne représentent que 61% des décarations selon cette même enquête.

De plus, on peut supposer que les demandes en ligne des habitants d'un département sont traitées par des agents des structures DGFIP du département en question.

La couverture du territoire par les structures DFIP est donc encore une probématique d'intérêt public que nous allons explorer dans ce projet. Nous nous sommes posés plusieurs questions auxquelles nous avons tenté d'apporter un éclairage quantitatif.

- Tous les départements sont-ils également en pourvus en structures DGFIP ? En nombre absolu et par habitant ? En termes de distance moyenne aux centres ?

- Les quartiers politique de la ville (QPV) sont-ils bien pourvus en structures DGFiP ?

- Quelle est le pourcentage d'un département situé à moins de 15 minutes en voitures d'un centre de Finances publiques ?

- Peut-on définir une zone d'influence d'une structure DGFiP et existe-t-il des disparités en termes de taille et caractéristiques socio-démographiques ?

- Comment re-localiser les centres de sorte à minimiser la distance aux utilisateurs ?


## Livrables

1. Un Dashboard Tableau présente la plupart des résulats obtenus[lien].
2. Des notebooks encore exploratoires sont disponibles dans [notebooks](notebooks/), notamment :
    - ```revenus.ipynb``` : les inégalités d'accès selon le revenu médian d'une commune.
    - ```professionnels.ipynb``` : distances des artisans, commerçants et chefs d'entreprise aux structures proposant un service pour professionnels.
3. Des fonctions pour lire, croiser et calculer des distances entre les IRIS/Communes et les structures DGFiP (cf documentation technique).
4. Un script [```optimloc.py```](dgfip/optimloc.py) pour calculer une re-localisation des structures DGFiP d'une zone avec un poids configurable pour chaque IRIS (population, population de 80 ans et + par exemple).


## Documentation technique

### Installation  :wrench:
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

### Documentation des fonctions
Toutes les fonctions possèdent une docstring et sont typées; une documentation automatique générée par [pdoc](https://pdoc3.github.io/pdoc/) est disponible dans ```doc/```
### Données

Nous avons principalement utilisé des données démographiques issues du recensement de l'Insee ainsi que la base des quartiers politique de la ville.
L'ensemble des sources, url et licences utilisées sont rassemblées [ici](URLS.yaml).


### Outils et méthodes

#### Statistiques descriptives (non spatiales) :bar_chart:
Toutes les manipulations non spatiales ont été réalisées avec [```pandas```](https://pandas.pydata.org/).

#### Calcul des distances et plus proches voisins 🗺️
Nous avons utilisé le pendant spatial de pandas, [```geopandas```](https://geopandas.org/en/stable/), pour les manipulations spatiales. La volumétrie étant assez importante (>40 000 "quartiers" IRIS), nous avons eu recours à [```pygeos```](https://pygeos.readthedocs.io/en/stable/) pour vectoriser les opérations de géometrie. Nous avons pris le soin de convertir les données en projection [Lambert 93 ](https://fr.wikipedia.org/wiki/Projection_conique_conforme_de_Lambert) afin d'assurer la précision des calculs de distances et d'aires. 

La distance moyenne aux structures DGFiP de type S au sein d'un département a été estimée par :
$$ \overline{D}(dep, S)  = \frac{1}{\sum_\limits{i \in IRIS(dep)} pop_i}  \sum_{i \in IRIS(dep)} pop_i  \times d(i, S)$$

où $d(i,S)$ est la distance de l'Iris i à la structure de type S la plus proche et $\text{pop}_i$ sa population 

(remarque: parfois la population est non exacte pour des soucis de secret mais c'est une première approximation).

#### Calcul des zones d'influences :high_brightness:
La partition en cellules de Voronoi a été réalisée à l'aide la librairie de statistiques spatiales [```libpysal```](https://pysal.org/libpysal/). Les données démographiques disponibles à l'IRIS ont ensuite été agrégées pour obtenir un indicateur par cellule.

#### Optimisation de l'implantation des centres :round_pushpin:
Pour optimiser la localisation des centres, nous avons choisi de minimiser le critère suivant :

$$ L(C) = \sum_{i \in IRIS} w_i d_2(i, C)^2$$

où $C=\{c_1,...,c_k\} \in \mathbb{R}^{2 \times k}$ est la localisation des centres, $d_2(i,C)$ est la distance euclidienne de l'Iris au point de C le plus proche et $w_i$ un poids à choisir; par exemple la population de l'IRIS, la population des retraités de l'IRIS ou une combinaison de ces populations. 

Cela revient exactement à effectuer des kmeans pondérés et nous avons donc utilisé [```sklearn```](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html).

#### Isochrones :blue_car:
Un calcul du temps de trajet aux structures DGFIP a été expérimenté avec le moteur open-source [Valhalla](https://github.com/valhalla/valhalla) et la lirbrairie [```routingpy```](https://routingpy.readthedocs.io/en/latest/). Nous avons utilisé l'[image Docker](https://github.com/gis-ops/docker-valhalla) mise à disposition par gis-op.
Monter un serveur de calcul sur un ordinateur personnel étant gourmand en ressources, nous nous sommes limités à la Bretagne. Ce choix est motivé par deux raisons, par chauvinisme mais aussi pour éviter les effets de bord : les Finistérois ne peuvent en effet accéder qu'aux structures DGFIP de la région Bretagne et aucune autre. 

