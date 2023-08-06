# Copyright 2020-2021 Cambridge Quantum Computing
#
# You may not use this file except in compliance with the Licence.
# You may obtain a copy of the Licence in the LICENCE file accompanying
# these documents or at:
#
#     https://cqcl.github.io/pytket/build/html/licence.html

"""Backends for processing pytket circuits with the Microsoft QDK
"""

# _metadata.py is copied to the folder after installation.
from ._metadata import __extension_version__, __extension_name__  # type: ignore
from .simulator import QsharpSimulatorBackend
from .estimator import QsharpEstimatorBackend
from .toffoli import QsharpToffoliSimulatorBackend
from .azure_quantum import AzureBackend
