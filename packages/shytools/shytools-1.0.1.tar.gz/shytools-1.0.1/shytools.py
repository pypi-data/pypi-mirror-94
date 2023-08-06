"""
Shy tools.
"""

import sys
import types



NAMESPACES = {}



def shymethod(method):
    """
    Shy methods decorator.
    """

    def shymethod(*pargs, **kwargs):
        shy = pargs[0]
        regular = NAMESPACES.get(id(shy), shy)
        return method(regular, *pargs[1:], **kwargs)

    return shymethod



class shyproperty(property):
    """
    Shy properties decorator.
    """

    def __init__(self, fget = None, fset = None, fdel = None, doc = None):

        if fget is not None:
            fget = shymethod(fget)

        if fset is not None:
            fset = shymethod(fset)

        if fdel is not None:
            fdel = shymethod(fdel)

        property.__init__(self, fget, fset, fdel, doc)



class shytype(object):
    """
    Shy abstract base class.
    """

    __slots__ = []



    def __init_subclass__(cls, *pargs, **kwargs):
        if not isinstance(cls.__slots__, tuple):
            raise TypeError(f'{cls.__name__}.__slots__ must be tuple')

        if cls.__slots__:
            raise ValueError(f'{cls.__name__}.__slots__ must be empty tuple')



    def __new__(cls, *pargs, **kwargs):
        if cls is shytype:
            raise TypeError("Can't instantiate abstract class shytype")

        shy = object.__new__(cls)
        NAMESPACES[id(shy)] = types.SimpleNamespace()

        return shy



    def __del__(self):
        try:
            del NAMESPACES[id(self)]
        except:
            pass



shytools = types.ModuleType('shytools', __doc__)

shytools.shymethod = shymethod
shytools.shyproperty = shyproperty
shytools.shytype = shytype

shytools.__file__ = __file__
shytools.__all__ = ('shymethod', 'shyproperty', 'shytype')
shytools.__version__ = '1.0.1'
shytools.__author__ = 'José Falero <jzfalero@gmail.com>'

sys.modules['shytools'] = shytools



