# pragma version 0.4.0
"""
@license MIT
@title snek_token
@author s3bc40
@notice CU ERC20 token course
"""
# @dev implement interface ensure that contract
# implements all necessary functions or else it
# won't compile
# ------------------------------------------------------------------
#                             IMPORTS
# ------------------------------------------------------------------
from ethereum.ercs import IERC20

implements: IERC20

from snekmate.auth import ownable
from snekmate.tokens import erc20

initializes: ownable
# erc20 uses ownable but does not init it
initializes: erc20[ownable := ownable]

exports: erc20.__interface__

# ------------------------------------------------------------------
#                         STATE VARIABLES
# ------------------------------------------------------------------
NAME: constant(String[25]) = "snek_token"
SYMBOL: constant(String[5]) = "SNEK"
DECIMALS: constant(uint8) = 18
EIP712_VERSION: constant(String[20]) = "1"


# ------------------------------------------------------------------
#                            FUNCTIONS
# ------------------------------------------------------------------
@deploy
def __init__(initial_supply: uint256):
    ownable.__init__()
    erc20.__init__(NAME, SYMBOL, DECIMALS, NAME, EIP712_VERSION)
    erc20._mint(msg.sender, initial_supply)
