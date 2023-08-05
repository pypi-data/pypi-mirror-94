# PiView

A Raspberry Pi system information package.

Provides the details of the Raspberry Pi currently being interrogated. Details that may be 
retrieved include:

- **CPU**: load, temperature
- **GPU**: temperature
- **HARDWARE**: bluetooth, i2c, spi
- **HOST**: boot time, model, name, revision, serial number, uptime
- **MEMORY**: free, total, used
- **NETWORK**: host name, interface names, ip addresses, mac addresses
- **STORAGE**: total, free

Also includes a small utility library with:

- conversion of bytes into KiloBytes, MegaBytes, GigaBytes and up
- create list with a quartet of integer numbers representing the IPv4 Address



## Copyright

Copyright Adrian Gould, 2021-.
Licensed under the [Open Software License version 3.0](./LICENSE.txt)
