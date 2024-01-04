# RGB Matrix LED - Games

## Requirements

- Adafruit RGB Matrix LED (_min. 1x 64x32_)
- Adafruit RGB Matrix Bonnet for Raspberry Pi
- Raspberry Pi (_min. Zero WH_)
- USB adapter (_USB to Micro USB_)

## Installation

In case your RGB Matrix LED installation is already done, you only need to ensure `Python evdev` and `git` is installed.

```shell
# change to home directory (optional)
$ cd ~

# update packages (optional)
$ sudo apt update && sudo apt upgrade -y

# get rgb matrix installation script
$ curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/main/rgb-matrix.sh >rgb-matrix.sh

# run installation
$ sudo bash rgb-matrix.sh
```

> Please be patient with your installation! This task can take some time. Also verify that installation was successful before you continue.

```shell
# install needed python packages and git
$ sudo apt install -y git python3-evdev
```

Done ... now clone the repository and enjoy the games.

```shell
# clone repository
$ git clone https://github.com/Lupin3000/RGB-Matrix-LED.git

# change into repository directory
$ cd RGB-Matrix-LED/
```

## Controller

To ensure your controller is connected and can be used, verify the input devices.

> In case the input will not be discovered, please check your USB cable and USB port on Raspberry Pi!

```shell
# verify current input devices (optional)
$ ls -la /dev/input/
```

Because you should run the Python scripts with `sudo` permission, it's good to add the root user into `input` group. Otherwise, it will show error messages.

```shell
# add root to input group
$ sudo usermod -a -G input root
```

> Inside directory `usb` are some files to help with your controller. In case you don't have same you can use these scripts, to configure any other brand. But also adaptations inside `lib/stadia_controller` will be needed!

## Execute games

All games are started very similar:

```shell
# run Pong
$ sudo python -B Pong.py

# run Snake
$ sudo python -B Snake.py
```

## Participate the project

You are very welcome to take part in this project! No matter whether you want to develop new games or expand / optimize existing games. There are very few rules:

- Games must be developed in MicroPython
- No insults are allowed
- The code should be at least somewhat documented (e.g. DocStrings)
- Anyone who destroys something has to fix it again
