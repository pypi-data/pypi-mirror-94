'''
A Simple HTTP Server.

Servers:
    AsyncHTTPServer:     Async HTTP server
    ThreadedHTTPServer:  Threaded HTTP Server
Apps:
    App:         A Simple App class with @App.route(route, methods=['GET', 'POST'])
    Application: Same as App
    
There is a example at serverhttp.example. Run it from the command line or read the code.
'''

from .app import *
from .srv import *
from .http_support.responses import *

__version__ = 1.6.2
__all__ = (
	"App", "Application", "AsyncHTTPServer", "__version__", "Response", 
	"ThreadedHTTPServer")
