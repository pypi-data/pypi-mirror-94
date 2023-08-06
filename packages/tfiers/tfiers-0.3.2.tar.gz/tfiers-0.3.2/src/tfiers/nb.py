"""
IPython notebook initialisation.
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# Give user feedback during slow imports.

from preload import preload

preload(["numpy", "matplotlib.pyplot", "pandas", "seaborn"])
# ────────────────────────────────────────────────────────────────────────────────────╯


#


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

print("Imported `np`, `mpl`, `plt`, `sns`, `pd`")
# ────────────────────────────────────────────────────────────────────────────────────╯


#


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
try:
    import IPython

    ipython = IPython.get_ipython()
    #   Will be `None` if running as a script (i.e. not in a notebook or IPython REPL).

except ImportError:
    
    ipython = False

if ipython:

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    # The following allows you to edit the source code of packages installed with `pip
    # install -e` (or `--editable)`, while running a notebook, and then use this updated
    # code in the notebook, without having to restart the kernel on every code change.
    # This works well but not perfectly, so kernel restarts may still be required.
    ipython.run_line_magic("reload_ext", "autoreload")
    ipython.run_line_magic("autoreload", "2")
    # Exclude ourself from autoreloading, to avoid an exponential recursive import
    # monster.
    ipython.run_line_magic("aimport", "-tfiers.nb")
    # ────────────────────────────────────────────────────────────────────────────────╯

    #

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    # If the last expression of a code cell is eg `product = 3 * 7`, and the cell is
    # run, IPython prints nothing, by default. Here, we make it print the result
    # (`21`). This avoids having to type an extra line with just `product` to see
    # the result. (Prints can still be suppressed by ending the line with `;`).

    from IPython.core.interactiveshell import InteractiveShell

    InteractiveShell.ast_node_interactivity = "last_expr_or_assign"
    # ────────────────────────────────────────────────────────────────────────────────╯

    #

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    # Double resolution plots (without taking up twice as much screen space).

    from IPython.display import set_matplotlib_formats

    set_matplotlib_formats("retina")
    # ────────────────────────────────────────────────────────────────────────────────╯

# ────────────────────────────────────────────────────────────────────────────────────╯


#


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# Print precision for (floating point) numbers.


def set_print_precision(digits=4):
    # The ".4G" format allows eg `array([1000, 1E+05, 0.111])`
    number_format = f".{digits}G"
    # Print precision for plain Python numbers..
    if ipython:
        ipython.run_line_magic("precision", "%" + number_format)
    # ..and for NumPy.
    np.set_printoptions(
        formatter={
            "float_kind": lambda x: format(x, number_format),
        }
    )


set_print_precision()
# ────────────────────────────────────────────────────────────────────────────────────╯


#


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# Misc imports

# Useful higher-order function from the Python standard library. Given a function,
# returns a copy of that function, but with some arguments already applied.
from functools import partial

# On import, augments Pandas dataframes with better wrangling API.
# import janitor

# Our own styling
from . import plot_style

plot_style.reset_and_apply()

# kwargs for creating new figures with a desired aspect ratio & width.
from .plot_util import figsize

# ────────────────────────────────────────────────────────────────────────────────────╯


#

# Reassignment trick to stop PyCharm from complaining about unused imports:
mpl, plt, sns, pd = mpl, plt, sns, pd
partial = partial
figsize = figsize
