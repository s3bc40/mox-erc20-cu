from snekmate.auth import ownable

initializes: ownable

@deploy
def __init__():
    ownable.__init__()
    
