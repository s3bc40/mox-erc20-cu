import boa
from eth.constants import ZERO_ADDRESS
from eth_utils import to_wei

from script.deploy import INITIAL_SUPPLY

RANDOM_USER = boa.env.generate_address("random")
TRANSFER_AMOUNT = to_wei(100, "ether")
EXCEED_TRANSFER_AMOUNT = to_wei(5000, "ether")


def test_token_supply(snek_contract):
    assert snek_contract.totalSupply() == INITIAL_SUPPLY


def test_token_emits_event(snek_contract):
    with boa.env.prank(snek_contract.owner()):
        snek_contract.transfer(RANDOM_USER, INITIAL_SUPPLY)
        logs = snek_contract.get_logs()
        log_owner = logs[0].topics[0]
        assert log_owner == snek_contract.owner()
    assert snek_contract.balanceOf(RANDOM_USER) == INITIAL_SUPPLY


# WORKSHOP
def test_token_transfer_empty_address_should_fail(snek_contract):
    print("snek_contract.owner()", snek_contract.owner())
    with boa.env.prank(snek_contract.owner()):
        with boa.reverts("erc20: transfer to the zero address"):
            snek_contract.transfer_from_owner(ZERO_ADDRESS.hex(), TRANSFER_AMOUNT)


def test_token_tranfer_not_enough_balance_should_fail(snek_contract):
    with boa.env.prank(snek_contract.owner()):
        with boa.reverts("erc20: transfer amount exceeds balance"):
            snek_contract.transfer_from_owner(RANDOM_USER, EXCEED_TRANSFER_AMOUNT)


def test_token_transfer_from_owner(snek_contract):
    with boa.env.prank(snek_contract.owner()):
        snek_contract.transfer_from_owner(RANDOM_USER, TRANSFER_AMOUNT)

    assert snek_contract.balanceOf(RANDOM_USER) == TRANSFER_AMOUNT
    assert (
        snek_contract.balanceOf(snek_contract.owner())
        == INITIAL_SUPPLY - TRANSFER_AMOUNT
    )
    assert snek_contract.totalSupply() == INITIAL_SUPPLY
