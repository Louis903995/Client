I. Automatiser l’extraction des données

A. Contexte du projet

Le projet "Ticket Classification" vise à classer automatiquement les produits figurant sur un ticket de caisse d’une enseigne alimentaire.
L’utilisateur scanne son ticket, puis voit apparaître la liste de ses produits organisés en une dizaine de catégories couramment utilisées dans un supermarché, telles que : fruits et légumes, viandes et charcuterie, poissons et fruits de mer, épicerie sucrée, épicerie salée, boissons non alcoolisées, boissons alcoolisées, produits ménagers, etc.

Cette classification permet au client de visualiser, de manière intuitive, ses achats répartis par type de produit, même dans les cas où le supermarché ne fournit pas ce détail sur le ticket.

De plus, l’utilisateur peut définir un budget mensuel. À chaque dépense enregistrée, le système lui indique où il en est par rapport à ce budget. Un indicateur visuel simple permettra au client de savoir si ce budget sera respecté ou dépassé.

En somme, le client disposera d’une vision claire de la répartition de ses dépenses alimentaires ou ménagères, saura où il en est dans le respect de son budget et bénéficiera d’une estimation de ses dépenses pour les semaines à venir.




B. Spécifications techniques

Le projet est développé en Python pour la mise en œuvre des traitements, des modèles de classification et des prédictions.
L’hébergement des bases de données, le déploiement des API ainsi que le monitoring de l’application sont assurés via la plateforme Azure. Les données sont stockées dans une base SQL hébergée sur Azure, garantissant fiabilité et disponibilité.

La solution est conteneurisée à l’aide de Docker afin d’assurer la portabilité de l’environnement et de simplifier les déploiements. Un système de monitoring intégré permet de suivre l’état de l’application en temps réel et d’anticiper les anomalies.

Le code est rédigé dans Visual Studio Code et versionné sur un dépôt GitHub, facilitant la gestion des versions et la collaboration au sein de l’équipe.

Sur le plan algorithmique, le projet intègre plusieurs approches d’intelligence artificielle :

NLP (Natural Language Processing) pour analyser et catégoriser les libellés produits présents sur les tickets.

Reconnaissance d’images pour extraire automatiquement les informations à partir des tickets scannés.

Modèles de séries temporelles pour prédire les dépenses futures des utilisateurs à partir de leur historique.



C. Extraction des données








II. Développer des requêtes de type SQL d’extraction des données


III. Développer des règles d'agrégation de données issues de différentes sources


IV. Créer une base de données



V. Développer une API mettant à disposition le jeu de données


Annexes