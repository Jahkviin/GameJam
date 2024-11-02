import item

class reverse(item.Item):
    def __init__(self, position):
        super().__init__(position)

    def use(self, vhsSpeed):
        vhsSpeed = -vhsSpeed
        return vhsSpeed