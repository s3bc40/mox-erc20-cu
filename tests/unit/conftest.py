import pytest
from moccasin.boa_tools import VyperContract

from script import deploy


@pytest.fixture(scope="function")
def snek_contract() -> VyperContract:
    """
    @dev deploy snek contract fixture
    """
    return deploy.deploy()
