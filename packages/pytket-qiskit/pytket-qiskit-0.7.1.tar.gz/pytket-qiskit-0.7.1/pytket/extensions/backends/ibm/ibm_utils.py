# Copyright 2019 Cambridge Quantum Computing
#
# You may not use this file except in compliance with the Licence.
# You may obtain a copy of the Licence in the LICENCE file accompanying
# these documents or at:
#
#     https://cqcl.github.io/pytket/build/html/licence.html

"""Shared utility methods for ibm backends.
"""
from typing import List, Iterator, Iterable, Sequence, Type, Tuple
from collections import Counter
import numpy as np  # type: ignore

from qiskit.result import Result  # type: ignore
from qiskit.providers import JobStatus  # type: ignore
from pytket.circuit import Bit, Qubit, UnitID  # type: ignore
from pytket.backends.status import StatusEnum
from pytket.backends.backendresult import BackendResult
from pytket.utils.outcomearray import OutcomeArray

_STATUS_MAP = {
    JobStatus.CANCELLED: StatusEnum.CANCELLED,
    JobStatus.ERROR: StatusEnum.ERROR,
    JobStatus.DONE: StatusEnum.COMPLETED,
    JobStatus.INITIALIZING: StatusEnum.SUBMITTED,
    JobStatus.VALIDATING: StatusEnum.SUBMITTED,
    JobStatus.QUEUED: StatusEnum.QUEUED,
    JobStatus.RUNNING: StatusEnum.RUNNING,
}
