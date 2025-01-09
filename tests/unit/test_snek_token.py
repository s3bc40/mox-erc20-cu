import boa

from script.deploy import INITIAL_SUPPLY

RANDOM_USER = boa.env.generate_address("random")


def test_token_supply(snek_contract):
    assert snek_contract.totalSupply() == INITIAL_SUPPLY


def test_token_emits_event(snek_contract):
    with boa.env.prank(snek_contract.owner()):
        snek_contract.transfer(RANDOM_USER, INITIAL_SUPPLY)
        logs = snek_contract.get_logs()
        log_owner = logs[0].topics[0]
        assert log_owner == snek_contract.owner()
    assert snek_contract.balanceOf(RANDOM_USER) == INITIAL_SUPPLY
