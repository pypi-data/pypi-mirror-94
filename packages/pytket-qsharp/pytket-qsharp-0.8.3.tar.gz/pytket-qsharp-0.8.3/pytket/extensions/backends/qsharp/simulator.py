# Copyright 2020-2021 Cambridge Quantum Computing
#
# You may not use this file except in compliance with the Licence.
# You may obtain a copy of the Licence in the LICENCE file accompanying
# these documents or at:
#
#     https://cqcl.github.io/pytket/build/html/licence.html

from typing import TYPE_CHECKING, Optional

import numpy as np
from .common import _QsharpSimBaseBackend, BackendResult
from pytket.utils.outcomearray import OutcomeArray

if TYPE_CHECKING:
    from qsharp.loader import QSharpCallable  # type: ignore


class QsharpSimulatorBackend(_QsharpSimBaseBackend):
    """Backend for simulating a circuit using the QDK."""

    _supports_shots = True
    _supports_counts = True

    def _calculate_results(
        self, qscall: "QSharpCallable", n_shots: Optional[int] = None
    ) -> BackendResult:
        if n_shots:
            shots_ar = np.array(
                [qscall.simulate() for _ in range(n_shots)], dtype=np.uint8
            )
            shots = OutcomeArray.from_readouts(shots_ar)  # type: ignore
            # ^ type ignore as array is ok for Sequence[Sequence[int]]
            # outputs should correspond to default register,
            # as mapped by FlattenRegisters()
            return BackendResult(shots=shots)
        raise ValueError("Parameter n_shots is required for this backend")
