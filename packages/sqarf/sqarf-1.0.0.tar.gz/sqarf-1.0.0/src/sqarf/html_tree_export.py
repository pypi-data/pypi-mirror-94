# flake8: noqa
import time
import json


from .exporter import _BasicExporter
from .session import Session


HEAD_ICONS = """
<!-- icons from https://remixicon.com/ -->
<link href="https://cdn.jsdelivr.net/npm/remixicon@2.5.0/fonts/remixicon.css" rel="stylesheet">
"""

HEAD_CSS_TOOLBAR = """
  <style type="text/css">
  /* Tools CSS */

    /* Add a black background color to the top navigation */
    .top_tools, .top_tools a{
        background-color: #333;
        overflow: hidden;
        display: flex;
        align-items: center;
    }

    /* toggleable resize when hidden-toggle button resizes */
    .toggleable {
        padding: 5px;
    }

    /* Style the links inside the top bar */
    .top_tools a {
        float: left;
        color: #f2f2f2;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
        font-size: 17px;
    }

    /* Add a color to the active tools */
    .top_tools a.active {
        background-color: #4CAF50;
        color: white;
    }

    /* Change the color of links on hover */
    .top_tools a:hover {
        background-color: #ddd;
        color: black;
    }
  </style>
"""

HEAD_CSS_TOOLTIPS = """
  <style type="text/css">
  /* Tooltips CSS */
    .tooltip {
    position: relative;
    display: inline-block;
    }

    .tooltip .tooltiptext {
    visibility: hidden;
    //width: 120px;
    background-color: black;
    color: #fff;
    //text-align: center;
    border-radius: 6px;
    padding: 10px 10px 5px 5px;
    position: absolute;
    z-index: 1;
    top: -5px;
    left: 110%;
    }

    .tooltip .tooltiptext::after {
    content: "";
    position: absolute;
    top: 20px;
    right: 100%;
    margin-top: -5px;
    border-width: 5px;
    border-style: solid;
    border-color: transparent black transparent transparent;
    }
    .tooltip:hover .tooltiptext {
    visibility: visible;
    }
  </style>
"""

HEAD_CSS_TABLETREE = """
  <style type="text/css">
  /* TableTree CSS */

  table.tree {
  	border-collapse: collapse;
    width: 100%;
  }

  table.tree tr {
  }

  table.tree tr:hover {
      text-shadow: 2px 2px 2px #00000036;
  }

  table.tree td {
  }

  table.tree td:first-child {
  }
  </style>
"""

HEAD_CSS_LOOK = """
  <style type="text/css">
  /* Look CSS */

    body {
      font-family: Arial;
    }

    .hfill {
        width: 100%;
        background-color=red;
    }
    
    .status {
      padding: 5;
      margin: 0 -5px 0 0;
    }

    .ERROR {
        background-color: red;
        color: cyan;
    }
    .FAILED {
      background-color: fdd;
      color: maroon;
    }
    .PASSED {
      background-color: dfd;
      color: green;
    }
    .IRRELEVANT {
      background-color: #bbb;
      color: #eee;
    }
    .NA {
      background-color: grey;
      color: white;
    }
  </style>
"""

HEAD = (
    "<head>"
    "<title>SQARF Report</title>" + HEAD_ICONS + HEAD_CSS_TOOLBAR + HEAD_CSS_TOOLTIPS
    # + HEAD_CSS_TREE
    + HEAD_CSS_TABLETREE + HEAD_CSS_LOOK + "</head>"
)

