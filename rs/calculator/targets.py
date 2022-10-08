import math

from rs.calculator.powers import PowerId, Powers


class Target:
    def __init__(self, current_hp: int, max_hp: int, block: int, powers: Powers):
        self.current_hp: int = current_hp
        self.max_hp: int = max_hp
        self.block: int = block
        self.powers: Powers = powers

    def inflict_damage(self, base_damage: int, hits: int, blockable: bool = True, vulnerable_modifier: float = 1.5):
        damage = base_damage
        if PowerId.VULNERABLE in self.powers and self.powers[PowerId.VULNERABLE]:
            damage = math.floor(damage * vulnerable_modifier)
        damage *= hits
        if blockable:
            self.block -= damage
            if self.block < 0:
                self.current_hp += self.block
                self.block = 0
        else:
            self.current_hp -= damage
        self.current_hp = max(0, self.current_hp)

    def add_powers(self, powers: Powers):
        keys = dict.keys(powers)
        for power in powers:
            if power in self.powers:
                self.powers[power] += powers[power]
            else:
                self.powers[power] = powers[power]


class Player(Target):

    def __init__(self, current_hp: int, max_hp: int, block: int, powers: Powers, energy: int):
        super().__init__(current_hp, max_hp, block, powers)
        self.energy: int = energy
