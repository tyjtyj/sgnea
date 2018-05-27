# SGNEA home-assistant


Home Assistant Custom Component to get now cast from Singapore National Enviroment Agency (SG NEA)


This file is modified from home assistant scraper.py


Home assistant
configuration.yaml file

With API key
- Get your API key from SG NEA from https://www.nea.gov.sg/api. Fill up your YOURAPIKEY

```
Sensor
  - platform: sgnea
    resource: http://api.nea.gov.sg/api/WebAPI/?dataset=2hr_nowcast&keyref=<YOURAPIKEY>
    name: 'SGNEA NowCast'
    select: 'area[name="YOURLOCATION"]'
    attribute: 'forecast'
```
Without API key
```
Sensor
  - platform: sgneaweb
    resource: http://www.nea.gov.sg/weather-climate/forecasts/2-hour-nowcast(optional)
    name: 'SGNEA NowCast'
    area: 'YOURLOCATION'
```


Location List:
- Replace YOURLOCATION with the locations below. Without APi key, replace space with _

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