BODY_TOOLBAR = """
<div class="top_tools">
    <!-- <a class="button remove-class" affected=".with_children" to_remove="open"><i class="ri-add-box-line"></i>All</a> -->
    <!-- <a class="button add-class" affected=".with_children" to_add="open"><i class="ri-checkbox-indeterminate-line"></i>All</a> -->

    <!-- <a class="button hidden-toggle active" to_toggle=".test-name"><i class="ri-checkbox-fill ri-1x"></i><span>Show Test Name</span></a> -->
    <!-- <a class="button hidden-toggle active" to_toggle=".test-summary"><i class="ri-checkbox-fill ri-1x"></i><span>Summaries</span></a> -->
    <a class="button hidden-toggle active" to_toggle=".info-description"><i class="ri-checkbox-fill ri-1x"></i> Descriptions</a>
    <a class="button hidden-toggle active" to_toggle=".info-time"><i class="ri-checkbox-fill ri-1x"></i>Show Run Times</a>
    <a class="button hidden-toggle active" to_toggle=".info-source"><i class="ri-checkbox-fill ri-1x"></i>Show Test Source</a>
<!--    <a class="button hidden-toggle active" to_toggle=".PASSED"><i class="ri-checkbox-fill ri-1x"></i>Hide Passed</a> -->
<!--   <a class="button hidden-toggle active" to_toggle=".IRRELEVANT"><i class="ri-checkbox-fill ri-1x"></i>Show Irrelevants</a> -->
    <!-- <a class="button hidden-toggle active" to_toggle=".info-traceback"><i class="ri-checkbox-fill ri-1x"></i>Traces</a> -->
</div>
"""

TOP = "<html>" + HEAD + "<body>" + BODY_TOOLBAR

JS_TOOLBAR = """ 
    /* button click */
    var buttons = document.querySelectorAll('.button, .button *');
    for (var i = 0; i < buttons.length; i++){
        buttons[i].addEventListener('click', function(e) {
            e.stopPropagation(); /* needed to avoid double trigger on image click */
            var b = e.srcElement.closest('a');

            // Visibility toggle button
            if(b.classList.contains('hidden-toggle')) {
                b.classList.toggle('active');
                b.querySelector('i').classList.toggle('ri-checkbox-blank-line');
                b.querySelector('i').classList.toggle('ri-checkbox-fill');
                var toggleable = document.querySelectorAll('.toggleable'+b.getAttribute('to_toggle'));
                for(var i=0; i < toggleable.length; i++){
                    toggleable[i].hidden = ! toggleable[i].hidden;
                }
            }

            // Class add button
            if(b.classList.contains('add-class')) {
                var affected = document.querySelectorAll(b.getAttribute('affected'));
                for(var i=0; i < affected.length; i++){
                    affected[i].classList.remove(b.getAttribute('to_add'));
                }
            }

            // Class remove button
            if(b.classList.contains('remove-class')) {
                var affected = document.querySelectorAll(b.getAttribute('affected'));
                for(var i=0; i < affected.length; i++){
                    affected[i].classList.add(b.getAttribute('to_remove'));
                }
            }
        });
    }

    /* click toggle buttons to set default state */
    var hbs = document.querySelectorAll('.hidden-toggle')
    for(var i = 0; i < hbs.length; i++){
        hbs[i].dispatchEvent(new Event('click'));
    }
"""

JS_TABLETREE = """

    /* Table Tree */
	var collect_sibblings = function (elem, skip_func, break_func) {
		var collected = [];
		elem = elem.nextElementSibling;
		while (elem) {
			console.log('?', elem, elem.getAttribute('data-depth'), skip_func(elem), break_func(elem));
			if (break_func(elem)) break;
			if (!skip_func(elem)){
                console.log('+', elem)
                collected.push(elem);
            };
			elem = elem.nextElementSibling;
		}
		return collected;
	};
    var findAllSubs = function (tr) {
        var depth = parseInt(tr.getAttribute('data-depth'));
        var break_if = function (el) {
            return el.getAttribute('data-depth') <= depth;
        }
        var skip_if = function (el) {
            return false;
        }
        return collect_sibblings(tr, skip_if, break_if);
    };
    var findDirectSubs = function (tr) {
        var depth = parseInt(tr.getAttribute('data-depth'));
        var break_if = function (el) {
            return el.getAttribute('data-depth') <= depth;
        }
        var skip_if = function (el) {
            return el.getAttribute('data-depth') > depth+1;
        }
        return collect_sibblings(tr, skip_if, break_if);
    };
    var collapse = function(tr) {
        var subs = findAllSubs(tr);
        tr.classList.add('collapsed');
        for(i=0; i<subs.length; i++){
            subs[i].hidden = true;
            if(!subs[i].classList.contains('collapsed')){
                collapse(subs[i]);
            }
        }
    };
    var expand = function(tr) {
        var subs = findDirectSubs(tr);
        tr.classList.remove('collapsed');
        console.log('expand', tr, subs);
        for(i=0; i<subs.length; i++){
            subs[i].hidden = false;
        }
    }

    // init first tds indent
    var first_tds = document.querySelectorAll('table.tree td.collapser');
    for(var i = 0; i < first_tds.length; i++){
        var indent = first_tds[i].parentElement.getAttribute('data-depth')*50;
        first_tds[i].setAttribute("style", "border-left: "+indent+"px solid #fff");
    };
    
    // set .toggle click
    var collapsers = document.querySelectorAll('table.tree .collapser');
    for(var i = 0; i < collapsers.length; i++){
        collapsers[i].addEventListener('click', function(e) {
            var tr = e.srcElement.closest('tr'); //Get <tr> parent of tr collapser 
            if(tr.classList.contains('collapsed')) {
                expand(tr);
            }else{
                collapse(tr);
            }
        });
    };

"""

