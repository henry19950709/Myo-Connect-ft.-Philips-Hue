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


### Example

### Functions
	#Make Philips hue with ID 3 turn on (False means turn off) 
	b.control_light(3,True)
	
	#Set the specific brightness to Hue with ID 3 with transition time 0.2s
	b.set_brightness(id,bright,2)
	
	#Set the specific color to Hue with ID 3 with transition time 0.2s
	b.set_color(id,color)
	
You can check the callback function on_pose(), I make some combination between hand gesture and actions applied to the Hue and You can fix iy to your own one.

### My Combinations
* wave_out: turn into next color
* wave_in: turn into previous color
* fist: darken the hue by 45 brightness
* fingers_spread: lighten the hue by 45 brightness
* double_tap: make hue close or open 
