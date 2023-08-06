'''
Async And Threaded HTTP Servers.
'''
from .threaded import *
import sys
if float(sys.version[:3])<3.6:
    import warnings
    warnings.warn('Python version not supported', DeprecationWarning)
else:
    from .asyncsrv import *
