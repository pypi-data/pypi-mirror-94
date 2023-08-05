"""Eventloop helpers"""
from typing import Optional, Any, Callable

from gi.repository import GLib as glib  # type: ignore

MAINLOOP_SINGLETON: Optional[glib.MainLoop] = None


def singleton() -> glib.MainLoop:
    """Return singleton instance of the current loop"""
    global MAINLOOP_SINGLETON  # pylint: disable=W0603
    if not MAINLOOP_SINGLETON:
        MAINLOOP_SINGLETON = glib.MainLoop()
        # Monkeypatch the call_soon helper on the mainloop object
        MAINLOOP_SINGLETON.call_soon = call_soon
    return MAINLOOP_SINGLETON


def call_soon(glib_callback: Callable[..., Any], *args: Any) -> int:
    """Add a high-priority callback to the eventloop"""
    return int(glib.timeout_add(0, glib_callback, *args, priority=glib.PRIORITY_HIGH))
