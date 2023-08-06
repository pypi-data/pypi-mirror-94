# Recursive dictionary merge
# Copyright (C) 2016 Paul Durivage <pauldurivage+github@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
try:
    from collections.abc import Mapping
except ImportError:  # python <3.7
    from collections import Mapping
import copy


def dict_merge(dct, merge_dct):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.

    Inputs:
        dct (dict): dict into which the merge is executed
        merge_dct (dict): dict merged into dct
    Returns: None (only `dct` is updated in place)

    >>> old = dict(zip('abc', '123'))
    >>> new = dict(zip('cd', '34'))
    >>> dict_merge(old, new)
    >>> old == dict(zip('abcd', '1234'))
    True
    """
    for k, v in merge_dct.items():
        if (k in dct and
                # TODO: test with dest `dict` replaced with `Mapping`
                isinstance(dct[k], dict) and
                isinstance(merge_dct[k], Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]


def dict_diff(a, b):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.

    Inputs:
        a (dict): original dictionary
        b (dict): changed dictionary
    Returns:
        delta_a_to_b (dict): deepcopy of b with any unchanged k, v pairs deleted

    >>> old = {'a': '1', 'b': '2', 'c': '3'}
    >>> new = {                    'c': '3', 'd': 4}
    >>> dict_diff(old, new)
    {'d': 4, 'a': None, 'b': None}
    """
    abdiff = copy.deepcopy(b)
    keys_to_del = []
    for k, v in abdiff.items():
        if k in a:
            if isinstance(b[k], dict) and isinstance(a[k], Mapping):
                # TODO: test with dest `dict` replaced with `Mapping`
                abdiff[k] = dict_diff(a[k], b[k])
            elif abdiff[k] == a[k]:
                keys_to_del.append(k)
    for k, v in a.items():
        if k not in abdiff:
            abdiff[k] = None
    for k in keys_to_del:
        del abdiff[k]
    return abdiff
