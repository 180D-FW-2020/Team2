# Hardware Matrix Setup
LED Matrix -> RPi [(RPi pinout)](https://pinout.xyz/)
```
VCC->GPIO Pin #2 (5v)
GND->GPIO Pin #6 (GND)
DIN->GPIO Pin #19
CS ->GPIO Pin #24
CLK->GPIO Pin #23
```

# Software Matrix Setup
Link to [documentation](https://luma-led-matrix.readthedocs.io/en/latest/install.html) by Richard Hull

## Pre-requisite RPi Installation
1. Run `sudo raspi-config`
2. Use the down arrow to select `5 Interfacing Options`
3. Arrow down to `P4 SPI`
4. Select **yes** when it asks you to enable SPI
5. Also select **yes** when it asks about automatically loading the kernel module
6. Use the right arrow to select the **<Finish>** button
7. Reboot `sudo reboot`

After rebooting re-check that the `lsmod | grep -i spi` command shows whether SPI driver is loaded before proceeding.\
Depending on the hardware/kernel version, this may report **spi_bcm2807** rather than **spi_bcm2835** - either should be adequate. 

And to verify that the devices are successfully installed in `/dev`:
```
$ ls -l /dev/spi*
crw------- 1 root root 153, 0 Jan  1  1970 /dev/spidev0.0
crw------- 1 root root 153, 1 Jan  1  1970 /dev/spidev0.1
```

## Installing from PyPi
Install the dependencies for library first with:
```
$ sudo usermod -a -G spi,gpio pi
$ sudo apt install build-essential python3-dev python3-pip libfreetype6-dev libjpeg-dev libopenjp2-7 libtiff5
```
Make sure `pip` and `setuptools` are up to date by upgrading them first:
```
$ sudo -H pip install --upgrade --ignore-installed pip setuptools
```
Proceed to install latest version of the luma.led_matrix library directly from PyPI:
```
$ sudo -H pip install --upgrade luma.led_matrix
```

## Testing the matrix
Ensure you have followed the installation instructions above. Clone the [repo](https://github.com/rm-hull/luma.led_matrix) from Github, and run the example code as follows:
```
$ python examples/matrix_demo.py
```
For more details, refer to the [documentation](https://luma-led-matrix.readthedocs.io/en/latest/install.html) by Richard Hull
