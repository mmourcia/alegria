# Alegria 777 game like

## Contexte

Il s'agit d'un jeu de 777 "humain" avec quelques effets lumineux et sonores.  

![Le concept](./img/concept.png)

## Fonctionnement du jeu

* Boite à boutons + animations sonores et LED.

## Architecture

* Raspberry pi 0 2w pour le programme principal + gestion du son
* ESP32 Wled pour piloter les rubans LED

### Hardware

| Item                         | Photo                                          | Description |
| ---------------------------- | ---------------------------------------------- | ----------- |
| Raspberry pi 2 W             | ![raspberry pi 0 2w](./img/raspberrypi02w.jpg) | Carte principale |
| Carte son USB                | ![usb sound card](./img/usbsoundcard.jpg)      | Le Pi 0 ne spossède pas de carte intégrée |
| Cable micro USB              | ![Micro USB](./img/micro_usb.jpg)              | Convertisseur Micro USB -> USB A femelle  |
| Boutons jeu                  | | |
| Boutons pédale               | | |
| Connecteurs Jack 3,5mm       | | |
| Connecteur alimentation      | | |
| Cable jack 3,5mm mâle mâle   | | |
| ESP32                        | | |
| Rubans LED                   | | |
| Boite en bois 40x20x10 cm    | | |


## Montage

### Boite à boutons

![boite](./img/boite-bouttons.png)


| Bouton        | GPIO | Fonction                                                     |
| ------------- | ---- | ------------------------------------------------------------ |
| Rouge         | 17   | Déclenchement d'une animation WLED rouge + sons associés     |
| Bleu          | 4    | Déclenchement d'une animation WLED bleue + sons associés     |
| Jaune         | 27   | Déclenchement d'une animation WLED jaune + sons associés     |
| Pédale Succès | 23   | Déclencement d'une animation WLED de succès + sons associés  |
| Pédale Echec  | 24   | Déclencement d'une animation WLED d'echec  + sons associés   |

## Logiciels

### Système

* OS Raspberry pi OS 64 bits sans desktop 
* Sélection de la carte son USB via raspi-config

![usbsoundcardselect.png](./img/usbsoundcardselect.png)

### Réseau

Le raspberry pi 0 met à disposition un access point sur lequel l'ESP32 se connecte.  
Cela permet à l'ensemble de fonctionner sans pré-requis sur place.  
Le SSID monté par le RPI est : "banditmanchot" mais il est caché. 

```sh
sudo nmcli dev wifi hotspot ifname wlan0 ssid banditmanchot password jesusrevient
```

```sh
$ nmcli connection show
NAME           UUID                                  TYPE      DEVICE 
preconfigured  e0698bcc-307b-4008-8467-273b2787a0f7  wifi      wlan0  
lo             fccb0b26-68a2-4f85-96df-21324d617698  loopback  lo     
Hotspot        9d1cf409-2073-495d-9068-0f9b8c476b81  wifi      --   
```

Puis supprimer l'autoconnect sur la connexion wifi de base 

```sh
sudo nmcli connection modify preconfigured connection.autoconnect no
```


Puis adresse ipv4 statique : /etc/NetworkManager/system-connections/Hotspot.nmconnection

```
[ipv4]
method=manual
addresses1=192.168.147.1/24
```

### Programme principal sur le raspberry

**Installation**

```
sudo apt install git python3-yaml python3-pip python3-gpiozero python3-pygame
```

```
sudo cp contrib/alegria.service /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/alegria.service 
sudo systemctl daemon-reload
sudo systemctl enable alegria.service
sudo systemctl start alegria.service
```


### Image WLED sur l'ESP32

L'image a été déployée depuis l'installeur web fourni par WLED.  

L'ensemble des presets est disponible dans le répertoire [wled_presets](./wled_presets).  
