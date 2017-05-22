import functools
import os.path as osp

from traitlets import (Int, Integer, Float, Unicode, Enum, Long,
                       List, Bool, CRegExp, Dict, TraitError, observe, validate)
from traitlets.config import boolean_flag as flag


__all__ = ['Int', 'Integer', 'Float', 'Unicode', 'Enum', 'Long', 'List',
           'Bool', 'CRegExp', 'Dict', 'flag', 'TraitError', 'observe',
           'validate', 'traits_expand_path', 'traits_expects_directory']


def traits_expand_path(func):
    """Perform environment variables and ~user substitution
    in specified argument

    decorator usable with ```traitlets.validate``` decorator
    """
    @functools.wraps(func)
    def _wrapper(instance, proposal):
        proposal['value'] = osp.expandvars(osp.expanduser(proposal['value']))
        return func(instance, proposal)
    return _wrapper


def traits_expects_directory(func):
    """Ensure specified argument is a path to an existing directory

    decorator usable with ```traitlets.validate``` decorator
    """
    @functools.wraps(func)
    def _wrapper(instance, proposal):
        path = proposal['value']
        real_path = osp.realpath(path)
        if not osp.exists(real_path):
            raise TraitError('Path does not exists: %s' % real_path)
        if not osp.isfile(real_path):
            raise TraitError('Path is not a directory: %s' % real_path)
        return func(instance, proposal)
    return _wrapper
