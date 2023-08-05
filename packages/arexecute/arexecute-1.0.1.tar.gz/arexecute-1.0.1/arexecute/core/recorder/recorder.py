"""Module defining the recorder class and configurations."""


from dataclasses import dataclass

import pyautogui
from pynput.keyboard import Controller, Key, Listener

from ..actions import Actions
from ..arkey import ARKey
from ..filehandler import FileHandler
from .state import ActionRecordingState


@dataclass
class RecorderConfig:
    """Configure the recorder class."""

    MOVE_KEY: Key = Key.ctrl_l
    CLICK_KEY: Key = Key.shift_l
    INPUT_RECORD_KEY: Key = "i"
    WAIT_KEY: str = "w"
    VARIABLE_PLACE_KEY: str = "v"
    END_ACTION_KEY: Key = Key.caps_lock
    EXIT_KEY: Key = Key.alt_l


class Recorder:
    """Record a set of actions."""

    def __init__(self, filename, verbose=0, config=None):
        """Initialize the recorder object."""
        self.filename = filename
        self.verbose = verbose
        self.actions = Actions(pyautogui.size())
        self.listener = None

        self.config = config or RecorderConfig()

        self._keyboard = Controller()
        self.state = ActionRecordingState(self)

        self.caps = 0

    def set_state(self, state):
        """State machine pattern's set_state method."""
        self.state = state

    def print(self, message, verbosity=1):
        """Print a message according to verbosity."""
        if self.verbose == verbosity:
            print(message)

    def _on_press(self, key):
        """Define the on_press method of the pynput listener."""
        self.state.key_down(ARKey(key))

    def _on_release(self, key):
        """Define the on_release method of the pynput listener."""
        self.state.key_pressed(ARKey(key))

    def start(self):
        """Start recording."""
        with Listener(
            on_press=self._on_press, on_release=self._on_release
        ) as self.listener:
            self.listener.join()

    def exit(self):
        """Exit the recording, saving the actions."""
        FileHandler.save(self)
        if self.caps % 2 == 1:
            keyboard = Controller()
            keyboard.press(Key.caps_lock)
            keyboard.release(Key.caps_lock)

        self.listener.stop()
