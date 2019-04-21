# SolarBar
Sunlight simulator, sunrise sunset simulator for seasonal depression

>$ `sudo apt-get install memcached vim git python-smbus i2c-tools python-imaging python-smbus build-essential python-dev rpi.gpio python3 python3-pip python-memcache`


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

remember you have to include the rpi_ws281x.zip which you upzip to install, it's not working other wise

user crontab 

0 3 * * * python /home/pi/SolarBar/Alarm.py > /dev/null 2>&1
@reboot python /home/pi/SolarBar/Buttons.py > /dev/null 2>&1
@reboot python /home/pi/SolarBar/ControlPanel.py > /dev/null 2>&1
@reboot python /home/pi/SolarBar/Slider.py > /dev/null 2>&1


root crontab

@reboot python /home/pi/SolarBar/LEDs.py > /dev/null 2>&1


