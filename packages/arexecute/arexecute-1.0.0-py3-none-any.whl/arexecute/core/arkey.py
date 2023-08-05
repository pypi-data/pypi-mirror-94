"""Module that defines a wrapper for keys defined in pynput."""


from pynput.keyboard import Key, KeyCode


class ARKey:
    """Wrapper for pynput Key class.

    This class provides an implementation to translate some key combinations
    that are not well defined in pynput, like ctrl and another key at the
    same time.
    """

    def __init__(self, key):
        """Initialize ARKey class."""
        self.isctrl = False
        self.ischar = False

        if isinstance(key, (Key, KeyCode)):
            self.isctrl = (key == Key.ctrl_l) or (key == Key.ctrl_r)
            self.key = key

        elif isinstance(key, int):
            try:
                self.key = Key(KeyCode.from_vk(key))

            except ValueError:
                self.key = KeyCode.from_vk(key)

        elif isinstance(key, str):
            self.key = KeyCode.from_char(key)

    def __eq__(self, other):
        """Overload equality operator."""
        return self.key == other.key

    def key_for_action(self):
        """Return the pynput key."""
        return self.key

    def processed(self):
        """Preprocess a key to compare in a normalized way.

        The preprocessing only includes lowercase transformation.
        """
        if isinstance(self.key, KeyCode):
            return self.key.char.lower()

        else:
            return self.key

    def to_json(self):
        """Transform a key object to a value for JSON formatting."""
        if isinstance(self.key, Key):
            value = self.key.value.vk

        elif isinstance(self.key, KeyCode):
            value = self.key.char

        else:
            value = self.key

        return value
