"""Service baseclasses"""
import asyncio
import logging
from dataclasses import dataclass, field

from gi.repository import GLib as glib  # type: ignore
from datastreamservicelib.service import BaseService as DSLBaseService
from datastreamservicelib.service import SimpleServiceMixin

from .eventloop import singleton as eventloop_singleton

LOGGER = logging.getLogger(__name__)

# See https://github.com/python/mypy/issues/5374 why the typing ignore
@dataclass  # type: ignore
class BaseService(DSLBaseService):
    """Baseclass for services using GLib mainloop in addition to asyncio"""

    _gloop: glib.MainLoop = field(init=False, default_factory=eventloop_singleton, repr=False)

    async def run(self) -> int:
        """Main entrypoint, should be called with asyncio.get_event_loop().run_until_complete()"""
        await self.setup()
        # Run the GLib mainloop in the default (threaded) executor
        gfuture = asyncio.get_event_loop().run_in_executor(None, self._gloop.run)
        await self._quitevent.wait()
        if self._exitcode is None:
            LOGGER.error("Got quitevent but exitcode is not set")
            self._exitcode = 1
        # Tell the GLib mainloop to quit
        glib.idle_add(self._gloop.quit)
        # Try to make sure teardown does not hang
        BaseService.set_exit_alarm()
        await self.teardown()
        await gfuture
        return self._exitcode


@dataclass
class SimpleService(SimpleServiceMixin, BaseService):
    """Simple service does a bit of automagics in setup"""

    async def setup(self) -> None:
        """Called once by run, just calls reload which loads our config"""
        self.hook_signals()
        self.reload()
