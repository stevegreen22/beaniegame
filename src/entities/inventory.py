
# inventory object owned by the chest, player, animal etc
# animal inv will be the meat that it drops
# chest inventory will be the loot inside
# player inv is player inv.
# each inventory item will have it's own max qty per slot
class Inventory:
    def __init__(self, inv_type, inv_loot = None):
        self.inventory = []
