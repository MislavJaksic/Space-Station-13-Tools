import os
import sys

# Adds "ss13_tools" to sys.path
# Now you can do import with "from ss13_tools.Sub-Package ..."
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ss13_tools"))
)
