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

    def __init__(self, virtual:bool=False, spi:bool=True):
        self.virtual = virtual

        self.on_pause = lambda: None
        self.on_break = lambda: None
        self.on_focus = lambda: None
        self.on_start_recording = lambda: None
        self.on_stop_recording = lambda: None
        self.on_review = lambda: None
        self.on_sync = lambda: None
        self.on_before = lambda: None
        self.on_after = lambda: None

        if self.virtual:
            t = threading.Thread(target=self.key_detect)
            t.start()
        else:
            self.pause_btn = HoldableButton(4, pull_up=True)
            self.break_btn = HoldableButton(17, pull_up=True)
            self.focus_btn = HoldableButton(27, pull_up=True)
            self.record_btn = HoldableButton(22, pull_up=True)
            if spi:
                self.pot = MCP3008(0) # Channel 0
            else:
                class Pot:
                    '''A mock class that represents a potentiometer.'''
                self.pot = Pot()
                self.pot.value = 1.0

            self.pause_btn.short_callback = self._on_pause
            self.break_btn.short_callback = self._on_break
            self.focus_btn.short_callback = self._on_focus
            self.record_btn.when_pressed = self._on_start_recording
            self.record_btn.when_released = self._on_stop_recording
            self.pause_btn.long_callback = self._on_review
            self.focus_btn.long_callback = self._on_sync

    def _on_pause(self):
        '''Called when the pause button is pressed.'''
        logger.info('Detect pause button press')
        self.on_before()
        self.on_pause()
        self.on_after()

    def _on_break(self):
        '''Called when the break button is pressed.'''
        logger.info('Detect break button press')
        self.on_before()
        self.on_break()
        self.on_after()

    def _on_focus(self):
        '''Called when the focus button is pressed.'''
        logger.info('Detect focus button press')
        self.on_before()
        self.on_focus()
        self.on_after()

    def _on_start_recording(self):
        '''Called when the record button is pressed.'''
        logger.info('Detect record button press')
        self.on_before()
        self.on_start_recording()
        self.on_after()

    def _on_stop_recording(self):
        '''Called when the record button is released.'''
        logger.info('Detect record button release')
        self.on_before()
        self.on_stop_recording()
        self.on_after()

    def _on_review(self):
        '''Called when the pause button is held for a long time.'''
        logger.info('Detect pause button hold')
        self.on_before()
        self.on_review()
        self.on_after()

    def _on_sync(self):
        '''Called when the focus button is held for a long time.'''
        logger.info('Detect focus button hold')
        self.on_before()
        self.on_sync()
        self.on_after()

    @property
    def volume(self):
        """Get the volume"""
        if self.virtual:
            return 4.0
        else:
            return self.pot.value * 8.0

    def key_detect(self):
        """Detect a key to press"""
        while True:
            val = input()
            if val == "pause":
                self._on_pause()
            elif val == "break":
                self._on_break()
            elif val == 'focus':
                self._on_focus()
            elif val == "start_recording":
                self._on_start_recording()
            elif val == "stop_recording":
                self._on_stop_recording()
            elif val == "review":
                self._on_review()
            elif val == "sync":
                self._on_sync()
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
