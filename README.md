API stopped working since 2020. No update from regarding this. 

# SGNEA home-assistant


Home Assistant Custom Component to get now cast from Singapore National Enviroment Agency (SG NEA)


This file is modified from home assistant scraper.py


Home assistant
configuration.yaml file

```
sensor:
  - platform: sgnea
    name: 'SGNEA NowCast'
    area: 'YOURLOCATION'
```


Location List:
- Replace YOURLOCATION with the locations below. 

```
Ang Mo Kio
Bedok
Bishan
Boon Lay
Bukit Batok
Bukit Merah
Bukit Panjang
Bukit Timah
Central Water Catchment
Changi
Choa Chu Kang
Clementi
City
Geylang
Hougang
Jalan Bahar
Jurong East
Jurong Island
Jurong West
Kallang
Lim Chu Kang
Mandai
Marine Parade
Novena
Pasir Ris
Paya Lebar
Pioneer
Pulau Tekong
Pulau Ubin
Punggol
Queenstown
Seletar
Sembawang
Sengkang
Sentosa
Serangoon
Southern Islands
Sungei Kadut
Tampines
Tanglin
Tengah
Toa Payoh
Tuas
Western Islands
Western Water Catchment
Woodlands
Yishun
```
