# -- Path setup --------------------------------------------------------------

import re
from pathlib import Path


def find_version():
    path = Path(__file__).parent.parent.joinpath("setup.py")
    version_file = path.read_text()
    version_match = re.search(r'^ +version="([^"]+)",$', version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string")


# -- Project information -----------------------------------------------------


project = "Typed Settings"
author = "Stefan Scherfke"
copyright = "2020, Stefan Scherfke"
release = find_version()
version = ".".join(release.split(".")[0:2])


# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

html_theme = "furo"
# html_theme_options = {
#     "logo_only": True,
#     "sidebar_hide_name": True,
# }

html_static_path = ["_static"]
html_logo = "_static/typed-settings-spacing.svg"
html_title = "Typed Settings"


# -- Extension configuration -------------------------------------------------

# Autodoc
autodoc_member_order = "bysource"

# Intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "attrs": ("https://www.attrs.org/en/stable/", None),
    "click": ("https://click.palletsprojects.com/en/master/", None),
}
