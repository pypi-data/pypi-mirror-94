# Copyright 2020-2021 Cambridge Quantum Computing
#
# You may not use this file except in compliance with the Licence.
# You may obtain a copy of the Licence in the LICENCE file accompanying
# these documents or at:
#
#     https://cqcl.github.io/pytket/build/html/licence.html

from typing import TYPE_CHECKING, Optional, Union, Dict

from pytket.backends import ResultHandle, StatusEnum
from pytket.circuit import Circuit  # type: ignore

from .common import _QsharpBaseBackend, BackendResult

if TYPE_CHECKING:
    from typing import MutableMapping
    from qsharp.loader import QSharpCallable  # type: ignore

ResourcesResult = Dict[str, int]


class QsharpEstimatorBackend(_QsharpBaseBackend):
    """ Backend for estimating resources of a circuit using the QDK. """

    def _calculate_results(
        self, qscall: "QSharpCallable", n_shots: Optional[int] = None
    ) -> Union[BackendResult, "MutableMapping"]:
        results = qscall.estimate_resources()
        results["Measure"] = 0  # Measures were added by qscompile()
        return results  # type: ignore

    def get_resources(self, circuit: Union[Circuit, ResultHandle]) -> ResourcesResult:
        """Calculate resource estimates for circuit.

        :param circuit: Circuit to calculate or result handle to retrieve for
        :type circuit: Union[Circuit, ResultHandle]
        :return: Resource estimate
        :rtype: Dict[str, int]
        """
        if isinstance(circuit, Circuit):
            handle = self.process_circuits([circuit])[0]
        elif isinstance(circuit, ResultHandle):
            handle = circuit
            circ_status = self.circuit_status(handle)
            if circ_status.status is not StatusEnum.COMPLETED:
                raise ValueError(f"Handle is '{circ_status}'")
        else:
            raise TypeError(
                "Provide either a Circuit to run or a ResultHandle to a previously submitted circuit."
            )
        return self._cache[handle]["resource"]  # type: ignore
