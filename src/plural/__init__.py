# Return a dictionary with the needed variation of a word.
# Copyright (C) 2011 Dario Giovannetti <dev@dariogiovannetti.net>
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Return a dictionary with the needed variation of a word.

@author: Dario Giovannetti
@copyright: Copyright (C) 2011 Dario Giovannetti <dev@dariogiovannetti.net>
@license: GPLv3
@version: 1.0
@date: 2011-12-03
"""

# Shortcuts (predefined null/singular/plural tuples)
# Capitalized versions are created automatically
regpl = {
    's': ('s', '', 's'),
    'es': ('es', '', 'es'),
    'y': ('ies', 'y', 'ies'),
    'ies': ('ies', 'y', 'ies'),
    'this': ('these', 'this', 'these'),
    'these': ('these', 'this', 'these'),
    'that': ('those', 'that', 'those'),
    'those': ('those', 'that', 'those'),
    'is': ('are', 'is', 'are'),
    'are': ('are', 'is', 'are'),
}


def set(*args, **kwargs):
    """
    Return a dictionary with the needed form of a word (usually singular or
    plural).
    
    This function is best used as an unpacked dictionary inside str.format(),
    though also making references to the keys in the dictionary is possible
    (the latter method will be treated in the last part of this guide).
    
    Preview example:
    >>> print('Word{P0s}'.format(**plural.set((2,))))
    Words
    
    Usage (part1):
    plural.set(*args [, sep='|'])
    Where each element of *args is a tuple in which the first element is the
    test value (any type), and the following elements are the strings to be
    processed (optional, read about Shortcuts):
    (test [, string , string, ...])
    Finally, sep (optional) is the string used to recognize the different forms
    in a string: default separator is '|'.
    
    Valid examples of an element of *args:
    (2,)
    (0, 'leaf|leaves')
    ('testvalue', 'man|men', 'null|single|multi')
    
    Return:
    This function returns a dictionary in the form:
    {
        'PN|originalstring': 'returnstring',
        'PN|originalstring': 'returnstring',
        ...
    }
    Where N is the index of the tuple in *args
    
    Usage (part 2):
    'string' (string in a tuple of *args)
    '{PN|string}' (str.format variable)
    This string will return the same value ('string') for every test value, so
    this is pretty useless and supported only for completeness' sake.
    'sing|plur' (string in a tuple of *args)
    '{PN|sing|plur} (str.format variable)
    This string will return 'sing' if test value equals 1 (integer), otherwise
    it will return 'plur'.
    'null|single|multi' (string in a tuple of *args)
    '{PN|null|single|multi} (str.format variable)
    This string will return 'null' if test value equals 0 (integer), it will
    return 'single' if test value equals 1 (integer), otherwise it will return
    'multi'.
    
    Examples:
    >>> print('{P0|Fish}'.format(**plural.set((4, 'Fish'))))
    Fish
    
    >>> print('{P0|Leaf|Leaves}'.format(**plural.set(('none', 'Leaf|Leaves'))))
    Leaves
    
    >>> print('{P0|null|single|multi}'.format(**plural.set((0,
                                                    'null|single|multi'))))
    null
    
    Usage (part 3: Shortcuts):
    It's not always necessary to use strings. Most of the time, for regular
    plurals formation you will just want to use shortcuts: for every tuple in
    *args (thus for every test value), this function will automatically
    generate some predefined names to be used in str.format, like this:
    '{PNs}' (equivalent to '{PN||s}')
    This shortcut will write 's' only if test value is different from 1
    (integer), otherwise it will write nothing.
    '{PNS}' (equivalent to '{PN||S}')
    Same as for '{PNs}', but capitalized.
    Each shortcut can have multiple versions with different capitalizations.
    The list of all available shortcuts can be retrieved with
    plural.shortcuts().
    Note that shortcuts do NOT use a separator.
    
    Examples:
    >>> print('Word{P0s}'.format(**plural.set((2,))))
    Words
    
    >>> print('DAY{P0S}, cherr{P1ies}'.format(**plural.set((7,), (1,))))
    DAYS, cherry
    
    >>> print('{P0|This|These} {P0is} {P0|a |}word{P0s}.'.format(
                                            **plural.set((
                                                3,
                                                'This|These',
                                                'a |'
                                            ))))
    These are words.
    
    Usage (part 4: Separator):
    The default separator is '|', but you can specify another string using the
    sep key after all *args' tuples:
    sep='customSeparator'
    Remember that the first 2 occurrences (3 in str.format variables) of
    separator will be used for separating the elements in strings: the
    following occurrences will be considered part of the 3rd (plural) word.
    
    Example:
    >>> print('{P0<x>Leaf<x>Leaves}, {P1<x>aaa<x>bbb<x>ccc<x>ddd}'.format(
                                            **plural.set(
                                                (1, 'Leaf<x>Leaves'),
                                                (10, 'aaa<x>bbb<x>ccc<x>ddd'),
                                                sep='<x>',
                                            )))
    Leaf, ccc<x>ddd
    
    Usage (part 5: special characters in str.format):
    When using plural.set as an unpacked dictionary, you are _not_ limited to
    Python's variable characters (letters, numbers and _): you can use almost
    whatever character you want, with some exceptions:
    '!', '[', '{', '}', '.', ':'
    This list could not be exhaustive; if you want to be able to use '[' or '.'
    you could use the method descripted in the following section; if you want
    to use these characters you could consider processing the dictionary
    outside str.format.
    Always remember that the first 2 occurrences (3 in str.format variables) of
    separator will be used for separating the elements in strings.
    
    Example:
    >>> print('{P0|/+-|#&_|];%|$}'.format(**plural.set(
                                            (3, '/+-|#&_|];%|$')
                                        )))
    ];%|$
    
    Usage (part 6: mixing plural.set with other str.format variables):
    Of course you can mix plural.set variables with normal str.format
    variables; just remember to unpack plural.set at the end of format
    arguments.
    
    Example:
    >>> birds=2
    >>> stones=1
    >>> print('Kill {0} bird{P0s} with {stn} stone{P1s}.'.format(
                                            str(birds),
                                            stn=str(stones),
                                            **plural.set(
                                                (birds,),
                                                (stones,),
                                            )
                                        ))
    Kill 2 birds with 1 stone.
    
    Usage (part 7: not unpacking the dictionary):
    There is an alternative useful way of using this function in str.format:
    just make references to the dictionary keys instead of bare arguments.
    This way the list of incompatible characters is slightly different than
    with the former method:
    '!', ']', '{', '}', ':'
    This list could not be exhaustive; note that with respect to the former
    method, '[' and '.' are compatible, while ']' is now incompatible; if you
    want to use these characters you could consider processing the dictionary
    outside str.format.
    Still remember that the first 2 occurrences (3 in str.format variables) of
    separator will be used for separating the elements in strings.
    
    Example:
    >>> birds=2
    >>> stones=1
    >>> print('Kill {0} bird{P[P0s]} with {stn} stone{P[P1s]}.'.format(
                                            str(birds),
                                            stn=str(stones),
                                            P=plural.set(
                                                (birds,),
                                                (stones,),
                                            )
                                        ))
    Kill 2 birds with 1 stone.
    """
    # Necessary for Python 2 compatibility
    # The Python 3 definition was:
    #def set(*args, sep='|'):
    if 'sep' in kwargs:
        sep = kwargs['sep']
    else:
        sep = '|'
    
    result = {}
    
    for n, v in enumerate(args):
        n = str(n)
        
        # Tell which one of null/singular/plural is needed
        form = v[0]
        if form not in (0, 1):
            form = 2
        
        # Create the predefined shortcuts for this variable (also their
        # respective capitalized versions)
        for r in regpl:
            result['P' + n + r] = regpl[r][form]
            result['P' + n + r.upper()] = regpl[r][form].upper()
        
        for p in v[1:]:
            # Create the key with the needed form for this word
            s = p.split(sep, 2)
            if len(s) == 2:
                s.append(s[1])
                s[1] = s[0]
                s[0] = s[2]
            if len(s) == 1:
                s.append(s[0])
                s.append(s[0])
            result['P' + n + sep + p] = s[form]
    
    return(result)


def shortcuts():
    """
    Return the list of available shortcuts
    """
    tpl = '[{}: {}, {}, {}]'
    print('Available shortcuts: [shortcut: null, singular, plural]')
    for r in regpl:
        print(tpl.format(r, regpl[r][0], regpl[r][1], regpl[r][2]))
        print(tpl.format(r.upper(), regpl[r][0].upper(), regpl[r][1].upper(),
                         regpl[r][2].upper()))
