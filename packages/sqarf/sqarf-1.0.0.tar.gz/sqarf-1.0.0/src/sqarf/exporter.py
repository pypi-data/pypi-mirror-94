import os
import webbrowser
import json

from .session import Session


class Exporter(object):

    # str or None:
    EXPORTER_NAME = None

    # list of (str, bool)
    # must contain all supported key
    # for the `config` dict arg of the
    # constructor, associated with their
    # default (boolean) value:
    OPTION_DEFAULTS = ()

    @classmethod
    def exporter_name(cls):
        return cls.EXPORTER_NAME or cls.__name__

    @classmethod
    def get_defaults(cls):
        return cls.OPTION_DEFAULTS

    def __init__(self, config):
        super(Exporter, self).__init__()
        self.update_config(config)

    def update_config(self, config):
        pass

    def export(
        self,
        session_dict_list,
        filename,
        allow_overwrite,
        also_open_in_browser,
    ):
        if os.path.exists(filename) and not allow_overwrite:
            raise ValueError("Filename {} already exists !".format(filename))

        dirname = os.path.dirname(filename)
        if not os.path.isdir(dirname):
            try:
                os.makedirs(dirname)
            except Exception:
                raise ValueError("Error creating parent folder for {}".format(filename))

        content = self.get_export_content(session_dict_list)
        with open(filename, "w") as fp:
            fp.write(content)

        if also_open_in_browser:
            IN_SAME_TAB = 0
            webbrowser.open(filename, new=IN_SAME_TAB)

    def get_export_content(self, session_dict_list):
        raise NotImplementedError()


@Session.register_exporter
class JsonExporter(Exporter):
    """
    Exports to a json file.

    No Option: everything is always exported.
    """

    EXPORTER_NAME = "JSON"

    def get_export_content(self, session_dict_list):
        return json.dumps(session_dict_list)


class _BasicExporter(Exporter):

    EXPORTER_NAME = None
    OPTION_DEFAULTS = (
        ("Show Irrelevant Tests", True),
        ("Show Passed Tests", True),
        ("Show Logs", True),
        ("Hide Log if Passed", False),
        ("Show Debug Log", False),
        ("Show Context Edits", True),
        ("Show Context Data", False),
        ("Show Description", True),
        ("Show Times", True),
        ("Show Last Run Only", False),
    )

    def update_config(self, config):
        self.config = config.copy()
