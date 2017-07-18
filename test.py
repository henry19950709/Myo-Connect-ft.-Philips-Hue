# Copyright (c) 2015  Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import print_function

import myo as libmyo; libmyo.init('/Users/henry/Desktop/myo/sdk/myo.framework')
import time
import sys
from phue import Bridge


class Listener(libmyo.DeviceListener):
    """
    Listener implementation. Return False from any function to
    stop the Hub.
    """

    interval = 0.05  # Output only 0.05 seconds

    def __init__(self):
        super(Listener, self).__init__()
        self.orientation = None
        self.pose = libmyo.Pose.rest
        self.emg_enabled = False
        self.locked = False
        self.rssi = None
        self.emg = None
        self.last_time = 0
        self.color_index = 0
        self.color_array = [[0.658, 0.3134],
                            [0.5753, 0.3942],
                            [0.4597, 0.4794],
                            [0.4084, 0.5168],
                            [0.1684, 0.0416],
                            [0.2577, 0.1109],
                            [0.3127, 0.3277]]
        self.brightness = 100   
        self.flag = 1     

    def output(self):
        ctime = time.time()
        if (ctime - self.last_time) < self.interval:
            return
        self.last_time = ctime
        parts = []
        #if self.orientation:
            #for comp in self.orientation:
                #parts.append(str(comp).ljust(15))
        parts.append(str(self.pose).ljust(20,'d'))
        print('\r' + ''.join('[{0}]'.format(self.pose)), end='')
        #parts.append('E' if self.emg_enabled else ' ')
        #parts.append('L' if self.locked else ' ')
        #parts.append(self.rssi or 'NORSSI')
        #print (self.pose)
        '''
        if self.emg:
            for comp in self.emg:
                parts.append(str(comp).ljust(5))
        '''
        #print('\r' + ''.join('[{0}]'.format(p) for p in parts), end='')
        sys.stdout.flush()

    def on_connect(self, myo, timestamp, firmware_version):
        myo.vibrate('short')
        myo.vibrate('short')
        myo.request_rssi()
        myo.request_battery_level()

    def on_rssi(self, myo, timestamp, rssi):
        self.rssi = rssi
        self.output()

    def on_pose(self, myo, timestamp, pose):
        if pose == libmyo.Pose.double_tap:
            myo.set_stream_emg(libmyo.StreamEmg.enabled)
            self.emg_enabled = True
        elif pose == libmyo.Pose.fingers_spread:
            myo.set_stream_emg(libmyo.StreamEmg.disabled)
            self.emg_enabled = False
            self.emg = None
        self.pose = pose

        if pose == 'wave_out':
            self.color_index += 1
        elif pose == 'wave_in':
            self.color_index -= 1
        self.color_index %= len(self.color_array)
        set_color(3,self.color_array[self.color_index])

        if pose == 'fist' and self.brightness > 45:        
            self.brightness -= 45            
        elif pose == 'fingers_spread' and self.brightness < 210:
            self.brightness += 45
        set_brightness(3,self.brightness,1)

        if pose == 'double_tap':
            if self.flag == 1:
                control_light(3,False)
                self.flag = 0
            else:
                control_light(3,True)
                self.flag = 1

        
        self.output()

    def on_orientation_data(self, myo, timestamp, orientation):
        self.orientation = orientation
        self.output()

    def on_accelerometor_data(self, myo, timestamp, acceleration):
        pass

    def on_gyroscope_data(self, myo, timestamp, gyroscope):
        pass

    def on_emg_data(self, myo, timestamp, emg):
        self.emg = emg
        self.output()

    def on_unlock(self, myo, timestamp):
        self.locked = False
        self.output()

    def on_lock(self, myo, timestamp):
        self.locked = True
        self.output()

    def on_event(self, kind, event):
        """
        Called before any of the event callbacks.
        """

    def on_event_finished(self, kind, event):
        """
        Called after the respective event callbacks have been
        invoked. This method is *always* triggered, even if one of
        the callbacks requested the stop of the Hub.
        """

    def on_pair(self, myo, timestamp, firmware_version):
        """
        Called when a Myo armband is paired.
        """

    def on_unpair(self, myo, timestamp):
        """
        Called when a Myo armband is unpaired.
        """

    def on_disconnect(self, myo, timestamp):
        """
        Called when a Myo is disconnected.
        """

    def on_arm_sync(self, myo, timestamp, arm, x_direction, rotation,
                    warmup_state):
        """
        Called when a Myo armband and an arm is synced.
        """

    def on_arm_unsync(self, myo, timestamp):
        """
        Called when a Myo armband and an arm is unsynced.
        """

    def on_battery_level_received(self, myo, timestamp, level):
        """
        Called when the requested battery level received.
        """

    def on_warmup_completed(self, myo, timestamp, warmup_result):
        """
        Called when the warmup completed.
        """

def set_brightness(id,bright,t):
    #-----Brightness : 0~255
    b.set_light(id,'bri',bright,transitiontime = t)

def set_color(id,color):
    b.set_light(id,'xy',color,transitiontime = 2)   

def blink(bright):
    flag = 0
    counter = 0
    while counter<=2:
        set_brightness(3,bright,1)
        time.sleep(0.03)
        if flag == 0:
            if bright-15 >0:
                bright -= 15
            else:
                flag=1
                counter += 1
        elif flag == 1:
            if bright+15 < 254:
                bright += 15
            else:
                flag=0
                counter += 1

def control_light(id,mode):
    b.set_light(id,'on',mode)

def main():
    print("Connecting to Myo ... Use CTRL^C to exit.")
    try:
        hub = libmyo.Hub()
    except MemoryError:
        print("Myo Hub could not be created. Make sure Myo Connect is running.")
        return

    hub.set_locking_policy(libmyo.LockingPolicy.none)
    hub.run(1000, Listener())

    # Listen to keyboard interrupts and stop the hub in that case.
    try:
        while hub.running:
            time.sleep(0.25)
    except KeyboardInterrupt:
        print("\nQuitting ...")
    finally:
        print("Shutting down hub...")
        hub.shutdown()

b = Bridge('10.0.0.34')
set_brightness(3,100,1)

if __name__ == '__main__':

    main()

'''
red [0.658, 0.3134]
orange [0.5753, 0.3942]
yellow [0.4597, 0.4794]
green [0.4084, 0.5168]
blue [0.1684, 0.0416]
purple [0.2577, 0.1109]
white [0.3127, 0.3277]
'''
