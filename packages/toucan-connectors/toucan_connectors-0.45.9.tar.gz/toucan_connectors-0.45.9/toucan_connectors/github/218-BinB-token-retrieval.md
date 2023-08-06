# PAT 218 - Business in a Box Token retrieval

## Résumé
Au vu de la nouvelle architecture Business in a Box, les scripts d'extraction de données schedulés auront besoin d'obtenir les tokens utilisateur pour s'authentifier auprès des différentes API (Aircall, Github, ....).  


## Besoins
Il faut qu'à chaque execution de l'extraction, à fréquence journalière ou plus élevée, le script appelé ait un token valide pour s'authentifier.


## Rationale & Implémentation
### Implémentation dans Laputa


Le service d’extraction a un user superadmin spécifique qui permet d’accéder à la route suivante :

*GET laputa/<app-id>/<connector-type>/binb-token*

La fonctionnalité de cette nouvelle route est : 
 - Récupérer un nouveau token valide qui pourra être rafraîchit si besoin
 - Le renvoyer au script d'extraction

Dans la code base: 
- Tests à implémenter dans : *tests/api*
- La route est à écrire dans *api/resources/binb_token.py* et à déclarer dans le fichier *routes.py* via la fonction add_smallapp_resource.
- Nouvelle classe BinBToken implémente une méthode GET qui fait le refresh et sert le token, la classe BinBToken.get doit être accessible seulement par un super admin (décorateur)
- La route connaît le type de connecteur à instancier pour la exécuter la mécanique de récupération du token. Elle instancie ensuite un secrets keeper qui permettra d’obtenir le token via la méthode retrieve_token


La mécanique de Signup serait conservée en l'état (fonctionnelle mais pas très propre) et les développement seraient moins couteux. 

![Extraction Architecture](./binbtoken.png)


### Implementation en mode IDP/SP

- Ajouter un service d'IDP parallèle à Laputa (possible augmentation de la surface d'exposition)
- Durant le Signup Business in a Box, l'utilisateur est enregistré auprès de ce service
- Le service porte les secrets d'accès à l'API tierce (client_id/client_secret)
- Laputa est un service provider enregistré auprès de cet IDP (pour que la danse oAuth puisse s'effectuer)
- Le service d'extraction est aussi un service provider enregistré auprès de l'IDP et peut ainsi récupérer 


La mécanique serait un peu plus complexe et les coûts de dévelopements plus lourds mais permettrait d'aller vers la nouvelle architecture "multi-tenant".