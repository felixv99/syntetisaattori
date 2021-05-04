# Syntetisaattori

## Esittely

Ohjelma on digitaalinen syntetisaattori, joka toimii kahden oskillaattorin avulla. Kummastakin oskillaattorista pystyy säätämään signaalin aallon tyyppiä, oktaavia ja äänenvoimakkuuta. Lisäksi löytyy vaippa-säätimet (ADSR envelope), pää äänenvoimakkuuden säädin ja alipäästö-suodatin. Luodut äänet on mahdollista tallentaa ja ladata.

## Tiedosto- ja kansiorakenne
- Synthesizer -kansiosta löytyy ohjelman python tiedostot, sekä muutama valmiiksi tallennettu esi-asetus
- Documentation -kansiosta löytyy projektin suunnitelma ja dokumentaatio

## Asennusohje
- Pythonin versio täytyy olla [3.6.8]()https://www.python.org/downloads/release/python-368/)
- Tarvittavat Kirjastot:

| Kirjasto | Asennus komento |
| ------ | ------ |
| [PyAudio](https://pypi.org/project/PyAudio/) | pip install PyAudio |
|[Numpy](https://pypi.org/project/numpy/) | pip install numpy |
| [Matplotlib](https://pypi.org/project/matplotlib/) | pip install matplotlib |
|[Scipy.signal](https://pypi.org/project/scipy/) | pip install scipy |
|[PyQt](https://pypi.org/project/PyQt5/) | pip install PyQt5 |
- Lisäksi pythonin omat kirjastot: os, time, threading, sys, math, unittest (Ei tarvitse erillistä asennusta)

## Käyttöohje

- Ohjelma käynnistetään ajamalla soundout.py


- Syntetisaattori soittaa eri taajuuksista ääntä painamalla näppäimistön näppäimiä:
	(a,w,s,e,d,f,t,g,y,h,u,j)
- Kun käynnistät ohjelman kannattaa aloittaa pää-äänenvoimakkuuden (MASTER VOLUME) säätämisellä,
	kuunnellen äänenvoimakkuutta painamalla jotain yllämainitsemista näppäimistä.
- Sen jälkeen voit säädellä säätimiä missä tahansa järjestyksessä:
- Vaihda oskillaattoreiden aallon muotoa WAVE-liukusäätimistä
- Vaihda oskillaattoreiden oktaavia OCTAVE-liukusäätimistä
- Vaihda oskillaattoreiden äänenvoimakkuutta VOL1- ja VOL2-säätimistä
- Muuta amplitudin käyttäytymistä ATTACK, DECAY, SUSTAIN ja RELEASE-säätimistä
- Aseta alipäästösuodattimen rajataajuus LOW PASS FILTER-säätimestä
- Kun haluat tallentaa tekemäsi äänen, paina Save-painiketta ja tallenna tiedosto preset-kansioon
- Kun haluat ladata tekemäsi äänen, paina Load-painiketta ja etsi tallentamasi tiedosto preset-kansiosta
- Poistu ohjelmasta painamalla Exit-painiketta tai painamalla ruksia oikeassa yläkulmassaälkeen lisäsin suunnitelmaan presettien tallennuksen ja latauksen (5h)