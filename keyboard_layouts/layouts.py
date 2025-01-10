"""
Keyboard layout definitions for Shrthnder.
Each layout is defined as a dictionary mapping from QWERTY positions to the actual keys.
"""

class KeyboardLayouts:
    # Standard German QWERTZ Layout
    QWERTZ = {
        # Row 1
        'q': 'q', 'w': 'w', 'e': 'e', 'r': 'r', 't': 't', 'y': 'z', 'u': 'u', 
        'i': 'i', 'o': 'o', 'p': 'p', '[': 'ü', ']': 'ß',
        # Row 2
        'a': 'a', 's': 's', 'd': 'd', 'f': 'f', 'g': 'g', 'h': 'h', 'j': 'j',
        'k': 'k', 'l': 'l', ';': 'ö', "'": 'ä',
        # Row 3
        'z': 'y', 'x': 'x', 'c': 'c', 'v': 'v', 'b': 'b', 'n': 'n', 'm': 'm',
        ',': ',', '.': '.', '/': '-',
        'score': 525.23
    }

    # AdNW Layout
    ADNW = {
        # Row 1
        'q': 'k', 'w': 'u', 'e': 'ü', 'r': '.', 't': 'ä', 'y': 'v', 'u': 'g',
        'i': 'c', 'o': 'l', 'p': 'j', '[': 'f', ']': 'ß',
        # Row 2
        'a': 'h', 's': 'i', 'd': 'e', 'f': 'a', 'g': 'o', 'h': 'd', 'j': 't',
        'k': 'r', 'l': 'n', ';': 's', "'": 'x', '\\': 'y',
        # Row 3
        'z': 'ö', 'x': ',', 'c': 'q', 'v': 'b', 'b': 'p', 'n': 'w', 'm': 'm',
        ',': 'z', '.': '-',
        'score': 291.27
    }

    # CMOS Layout
    CMOS = {
        # Row 1
        'q': 'j', 'w': 'k', 'e': 'u', 'r': 'o', 't': 'ä', 'y': 'p', 'u': 'b',
        'i': 'l', 'o': 'm', 'p': 'ß', '[': 'x', ']': 'q',
        # Row 2
        'a': 'w', 's': 'h', 'd': 'i', 'f': 'e', 'g': 'a', 'h': 'd', 'j': 't',
        'k': 'n', 'l': 'r', ';': 's', "'": 'y', '\\': '.',
        # Row 3
        'z': 'ü', 'x': ',', 'c': 'ö', 'v': 'g', 'b': 'c', 'n': 'v', 'm': 'z',
        ',': 'f', '.': '-',
        'score': 250.73
    }

    # Hamlak Layout
    HAMLAK = {
        # Row 1
        'q': 'q', 'w': 'w', 'e': 'l', 'r': 'd', 't': 'b', 'y': 'j', 'u': 'f',
        'i': 'u', 'o': 'o', 'p': ';',
        # Row 2
        'a': 'a', 's': 's', 'd': 'r', 'f': 't', 'g': 'g', 'h': 'y', 'j': 'n',
        'k': 'e', 'l': 'i', ';': 'h',
        # Row 3
        'z': 'z', 'x': 'x', 'c': 'm', 'v': 'c', 'b': 'v', 'n': 'k', 'm': 'p',
        ',': ',', '.': '.', '/': '/'
    }

    # Programmer Dvorak Layout
    PROGRAMMER_DVORAK = {
        # Row 1
        'q': ';', 'w': ',', 'e': '.', 'r': 'p', 't': 'y', 'y': 'f', 'u': 'g',
        'i': 'c', 'o': 'r', 'p': 'l', '[': '/', ']': '=',
        # Row 2
        'a': 'a', 's': 'o', 'd': 'e', 'f': 'u', 'g': 'i', 'h': 'd', 'j': 'h',
        'k': 't', 'l': 'n', ';': 's', "'": '-',
        # Row 3
        'z': 'q', 'x': 'j', 'c': 'k', 'v': 'x', 'b': 'b', 'n': 'm', 'm': 'w',
        ',': 'v', '.': 'z'
    }

    # Colemak Mod-DH Layout
    COLEMAK_MOD_DH = {
        # Row 1
        'q': 'q', 'w': 'w', 'e': 'f', 'r': 'p', 't': 'b', 'y': 'j', 'u': 'l',
        'i': 'u', 'o': 'y', 'p': ';',
        # Row 2
        'a': 'a', 's': 'r', 'd': 's', 'f': 't', 'g': 'g', 'h': 'm', 'j': 'n',
        'k': 'e', 'l': 'i', ';': 'o',
        # Row 3
        'z': 'z', 'x': 'x', 'c': 'c', 'v': 'd', 'b': 'v', 'n': 'k', 'm': 'h',
        ',': 'q', '.': ',', '/': '.'
    }

    # Workman Layout
    WORKMAN = {
        # Row 1
        'q': 'q', 'w': 'd', 'e': 'r', 'r': 'w', 't': 'b', 'y': 'j', 'u': 'f',
        'i': 'u', 'o': 'p', 'p': ';',
        # Row 2
        'a': 'a', 's': 's', 'd': 'h', 'f': 't', 'g': 'g', 'h': 'y', 'j': 'n',
        'k': 'e', 'l': 'o', ';': 'i',
        # Row 3
        'z': 'z', 'x': 'x', 'c': 'm', 'v': 'c', 'b': 'v', 'n': 'k', 'm': 'l',
        ',': ',', '.': '.', '/': '/',
        'score': 367.36
    }

    @classmethod
    def get_layout(cls, name):
        """Get a keyboard layout by name."""
        layouts = {
            'qwertz': cls.QWERTZ,
            'adnw': cls.ADNW,
            'cmos': cls.CMOS,
            'hamlak': cls.HAMLAK,
            'programmer_dvorak': cls.PROGRAMMER_DVORAK,
            'colemak_mod_dh': cls.COLEMAK_MOD_DH,
            'workman': cls.WORKMAN
        }
        return layouts.get(name.lower()) 