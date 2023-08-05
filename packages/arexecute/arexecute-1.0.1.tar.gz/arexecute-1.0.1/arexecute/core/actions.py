"""Module that defines Action class."""


class Actions:
    """Defines a set of actions and methods to operate them.

    Actions are defined as things that are allowed to be done, these can be
    recorded and then executed.
    The ACTION_TRANSLATION constant defines the translation from a name to
    an abbreviation.
    """

    ACTION_TRANSLATION = {
        "move": "M",
        "click": "C",
        "variable": "V",
        "type_input": "I",
        "wait": "W",
    }

    def __init__(self, screen_size, actions=None):
        """Initialize Action object."""
        self.actions = actions or []
        self.screen_size = screen_size
        self.variables_index = 0

    def _add_action(self, action):
        """Add an action to the set."""
        self.actions.append(action)

    def get_actions_list(self):
        """Return the action set."""
        return self.actions

    def move(self, x, y):
        """Add a move action to an unnormalized x, y position."""
        action = (Actions.ACTION_TRANSLATION["move"], (x, y))
        self._add_action(action)

    def click(self, clicks):
        """Add a click action with n clicks."""
        action = (Actions.ACTION_TRANSLATION["click"], clicks)
        self._add_action(action)

    def variable(self):
        """Add a variable placeholder action."""
        action = (Actions.ACTION_TRANSLATION["variable"], self.variables_index)
        self.variables_index += 1
        self._add_action(action)

    def type_input(self, inputs):
        """Add a typing action."""
        action = (Actions.ACTION_TRANSLATION["type_input"], inputs)
        self._add_action(action)

    def wait(self, time):
        """Add a wait action for n seconds."""
        action = (Actions.ACTION_TRANSLATION["wait"], time)
        self._add_action(action)
