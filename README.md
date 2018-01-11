# home-assistant-sgnea
Home Assistant Custom Component to get now cast from Singapore National Enviroment Agency (SG NEA)

Home assistant
configuration.yaml file

This file is modified from home assistant scraper.py

Sensor
  - platform: sgnea
    resource: http://api.nea.gov.sg/api/WebAPI/?dataset=2hr_nowcast&keyref=<YOURAPIKEY>
    name: 'SGNEA NowCast'
    select: 'area[name="YOURLOCATION"]'
    attribute: 'forecast'
    
1. Get your API key from SG NEA from https://www.nea.gov.sg/api
   Fill up your YOURAPIKEY

2.Replace YOURLOCATION with the locations below

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
