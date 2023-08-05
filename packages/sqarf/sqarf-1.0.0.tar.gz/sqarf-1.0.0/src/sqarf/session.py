"""




"""
import os
import json

from .context import QAContext
from .qatest import QATest


class _SessionRootTest(QATest):

    SESSION = None

    @classmethod
    def test_name(cls):
        title = cls.SESSION._title
        return title or super(_SessionRootTest, cls).test_name()

    @classmethod
    def get_sub_test_types(cls):
        return cls.SESSION._test_types

    def can_fix(self, context):
        return False, "Can't fix the whole world :/"


class Session(object):
    class ObjectReprJSONEncoder(json.JSONEncoder):
        def default(self, obj):
            try:
                return json.JSONEncoder.default(self, obj)
            except TypeError:
                return repr(obj)

    # Exporter management
    _EXPORTERS = {}

    @classmethod
    def register_exporter(cls, ExporterType):
        """
        Registers an Exporter class. The `ExporterType`
        must be a subclass of `sqarf.exporter.Exporter`.

        Can be used as a class decorator.
        """
        cls._EXPORTERS[ExporterType.exporter_name()] = ExporterType
        return ExporterType

    @classmethod
    def get_exporter_names(cls):
        return sorted(cls._EXPORTERS.keys())

    @classmethod
    def get_exporter_defaults(cls, exporter_name):
        ExporterType = cls._EXPORTERS.get(exporter_name)
        if ExporterType is None:
            return []
        return ExporterType.get_defaults()

    @classmethod
    def get_exporter(cls, exporter_name, config):
        ExporterType = cls._EXPORTERS.get(exporter_name)
        if ExporterType is None:
            raise ValueError(
                'Unknown exporter type "{}" '
                '(know names are: "{}"'.format(
                    exporter_name,
                    cls.get_exporter_names(),
                )
            )
        return ExporterType(config)

    def __init__(self):
        super(Session, self).__init__()

        # This is sooooooooooo hacky !!! ^o^
        # I'll burn in hell for this :p
        class Root(_SessionRootTest):
            SESSION = self

        self._title = None

        self._test_types = []
        self._root_test_type = Root

        self._stop_on_fail = None
        self._allow_auto_fix = None
        self._context = QAContext(None)

        self._runs = []

    def set_title(self, title):
        """
        The title will be used as the Root test name
        (This only affects reports).

        Use None to revert to default.
        """
        self._title = title

    def register_test_types(self, test_types):
        self._test_types.extend(test_types)

    def register_tests_from_file(self, filename):
        """
        WARNING: only use this on trusted files !

        The python code in `filename` file must declare a `get_root_tests()`
        function returning a list of test types to register.

        The code can also use the gloable name `SESSION` which contains
        the session being configured.
        """
        if not os.path.isfile(filename):
            raise ValueError("{} is not a file !".format(filename))

        with open(filename, "rb") as fp:
            content = fp.read()

        self.register_tests_from_string(content, filename)

    def register_tests_from_string(self, code_string, virtual_filename):
        """
        WARNING: only use this with trusted data ! The `code_string` has
        the ability to wipe your server clean or tell anything to your
        mother in law !

        The python code in `code_string` string must declare a `get_root_tests()`
        function returning a list of test types to register.

        The code can also use the gloable name `SESSION` which contains
        the session being configured.

        The `virtual_filename` string will be used as the "source filename" in
        reports and some exceptions.
        """
        compiled = compile(code_string, virtual_filename, "exec")
        namespace = {"SESSION": self, "__filename__": virtual_filename}
        exec(compiled, namespace, namespace)
        getter_name = "get_root_tests"
        getter = namespace.get(getter_name)
        if getter is None:
            raise Exception(
                'Could not find a "{}()" function in {}. '
                "No test registered.".format(getter_name, virtual_filename)
            )

        try:
            test_types = getter()
        except Exception as err:
            import traceback

            traceback.print_exc()
            raise Exception(
                'Error executing "{}()" from {}: {}'.format(
                    getter_name, virtual_filename, err
                )
            )

        for TestType in test_types:
            TestType._forced_filename = virtual_filename
        self._test_types.extend(test_types)

    def context_set(self, **values):
        self._context.update(**values)

    def set_stop_on_fail(self, stop_on_fail):
        """
        `stop_on_fail` can be True, False, or None for default behavior
        """
        self._context.set_stop_on_fail(stop_on_fail)

    def set_allow_auto_fix(self, allow_auto_fix):
        """
        `allow_auto_fix` can be True, False, or None for default behavior
        """
        self._context.set_allow_auto_fix(allow_auto_fix)

    def run(self):
        root_test = self._root_test_type()
        self._runs.append(root_test)

        # use a copy of the context, tests will modify it:
        context = QAContext(self._context)

        # run all the tests:
        result = root_test.run(context)
        return result

    def to_lines(self):
        lines = []
        for run in self._runs:
            lines.extend(run.to_lines())
        return lines

    def to_dict_list(self):
        ret = []
        for run in self._runs:
            ret.append(run.to_dict())
        return ret

    def to_json(self):
        as_dict_list = self.to_dict_list()
        return json.dumps(as_dict_list, cls=self.ObjectReprJSONEncoder)
