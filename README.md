# SecDuck

## Shutdown Configurations

In `/boot/config.txt`, edit as the following

```
dtoverlay=gpio-shutdown,debounce=1000
```

And you can shutdown the RPi by holding GPIO3 for 1000 ms and boot it by pressing GPIO3.

## Read potentiometer's analog input via SPI

Enable SPI functionality by running

```
sudo raspi-config nonint do_spi 0
```

## Install OpenJtalk

```bash
sudo apt-get install open-jtalk
sudo apt-get install open-jtalk-mecab-naist-jdic
wget https://sourceforge.net/projects/mmdagent/files/MMDAgent_Example/MMDAgent_Example-1.8/MMDAgent_Example-1.8.zip/download -O MMDAgent_Example-1.8.zip
unzip MMDAgent_Example-1.8.zip MMDAgent_Example-1.8/Voice/*
sudo cp -r MMDAgent_Example-1.8/Voice/mei/ /usr/share/hts-voice
```
