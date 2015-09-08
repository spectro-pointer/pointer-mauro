# spectro-pointer


Le Spectro-Pointer est un dispositif optique et mécanique, contrôlé par un software open source en cours de développement.

### Fonction du dispositif :

La finalité de cet instrument est de pouvoir repérer dans le ciel, de manière automatique, toute lumière d'origine inconnue, en mouvement ou statique, d'en effectuer une prise d'image et de signature spectrale et finalement de comparer celle-ci avec l'actuelle base de données de signatures spectrales.

Base de données de signatures spectrales : <http://www.ifa.org.ar/espectros.html>

### Antécédents :

Le premier prototype du Spectro-Pointer a été installé à l'aéroport international de San Carlos de Bariloche, en Patagonie argentine. Il fonctionne manuellement, dans toutes les conditions climatiques.

<http://www.ifa.org.ar/proyectos.html>


### Défi à relever :

a) Le processus actuel est complètement manuel et nécessite la présence physique d'un opérateur. Comme les phénomènes lumineux peuvent se produire à n'importe quel moment, il est bien évidemment nécessaire d'automatiser le système de repérage et de focalisation de ces lumières, pour pouvoir en suivre les mouvements et les prendre en photo.

b) La deuxième étape de ce développement sera l'automatisation du processus de comparaison avec la base de données de signatures spectrales déjà identifiées.

## Configuration du client (testé sous Ubuntu 14.04)

 Pour le bon fonctionnement des programmes mentionnés ci-dessus, il faut d'abord installer, sur le client et sur le server, le script suivant :
```
git clone https://git.fixme.ch/gustavo/spectro-pointer.git && sudo ./spectro-pointer/extra/opencv3.0+gstreamer1.0.sh

```
Pour exécuter l'interface graphique sur le client il faut se connecter sur le réseau Wi-Fi Spectro-Pointer (sans mot de passe), puis exécuter:
```
sudo ./spectro-pointer/gui/pointer/pointer_gui.py
```

À l'heure actuelle, le spectro-pointer n'arrive pas à centrer la lumière sur l'entrée de la fibre optique. Il faut donc régler manuelleme en utilisant l'interface graphique du logiciel colimacion.py:
```
sudo ./spectro-pointer/gui/pointer/colimacion.py
```

## Debug
Si le serveur est éteint voici la procédure à suivre pour le démarrer:

1. Se connecter sur le réseau Wi-Fi spectro-pointer
2. Se connecter via SSH sur le serveur (password: password)
> ssh pi@192.168.0.100
3. sudo ./pointer/rtsp-opencv/gs-server.sh
4. Se connecter sur l'autre serveur et reproduire la même procédure que sur le premier serveur, puis
> sudo ./pointer/pointer serve