BOTTOM = (
    '<script type="text/javascript">'
    + JS_TOOLBAR
    + JS_TABLETREE
    + "</script>"
    + "</body></html>"
)


def test_to_html_tree(test, root_timestamp, indent=0):
    """
    Returns the html table-tree for the given test json export.
    """
    S = indent * "  "
    lines = []
    test_name = test["test_name"]
    short = test["short_description"]
    long = test["long_description"]
    start_time = test["timestamp"] - root_timestamp
    run_time = test["result"]["timestamp"] - test["timestamp"]
    result = test["result"]
    status = result["status"]
    summary = result["summary"] or ""
    error = result["error"]
    trace = result["trace"]

    lines = []
    lines.append('{}<tr data-depth="{}" class="">'.format(S, indent))

    # Test name + tooltip status and summary
    lines.append('{}  <td class="collapser status {}">'.format(S, status))
    if test["sub_tests"]:
        lines.append(S + '<i class="ri-flask-fill"></i>')
    else:
        lines.append(S + '<i class="ri-test-tube-fill"></i>')
    lines.append(S + '    <span class="tooltip">{}'.format(test_name))
    lines.append(S + '      <span class="tooltiptext">')
    lines.append(S + '        <span class="status {}">{}</span>'.format(status, status))
    lines.append(S + "        <pre>{}</pre>".format(summary))
    if error:
        lines.append(S + "        <pre>{}</pre>".format(error))
        lines.append(S + "        <pre>{}</pre>".format(trace))

    lines.append(S + "        </span>")
    lines.append(S + "      </span>")
    lines.append(S + "    </td>")

    # Test short description + tooltip long description
    lines.append(S + '    <td class="{} toggleable info-description">'.format(status))
    lines.append(S + '      <span class="tooltip">{}'.format(short or ""))
    if long:
        lines.append(S + '      <span class="tooltiptext">')
        lines.append(S + "        <pre>{}</pre>".format(long))
        lines.append(S + "    </span>")
    lines.append(S + "    </td>")

    # Run times
    lines.append(
        S
        + '    <td class="{} toggleable info-time">start @+{:.02f}, {:.02f}s long.</td>'.format(
            status, start_time, run_time
        )
    )

    # Test type + tooltip source file
    lines.append(S + '    <td class="{} toggleable info-source">'.format(status))
    lines.append(S + '      <span class="tooltip">{}'.format(test["test_type"]))
    lines.append(S + '      <span class="tooltiptext">')
    lines.append(S + "        <pre>{}</pre>".format(test["test_filename"]))
    lines.append(S + "    </span>")
    lines.append(S + "    </td>")

    lines.append(S + "</tr>")

    # sub tests:
    for sub_test in test["sub_tests"]:
        lines.extend(test_to_html_tree(sub_test, root_timestamp, indent + 1))

    return lines


def html_tree(session_dict_list, config):
    lines = []
    for run in session_dict_list:
        title = "Results on {}".format(time.ctime(run["timestamp"]))
        lines.append('<h3 class="session-run">{}</h3>'.format(title))
        lines.append('<table class="tree">')
        lines.extend(test_to_html_tree(run, run["timestamp"]))
        lines.append("</table>")
    lines = "\n".join(lines)
    return TOP + lines + BOTTOM


@Session.register_exporter
class HtmlTreeExporter(_BasicExporter):

    EXPORTER_NAME = "Html Tree"

    def get_export_content(self, session_dict_list):
        return html_tree(session_dict_list, self.config)
