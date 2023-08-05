"""




"""
from contextlib import contextmanager


class Message(object):
    class MESSAGE_TYPES:

        TITLE = "Title"
        INFO = "Info"
        DEBUG = "Debug"
        WARNING = "Warning"
        ERROR = "Error"

        @classmethod
        def to_prefix(cls, message_type):
            return {
                cls.TITLE: "### ",
                cls.INFO: "",
                cls.DEBUG: ">>> ",
                cls.WARNING: "[!] ",
                cls.ERROR: "[!!!] ",
            }.get(message_type, "?")

    @classmethod
    def pformat_lines(cls, lines, include_debug, indent_level, indent_string):
        to_prefix = cls.MESSAGE_TYPES.to_prefix
        DEBUG = cls.MESSAGE_TYPES.DEBUG
        return "\n".join(
            "{}{}{}".format(
                indent_string * indent_level, to_prefix(message_type), message
            )
            for (indent_level, message_type, message) in lines
            if include_debug or message_type != DEBUG
        )

    def __init__(self, message_type, message_content):
        super(Message, self).__init__()
        self.message_type = message_type
        self.message_content = message_content

    def to_lines(self, indent_level):
        return [
            (indent_level, self.message_type, self.message_content),
        ]


class Section(Message):
    def __init__(self, title):
        super(Section, self).__init__(Message.MESSAGE_TYPES.TITLE, title)
        self.messages = []  # Message / Section instances

    def _add_message(self, message_type, message_texts):
        self.messages.append(
            Message(message_type, " ".join([str(i) for i in message_texts]))
        )

    def info(self, *texts):
        self._add_message(Message.MESSAGE_TYPES.INFO, texts)

    def debug(self, *texts):
        self._add_message(Message.MESSAGE_TYPES.DEBUG, texts)

    def warning(self, *texts):
        self._add_message(Message.MESSAGE_TYPES.WARNING, texts)

    def error(self, *texts):
        self._add_message(Message.MESSAGE_TYPES.ERROR, texts)

    @contextmanager
    def section(self, *title_texts):
        section = Section(" ".join([str(i) for i in title_texts]))
        self.messages.append(section)
        yield section

    def to_lines(self, indent_level):
        ERROR = self.MESSAGE_TYPES.ERROR
        WARNING = self.MESSAGE_TYPES.WARNING
        lines = []
        errs = 0
        warns = 0
        for message in self.messages:
            sub_lines = message.to_lines(indent_level + 1)
            errs += len([line for line in sub_lines if line[1] == ERROR])
            warns += len([line for line in sub_lines if line[1] == WARNING])
            lines.extend(sub_lines)
        extras = []
        if errs:
            extras.append("{} Errors".format(errs))
        if warns:
            extras.append("{} Warnings".format(warns))
        extra_str = extras and " ({})".format(", ".join(extras)) or ""
        indent_level, message_type, message = super(Section, self).to_lines(
            indent_level
        )[0]
        return [
            (
                indent_level,
                message_type,
                message + extra_str,
            )
        ] + lines

    def pformat(self, include_debug, indent_level, indent_string):
        lines = self.to_lines(indent_level)
        return self.pformat_lines(
            lines,
            include_debug,
            indent_level,
            indent_string,
        )


class Log(Section):
    def __init__(self, title=None):
        if title is None:
            title = "Log"
        super(Log, self).__init__(title)

    def to_lines(self, indent_level=0):
        return super(Log, self).to_lines(indent_level)

    def pformat(self, include_debug=False, indent_level=0, indent_string="    "):
        return (
            super(Log, self).pformat(include_debug, indent_level, indent_string) + "\n"
        )
