"""Module defining the executer class and configuration."""


from dataclasses import dataclass

import pyautogui
from pynput.keyboard import Controller

from ..arkey import ARKey
from ..filehandler import FileHandler


@dataclass
class ExecuterConfig:
    """Dataclass defining the executer configurations."""

    MOVE_DURATION: float = 0.2
    CLICK_INTERVAL: float = 0.1
    WRITE_SPEED: float = 0.1


class Executer:
    """Execute a set of actions."""

    def __init__(self, filename, variables=None, verbose=0, config=None):
        """Initialize the executer."""
        self.filename = filename
        self.verbose = verbose

        self.current_position = None
        self.config = config or ExecuterConfig()

        self.actions = FileHandler.load(self.filename)
        self.translations = {v: k for k, v in self.actions.ACTION_TRANSLATION.items()}

        self.variables = variables
        self.verify_variables()

        self.size_conversion = [
            new_size / ref_size
            for new_size, ref_size in zip(pyautogui.size(), self.actions.screen_size)
        ]
        self._keyboard = Controller()

    def verify_variables(self):
        """Verify that all variables in actions are defined."""
        variable_count = [
            self.translations[action[0]] for action in self.actions.get_actions_list()
        ].count("variable")

        real_variable_count = 0 if self.variables is None else len(self.variables)

        if real_variable_count != variable_count:
            raise ValueError(
                "Specify the same amount of variables that are defined in the recorded action."
            )

    def start(self):
        """Start the execution."""
        for action in self.actions.get_actions_list():
            self.__getattribute__(self.translations[action[0]])(action[1])

    def move(self, pos):
        """Execute move action."""
        conv_pos = [
            pos * conversion for pos, conversion in zip(pos, self.size_conversion)
        ]
        self.current_position = conv_pos
        pyautogui.moveTo(conv_pos[0], conv_pos[1], duration=self.config.MOVE_DURATION)

    def click(self, clicks):
        """Execute click action."""
        pos = self.current_position or list(pyautogui.position())
        pyautogui.click(
            pos[0], pos[1], clicks=clicks, interval=self.config.CLICK_INTERVAL
        )

    def variable(self, index):
        """Execute insert variable action."""
        pyautogui.typewrite(self.variables[index], self.config.WRITE_SPEED)

    def type_input(self, inp):
        """Execute input typing action."""
        inp = [[ARKey(elem) for elem in inp_list] for inp_list in inp]

        for inp_list in inp:
            for elem in inp_list:
                self._keyboard.press(elem.key_for_action())

            for elem in inp_list:
                self._keyboard.release(elem.key_for_action())
