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
