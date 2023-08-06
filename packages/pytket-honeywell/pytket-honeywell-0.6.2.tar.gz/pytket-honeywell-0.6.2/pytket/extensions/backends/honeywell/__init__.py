# Copyright 2020-2021 Cambridge Quantum Computing
#
# You may not use this file except in compliance with the Licence.
# You may obtain a copy of the Licence in the LICENCE file accompanying
# these documents or at:
#
#     https://cqcl.github.io/pytket/build/html/licence.html

"""Backends for processing pytket circuits with Honeywell devices
"""

# _metadata.py is copied to the folder after installation.
from ._metadata import __extension_version__, __extension_name__  # type: ignore
from .honeywell import HoneywellBackend
from .api_wrappers import split_utf8
