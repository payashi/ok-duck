'''
A class that controls the output of the device.
'''
import logging
from gpiozero import LED

logger = logging.getLogger('DeviceOutput')

class DeviceOutput:
    '''
    A class that controls the output of the device.
    '''
    def __init__(self, virtual: bool=False):
        if virtual:
            led = VirtualLED
        else:
            led = LED

        self.pause_led = led(14)
        self.break_led = led(15)
        self.focus_led = led(18)
        self.record_led = led(23)
        self.power_led = led(24)

        self.power_led.on()

    def on_pause(self):
        '''Turn on the pause led.'''
        logger.info('Turn on pause led')
        self.pause_led.on()
        self.break_led.off()
        self.focus_led.off()

    def on_break(self):
        '''Turn on the break led.'''
        logger.info('Turn on break led')
        self.pause_led.off()
        self.break_led.on()
        self.focus_led.off()

    def on_focus(self):
        '''Turn on the focus led.'''
        logger.info('Turn on focus led')
        self.pause_led.off()
        self.break_led.off()
        self.focus_led.on()

    def on_review(self):
        '''Turn on the pause led.'''
        self.on_pause()

    def on_start_recording(self):
        '''Turn on the record led.'''
        logger.info('Turn on record led')
        self.record_led.on()

    def on_stop_recording(self):
        '''Turn off the record led.'''
        logger.info('Turn off record led')
        self.record_led.off()

class VirtualLED:
    '''
    A virtual button that can be used for testing.
    '''
    def __init__(self, pin=None):
        self.is_lit = False
        self.pin = pin

    def on(self):
        '''Turn the led on.'''
        self.is_lit = True

    def off(self):
        '''Turn the led off.'''
        self.is_lit = False
