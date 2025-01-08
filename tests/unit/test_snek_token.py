from script.deploy import INITIAL_SUPPLY


def test_token_supply(snek_contract):
    assert snek_contract.totalSupply() == INITIAL_SUPPLY
