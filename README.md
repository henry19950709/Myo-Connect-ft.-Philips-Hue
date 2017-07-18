Use gesture recognition to control Philips Hue
Developed by Python
## Tools
* Myo Connect ([here](https://www.myo.com/))
* Philips Hue ([here](www2.meethue.com/))


## Installation
### Library Used
* phue
* myo-python

### Commands
	sudo pip install phue
	sudo pip install myo-python
	
or

	sudo easy_install phue
	sudo pip install myo-python
	
### SDK Used
[Myo SDK](https://developer.thalmic.com/downloads)
### Manually
The code is for only one Myo and one Philips Hue. Note that I initialize the myo in line 23 with the following one.

	import myo as libmyo; libmyo.init('/Users/henry/Desktop/myo/sdk/myo.framework')
	
Please pass the absolute path of the Myo sdk so that the initialization goes well.

##Example
