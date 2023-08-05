# PiView

A Raspberry Pi system information package.

PiView provides the details of the Raspberry Pi currently being interrogated. 
System information that may be retrieved includes:

- **CPU**: load, temperature
- **GPU**: temperature
- **HARDWARE**: bluetooth, i2c, spi
- **HOST**: boot time, model, name, revision, serial number, uptime
- **MEMORY**: free, total, used
- **NETWORK**: host name, interface names, ip addresses, mac addresses
- **STORAGE**: total, free

Also includes a small utility library with:

- conversion of bytes into Kilobytes, Megabytes, Gigabytes and up
- create list with a quartet of integer numbers representing the IPv4 Address


## Acknowledgements

A very large thank you to Matt Hawkins upon whose code this package is based.
[https://www.raspberrypi-spy.co.uk/](https://www.raspberrypi-spy.co.uk/)

The original code may be found as
[mypi.py](https://github.com/tdamdouni/Raspberry-Pi-DIY-Projects/blob/master/MattHawkinsUK-rpispy-misc/python/mypi.py).



## Copyright

Copyright Adrian Gould, 2021-.
Licensed under the [Open Software License version 3.0](./LICENSE.txt)
