"""
simplecrits.lib.core.singleton
~~~~~~~~~~~~

This module implements multiple singletons

Currently that only means the ResourceSingleton which is specific to
simplecrits :D

"""


# Setup the module logger
import logging
logger = logging.getLogger(__name__)


class ResourceSingleton(type):
    """
    Singleton metaclass based upon resource of an item in the simplecrits
    library
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        logger.debug('CLASS: %s ARGS: %s KWARGS: %s', cls, args, kwargs)
        # We always want to keep the like resources singled out
        if (cls, args[-1]) not in cls._instances:
            cls._instances[(cls, args[-1])] = super(ResourceSingleton,
                                                    cls).__call__(*args,
                                                                  **kwargs)
        return cls._instances[(cls, args[-1])]
