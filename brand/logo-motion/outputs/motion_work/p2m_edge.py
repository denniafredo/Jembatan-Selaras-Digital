"""Run a Pixel2Motion Playwright QA script against the installed Microsoft Edge.

    python p2m_edge.py <script.py> [script args...]

The skill's scripts call chromium.launch() with Playwright's bundled browser; this shim
defaults the launch to channel="msedge" so no browser download is needed.
"""
import runpy
import sys

from playwright.sync_api import BrowserType

_launch = BrowserType.launch


def _edge_launch(self, *args, **kwargs):
    kwargs.setdefault('channel', 'msedge')
    return _launch(self, *args, **kwargs)


BrowserType.launch = _edge_launch
script = sys.argv[1]
sys.argv = sys.argv[1:]
runpy.run_path(script, run_name='__main__')
