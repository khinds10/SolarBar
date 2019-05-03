# Sunrise Alarm Clock
Schedule your own personal sunrise, improves morning wakefulness

![Finished](https://raw.githubusercontent.com/khinds10/SolarBar/master/construction/build-images/finished.png "Finished")

#### Flashing RaspberriPi Hard Disk / Install Required Software (Using Ubuntu Linux)

Download "RASPBIAN JESSIE LITE"
https://www.raspberrypi.org/downloads/raspbian/

**Create your new hard disk for DashboardPI**
>Insert the microSD to your computer via USB adapter and create the disk image using the `dd` command
>
> Locate your inserted microSD card via the `df -h` command, unmount it and create the disk image with the disk copy `dd` command
>
> $ `df -h`
> */dev/sdb1       7.4G   32K  7.4G   1% /media/XXX/1234-5678*
> a
> $ `umount /dev/sdb1`
>
> **Caution: be sure the command is completely accurate, you can damage other disks with this command**
>
> *if=location of RASPBIAN JESSIE LITE image file*
> *of=location of your microSD card*
>
> $ `sudo dd bs=4M if=/path/to/raspbian-jessie-lite.img of=/dev/sdb`
> *(note: in this case, it's /dev/sdb, /dev/sdb1 was an existing factory partition on the microSD)*

**Setting up your RaspberriPi**

*Insert your new microSD card to the raspberrypi and power it on with a monitor connected to the HDMI port*

Login
> user: **pi**
> pass: **raspberry**

Change your account password for security
>`sudo passwd pi`

Enable RaspberriPi Advanced Options
>`sudo raspi-config`

Choose:
`1 Expand File System`

`9 Advanced Options`
>`A2 Hostname`
>*change it to "SOLARLAMP"*
>
>`A4 SSH`
>*Enable SSH Server*
>
>`A7 I2C`
>*Enable i2c interface*
>
>`P4 SPI`
>*Enable/Disable automatic loading of SPI kernel module*
>

**Enable the English/US Keyboard**

>`sudo nano /etc/default/keyboard`

> Change the following line:
>`XKBLAYOUT="us"`

**Reboot PI for Keyboard layout changes / file system resizing to take effect**
>$ `sudo shutdown -r now`

**Auto-Connect to your WiFi**

>`sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`

Add the following lines to have your raspberrypi automatically connect to your home WiFi
*(if your wireless network is named "linksys" for example, in the following example)*

	network={
	   ssid="linksys"
	   psk="WIRELESS PASSWORD HERE"
	}

**Reboot PI to connect to WiFi network**

>$ `sudo shutdown -r now`
>
>Now that your PI is finally on the local network, you can login remotely to it via SSH.
>But first you need to get the IP address it currently has.
>
>$ `ifconfig`
>*Look for "inet addr: 192.168.XXX.XXX" in the following command's output for your PI's IP Address*

**Go to another machine and login to your raspberrypi via ssh**

> $ `ssh pi@192.168.XXX.XXX`

**Start Installing required packages**

>$ `sudo apt-get update`
>
>$ `sudo apt-get upgrade`
>
>$ `sudo apt-get install memcached vim git python-gpiozero python-smbus i2c-tools python-imaging python-smbus build-essential python-dev rpi.gpio python3 python3-pip python-memcache python3-spidev python-spidev`

**Update local timezone settings

>$ `sudo dpkg-reconfigure tzdata`

`select your timezone using the interface`

**Setup the simple directory `l` command [optional]**

>`vi ~/.bashrc`
>
>*add the following line:*
>
>`alias l='ls -lh'`
>
>`source ~/.bashrc`

**Fix VIM default syntax highlighting [optional]**

>`sudo vi  /etc/vim/vimrc`
>
>uncomment the following line:
>
>_syntax on_

**Install i2c Python Drivers**

Install the NeoPixel Driver as follows 

>`sudo apt-get install build-essential python-dev git scons swig`
>
>`sudo pip3 install --upgrade setuptools`
>
>`sudo pip3 install rpi_ws281x`
>
>`cd rpi_ws281x`
>
>`scons`
>
>`cd python`
>
>`sudo python setup.py install`
>
>`cd examples/`
>
>`sudo python strandtest.py`

# Supplies Needed

**5V Power Supply**

![5V Power Supply](https://raw.githubusercontent.com/khinds10/SolarBar/master/construction/5VPowerSupply.png "5V Power Supply")

**I2C 7 SEGMENT**

![I2C 7 SEGMENT](https://raw.githubusercontent.com/khinds10/SolarBar/master/construction/i2C7Segment.png "I2C 7 SEGMENT")

**Microchip MCP3008**

![Microchip MCP3008](https://raw.githubusercontent.com/khinds10/SolarBar/master/construction/MCP3008.png "Microchip MCP3008")

**Momentary Tactile Tact Push Button Switch [x5]**

![Momentary Tactile Tact Push Button Switch](https://raw.githubusercontent.com/khinds10/SolarBar/master/construction/MomentaryPushButton.png "Momentary Tactile Tact Push Button Switch")

**PI ZERO W**

![PI ZERO W](https://raw.githubusercontent.com/khinds10/SolarBar/master/construction/PiZero.jpg "PI ZERO W")

**Logarithmic Slide Potentiometer**

![Logarithmic Slide Potentiometer](https://raw.githubusercontent.com/khinds10/SolarBar/master/construction/Potentiometer.jpg "Logarithmic Slide Potentiometer")

**WS2812B Individually Addressable RGB LED Strip [x4]**

![WS2812B Individually Addressable RGB LED Strip](https://raw.githubusercontent.com/khinds10/SolarBar/master/construction/WS2812B.png "WS2812B Individually Addressable RGB LED Strip")

**Thin Plexi Glass Sheet**

![Plexi Glass](https://raw.githubusercontent.com/khinds10/SolarBar/master/construction/build-images/plexi-glass.png "Plexi Glass")

**Frosted Spray Paint**

![Frosted Spray Paint](https://raw.githubusercontent.com/khinds10/SolarBar/master/construction/build-images/frosted-paint.png "Frosted Spray Paint")

### Wiring the Components

**Build Wood Frame**

I've built a wooden frame for the LED strips to be enclosed in and painted it black.

![Build Wood Frame](https://raw.githubusercontent.com/khinds10/SolarBar/master/construction/build-images/build-wood-frame.jpg "Build Wood Frame")

**Paint Plexi Glass**

With some frosted spray paint, paint the glass so that it defuses the light from the strips.

![Paint Plexi Glass](https://raw.githubusercontent.com/khinds10/SolarBar/master/construction/build-images/paint-plexi-glass.jpg "Paint Plexi Glass")

**Mount Strips**

Using simple tape and the stickiness of the backside of the LED strips, mount the 4 strips to the wooden base

![Mount Strips](https://raw.githubusercontent.com/khinds10/SolarBar/master/construction/build-images/mount-strips.jpg "Mount Strips")

**Mount Buttons**

![Mount Buttons](https://raw.githubusercontent.com/khinds10/SolarBar/master/construction/build-images/mount-buttons.jpg "Mount Buttons")

**Mount Buttons on Panel**

![Mount Buttons on Panel](https://raw.githubusercontent.com/khinds10/SolarBar/master/construction/build-images/mount-buttons-panel.jpg "Mount Buttons on Panel")

**Mount Chip on the Slider**

![Mount Chip on the slider](https://raw.githubusercontent.com/khinds10/SolarBar/master/construction/build-images/mount-chip-slider.png "Mount Chip on the slider")

**Wire Panel**

![Wire Panel](https://raw.githubusercontent.com/khinds10/SolarBar/master/construction/build-images/wire-panel.jpg "Wire Panel")

**Wire Pi**

![Wire Pi](https://raw.githubusercontent.com/khinds10/SolarBar/master/construction/build-images/wire-to-pi.jpg "Wire Pi")

**Mount Panel**

![Mount Panel](https://raw.githubusercontent.com/khinds10/SolarBar/master/construction/build-images/mount-panel.jpg "Mount Panel")

**Apply Plexi Glass**

![Apply Plexi Glass](https://raw.githubusercontent.com/khinds10/SolarBar/master/construction/build-images/apply-plexi-glass.jpg "Apply Plexi Glass")

**Mount on the Wall**

![Mount on the Wall](https://raw.githubusercontent.com/khinds10/SolarBar/master/construction/build-images/mount-on-wall.jpg "Mount on the Wall")

![Mount on the Wall](https://raw.githubusercontent.com/khinds10/SolarBar/master/construction/build-images/mount-on-wall2.jpg "Mount on the Wall")

## Print the Enclosure panels

## Build the Solar Lamp

### Set pi user crontab 

Enter the following line for a minute by minute crontab

`$ crontab -e`

`0 3 * * * python /home/pi/SolarBar/Alarm.py > /dev/null 2>&1`
`@reboot python /home/pi/SolarBar/Buttons.py > /dev/null 2>&1`
`@reboot python /home/pi/SolarBar/ControlPanel.py > /dev/null 2>&1`
`@reboot python /home/pi/SolarBar/Slider.py > /dev/null 2>&1`

### Set root user crontab (this library requires root access)

Set "on reboot" to run the candle python script forever

`$ sudo su`

`$ crontab -e`

`@reboot python /home/pi/SolarBar/LEDs.py > /dev/null 2>&1`

# Finished!

![Finished](https://raw.githubusercontent.com/khinds10/SolarBar/master/construction/build-images/finished.png "Finished")


