import time
import json

try:
    import html
except ImportError:
    import cgi

    html_escape = cgi.escape
else:
    html_escape = html.escape
from .log import Log


from .exporter import _BasicExporter
from .session import Session
from .qatest import QAResult

TOP = "<html><body>"

BOTTOM = "</body></html>"


def get_status_colors(status):
    return dict(
        ERROR=("red", "cyan"),
        FAILED=("#FDD", "maroon"),
        PASSED=("#DFD", "green"),
        FIXED=("#DDF", "green"),
        IRRELEVANT=("#BBB", "eee"),
        NA=("grey", "white"),
    )[status]


def get_status_style(status):
    style = "padding: 5; margin: 0 -5px 0 0;"
    bg, fg = get_status_colors(status)
    return "{} background-color: {}; color: {};".format(
        style,
        bg,
        fg,
    )


def get_indent_style(depth, status):
    indent = depth * 25
    bg, _ = get_status_colors(status)
    if 0:
        # this does not show correctly in QTextEdit :'(
        style = "border-left: {}px solid {};".format(indent, bg)
    else:
        style = "color: {}; ".format(bg)
    return style


def get_context_style(status):
    return "background-color: #ffb; color: #aa6;"


def get_doc_style(status):
    return "background-color: #eee; color: #aaa;"


def E(s):
    return html_escape(s or "")


