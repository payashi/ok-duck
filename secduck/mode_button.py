from gpiozero import Button

class ModeButton(Button):
    def __init__(self, *args, short_callback=None, long_callback=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.short_callback = short_callback
        self.long_callback = long_callback

        self.was_held = False
        self.when_held = self._held
        self.when_released = self._released

    def _held(self):
        self.was_held = True
        if self.long_callback != None:
            self.long_callback()

    def _released(self):
        if self.was_held == False and self.short_callback != None:
            self.short_callback()
        self.was_held = False


class AsyncModeButton(ModeButton):

    async def _held(self):
        self.was_held = True
        if self.long_callback != None:
            await self.long_callback()

    async def _released(self):
        if self.was_held == False and self.short_callback != None:
            await self.short_callback()
        self.was_held = False
