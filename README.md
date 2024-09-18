# Alegria 777 game like

## Contexte

Il s'agit d'un jeu de bandit manchot "humain" avec quelques effets lumineux et sonores.  

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

On fait en sorte que le raspberry puisse être éteint/allumé avec un bouton physique connecté aux broches 5 et 6.  

```sh
sudo echo "dtoverlay=gpio-shutdown" >> /boot/firmware/config.txt
sudo reboot
```

### Réseau

Le raspberry pi 0 met à disposition un access point sur lequel l'ESP32 se connecte.  
Cela permet à l'ensemble de fonctionner sans pré-requis sur place.  
Le SSID monté par le RPI est : "banditmanchot".

```sh
sudo nmcli connection add type wifi ifname wlan0 con-name hotspot autoconnect yes ssid banditmanchot
sudo nmcli connection modify hotspot 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared
sudo nmcli connection modify hotspot wifi-sec.key-mgmt wpa-psk
sudo nmcli connection modify hotspot wifi-sec.psk jesusrevient
sudo nmcli connection down preconfigured
sudo nmcli connection up hotspot
```

### Programme principal sur le raspberry

**Installation**

```sh
sudo apt update
sudo apt install git python3-yaml python3-pip python3-gpiozero python3-pygame
```

```sh
git clone https://github.com/mmourcia/alegria.git
cd alegria
sudo cp contrib/alegria.service /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/alegria.service 
sudo systemctl daemon-reload
sudo systemctl enable alegria.service
sudo systemctl start alegria.service
```


### Image WLED sur l'ESP32

L'image a été déployée depuis l'installeur web fourni par WLED.  

L'ensemble des presets est disponible dans le répertoire [wled_presets](./wled_presets).  
