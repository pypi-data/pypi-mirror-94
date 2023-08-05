"""
This is a qiskit provider for the QC Ware "Forge" product,
allowing evaluation of circuits on a local simulator or 
our hosted GPU-accelerated quantum simulators
"""

from .qcware_job import QcwareJob
from .qcware_provider import QcwareProvider
from .version import __version__
