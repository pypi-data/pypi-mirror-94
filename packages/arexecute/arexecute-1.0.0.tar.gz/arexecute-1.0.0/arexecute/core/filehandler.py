"""Module that defines file handling elements."""


import json
from pathlib import Path

from .actions import Actions
from .arkey import ARKey


class CustomJSONEncoder(json.JSONEncoder):
    """JSON Encoder that supports ARKey."""

    def default(self, obj):
        if isinstance(obj, ARKey):
            return obj.to_json()

        return json.JSONEncoder.default(self, obj)


class JSONHandler:
    """File handler that uses JSON."""

    EXTENSION = ".json"

    @staticmethod
    def save(recorder, filepath):
        """Save the recorder actions to a file."""
        actions_dict = {
            "actions": recorder.actions.get_actions_list(),
            "screen_size": recorder.actions.screen_size,
        }

        with open(filepath, "w") as f:
            json.dump(actions_dict, f, cls=CustomJSONEncoder)

    @staticmethod
    def load(filepath):
        """Load actions from a file."""
        with open(filepath, "r") as f:
            actions_dict = json.load(f)

        actions = Actions(
            actions_dict["screen_size"], actions=actions_dict["actions"]
        )
        return actions


class FileHandler:
    """General file handler.

    Handlers save and load actions into a certain type of file.
    """

    HANDLER = JSONHandler

    @staticmethod
    def _preprocess(filename):
        """Preprocess the filename and convert it to a Path."""
        if not str(filename).endswith(FileHandler.HANDLER.EXTENSION):
            filename = str(filename) + FileHandler.HANDLER.EXTENSION

        return Path(str(filename))

    @staticmethod
    def save(recorder):
        """Save the recorder actions."""
        filepath = FileHandler._preprocess(recorder.filename)
        FileHandler.HANDLER.save(recorder, filepath)

    @staticmethod
    def load(filename):
        """Load a file with actions."""
        filepath = FileHandler._preprocess(filename)
        return FileHandler.HANDLER.load(filepath)
