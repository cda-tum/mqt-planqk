"""Template for implementing services running on the PlanQK platform"""

from __future__ import annotations

import time
from typing import Any

from loguru import logger
from mqt.ddsim import DDSIMProvider
from qiskit import QuantumCircuit, qasm2, qasm3

from .libs.return_objects import ErrorResponse, ResultResponse


def run(data: dict[str, Any] | None = None, params: dict[str, Any] | None = None) -> ResultResponse | ErrorResponse:
    """Default entry point of your code. Start coding here!

    Parameters:
        data: The input data sent by the client
        params: Contains parameters, which can be set by the client to configure the execution

    Returns:
        response: Response as arbitrary json-serializable dict or an error to be passed back to the client
    """
    qc_qasm: str | None = data.get("qc")
    if qc_qasm is None:
        return ErrorResponse(code="400", detail="No input circuit provided.")

    shots: int = params.get("shots", 1024)

    try:
        qc = QuantumCircuit.from_qasm_str(qc_qasm)
    except qasm2.QASM2ParseError:
        try:
            qc = qasm3.loads(qc_qasm)
        except qasm3.QASM3ImporterError as e:
            return ErrorResponse(code="400", detail=f"Invalid input circuit provided. Error: {e}")

    provider = DDSIMProvider()
    backend = provider.get_backend("qasm_simulator")

    start_time = time.time()

    logger.info("Starting execution...")
    job = backend.run(qc, shots=shots)
    counts = job.result().get_counts()

    logger.info("Finished execution")
    execution_time = time.time() - start_time

    result = {
        "counts": counts,
    }
    metadata = {
        "execution_time": round(execution_time, 3),
    }

    logger.info("Calculation successfully executed")

    return ResultResponse(result=result, metadata=metadata)
