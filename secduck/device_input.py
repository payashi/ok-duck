'''
This module contains the DeviceInput class.
'''
import logging
import threading
from gpiozero import Button, MCP3008

logger = logging.getLogger('DeviceInput')

class DeviceInput:
    '''
    A class that represents the input devices.

    Args:
        virtual: Whether the input devices are virtual.
    '''

    def __init__(self, virtual:bool=False):
        self.virtual = virtual

        self.on_pause = lambda: None
        self.on_break = lambda: None
        self.on_focus = lambda: None
        self.on_start_recording = lambda: None
        self.on_stop_recording = lambda: None
        self.on_review = lambda: None

        if self.virtual:
            t = threading.Thread(target=self.key_detect)
            t.start()
        else:
            self.pause_btn = HoldableButton(4, pull_up=True)
            self.break_btn = HoldableButton(17, pull_up=True)
            self.focus_btn = HoldableButton(27, pull_up=True)
            self.record_btn = HoldableButton(22, pull_up=True)
            self.pot = MCP3008(0) # Channel 0

            self.pause_btn.short_callback = self._on_pause
            self.break_btn.short_callback = self._on_break
            self.focus_btn.short_callback = self._on_focus
            self.record_btn.when_pressed = self._on_start_recording
            self.record_btn.when_released = self._on_stop_recording
            self.pause_btn.long_callback = self._on_review


    def _on_pause(self):
        '''Called when the pause button is pressed.'''
        logger.info('Detect pause button press')
        self.on_pause()

    def _on_break(self):
        '''Called when the break button is pressed.'''
        logger.info('Detect break button press')
        self.on_break()

    def _on_focus(self):
        '''Called when the focus button is pressed.'''
        logger.info('Detect focus button press')
        self.on_focus()

    def _on_start_recording(self):
        '''Called when the record button is pressed.'''
        logger.info('Detect record button press')
        self.on_start_recording()

    def _on_stop_recording(self):
        '''Called when the record button is released.'''
        logger.info('Detect record button release')
        self.on_stop_recording()

    def _on_review(self):
        '''Called when the pause button is held for a long time.'''
        logger.info('Detect pause button hold')
        self.on_review()


    @property
    def volume(self):
        """Get the volume"""
        if self.virtual:
            return 1.0
        else:
            return self.pot.value

    def key_detect(self):
        """Detect a key to press"""
        while True:
            val = input()
            if val == "on_pause":
                self._on_pause()
            elif val == "on_break":
                self._on_break()
            elif val == 'on_focus':
                self._on_focus()
            elif val == "start_recording":
                self._on_start_recording()
            elif val == "stop_recording":
                self._on_stop_recording()
            elif val == "on_review":
                self._on_review()
            elif val == "quit":
                break


class HoldableButton(Button):
    '''
    A button that can be held for a long time.

    Args:
        *args: Arguments to pass to the superclass constructor.
        short_callback: Callback to be called when the button is released after a short press.
        long_callback: Callback to be called when the button is released after a long press.
        **kwargs: Keyword arguments to pass to the superclass constructor.
    '''
    def __init__(self, *args, short_callback=None, long_callback=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.short_callback = short_callback
        self.long_callback = long_callback

        self.was_held = False
        self.when_held = self._held
        self.when_released = self._released

    def _held(self):
        self.was_held = True
        if self.long_callback is not None:
            self.long_callback()

    def _released(self):
        if self.was_held is False and self.short_callback is not None:
            self.short_callback()
        self.was_held = False
