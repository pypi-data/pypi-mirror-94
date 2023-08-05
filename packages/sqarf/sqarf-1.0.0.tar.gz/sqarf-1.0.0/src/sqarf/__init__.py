from ._version import get_versions

from .qatest import QATest
from .session import Session

# this is to register default exporters
import sqarf.exporter
import sqarf.html_table_export
import sqarf.html_tree_export

__version__ = get_versions()["version"]
del get_versions