def test_to_html_table(
    test,
    root_timestamp,
    indent,
    config,
):
    """
    Returns the html table-tree for the given test json export.
    """
    S = indent * "  "
    lines = []
    test_name = test["test_name"]
    short = E(test["short_description"] or "No description...")
    long = E(test["long_description"] or "")
    result = test["result"]
    status = result["status"]
    summary = E(result["summary"] or "")
    error = E(result["error"])
    trace = E(result["trace"])
    test_filename = E(test["test_filename"])
    status_style = get_status_style(status)

    if (
        not config.get("Show Irrelevant Tests", True)
        and status == QAResult.STATUS.IRRELEVANT
    ):
        return []
    if (
        not config.get("Show Passed Tests", True)
        and status in QAResult.passed_statuses()
    ):
        return []

    lines = []
    lines.append('{}<tr style="{}">'.format(S, status_style))

    if test["sub_tests"]:
        icon = "&#x1F52C;"  # microscope
        icon = "&#x2697;"  # alembic
        icon = "&#x1F9EB;"  # petri dish
    else:
        icon = "&#x1F9EA;"  # test tube
    indent_style = get_indent_style(indent, status)
    indent_text = indent * "__"
    source = "{}\n{}\n".format(test["test_type"], test_filename)
    lines.append(S + "  <td>")
    lines.append(
        '{}    <span style="{}">{}</span>'.format(S, indent_style, indent_text)
        + '<span title="{}\n{}\n{}">{} {}</span>'.format(
            source, short, long, icon, test_name
        )
    )
    lines.append(S + "  </td>")
    lines.append(S + "  <td>{}</td>".format(status))
    lines.append(S + "  <td>{}</td>".format(summary))
    lines.append(S + "</tr>")

    if error:
        short = test["short_description"] or "No description..."
        long = test["long_description"] or ""
        lines.append(S + "<tr>")
        lines.append(S + "<td></td>")
        lines.append(
            '{}<td colspan=2 style="{}">'.format(S, status_style)
            + "{}<br><pre>{}</pre>".format(error, trace)
            + "</td>"
        )
        lines.append(S + "</tr>")

    show_debug_log = config.get("Show Debug Log", False)
    show_log = True
    if config.get("Hide Log if Passed") and status in QAResult.passed_statuses():
        show_log = False
    if show_log:
        log_lines = test.get("log_lines", [])
        if log_lines:
            log = Log.pformat_lines(
                log_lines,
                include_debug=show_debug_log,
                indent_level=0,
                indent_string="  ",
            )
        else:
            log = "No log found :/"
        log = E(log)
        # style = get_context_style(status)
        lines.append(S + "<tr>")
        lines.append(S + "<td></td>")
        lines.append(
            '{}<td colspan=2 style="{}"><pre>{}</pre></td>'.format(S, status_style, log)
        )
        lines.append(S + "</tr>")

    if config.get("Show Times", False):
        style = get_context_style(status)
        start_time = test["timestamp"] - root_timestamp
        run_time = test["result"]["timestamp"] - test["timestamp"]
        time_txt = "started at +{:.02f}, ran for {:.02f}s.".format(
            start_time,
            run_time,
        )
        lines.append(S + "<tr>")
        lines.append(S + "<td></td>")
        lines.append(
            '{}<td style="{}  vertical-align:top; text-align:right;">'.format(
                S,
                style,
            )
            + "Run time:"
            + "</td>"
        )
        lines.append('{}<td style="{}">{}</td>'.format(S, style, time_txt))
        lines.append(S + "</tr>")

    if config.get("Show Context Edits", False):

        style = get_context_style(status)
        adds, overs, dels = test["context_edits"] or ({}, {}, [])
        nb = len(adds) + len(overs) + len(dels)
        if nb:
            adds = "\n".join(["+%s=%r" % (k, v) for k, v in adds.items()])
            overs = "\n".join(["*%s=%r" % (k, v) for k, v in overs.items()])
            dels = "\n".join(["-" + i for i in dels])
            title = "%i Context Edits:" % (nb,)
            context_edits = "\n%s\n%s\n%s" % (
                adds,
                overs,
                dels,
            )
            # else:
            #     title = "Context Edits:"
            #     context_edits = "/"
            context_edits = E(context_edits.strip())
            lines.append(S + "<tr>")
            lines.append(S + "<td></td>")
            lines.append(
                '{}<td style="{} vertical-align:top; text-align:right">'.format(
                    S,
                    style,
                )
                + title
                + "</td>"
            )
            lines.append(
                '{}<td style="{}"><pre>{}</pre></td>'.format(S, style, context_edits)
            )
            lines.append(S + "</tr>")

    if config.get("Show Context Data", False):
        style = get_context_style(status)
        context = test["context"]
        title = "Context Values:"
        if context:
            context = "\n".join(["    %s=%r" % (k, v) for k, v in context.items()])
            context = E(context.strip())
        else:
            context = "/!\\ Empty Context /!\\"
        lines.append(S + "<tr>")
        lines.append(S + "<td></td>")
        lines.append(
            S
            + '<td style="{} vertical-align:top; text-align:right;">'.format(style)
            + title
            + "</td>"
        )
        lines.append(
            '{}<td style="{}"><pre>{}</pre></td>'.format(
                S,
                style,
                context,
            )
        )
        lines.append(S + "</tr>")

    if config.get("Show Description", False):
        style = get_doc_style(status)
        lines.append(S + "<tr>")
        lines.append(S + "<td></td>")
        lines.append(
            '{}<td style="{} vertical-align:top; text-align:right">'.format(
                S,
                style,
            )
            + "Description:"
            "</td>"
        )
        lines.append(
            '{}<td style="{}"><pre>\n{}\n\n{}</pre></td>'.format(S, style, short, long)
        )
        lines.append(S + "</tr>")

    # sub tests:
    for sub_test in test["sub_tests"]:
        lines.extend(
            test_to_html_table(
                sub_test,
                root_timestamp,
                indent + 1,
                config,
            )
        )

    return lines


def html_table(session_dict_list, config):
    """
    Get html content showing the test results in a table
    as described by the config dict.

    A default config dict is returned by `get_default_config()`, use
    it as a starting point.
    """
    if config.get("Show Last Run Only"):
        session_dict_list = [session_dict_list[-1]]

    lines = []
    for run in session_dict_list:
        title = "Results on {}".format(time.ctime(run["timestamp"]))
        lines.append('<h3 class="session-run">{}</h3>'.format(title))
        # "boder-spacing" style is not supported by Qt
        # so we use "cellspacing
        lines.append('<table cellspacing="0">')
        lines.extend(
            test_to_html_table(
                run,
                run["timestamp"],
                0,
                config,
            )
        )
        lines.append("</table>")
    lines = "\n".join(lines)
    return TOP + lines + BOTTOM


@Session.register_exporter
class HtmlTableExporter(_BasicExporter):

    EXPORTER_NAME = "Html Table"

    def get_export_content(self, session_dict_list):
        return html_table(session_dict_list, self.config)
