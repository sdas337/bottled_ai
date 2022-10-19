import math
from typing import List

from rs.calculator.powers import PowerId, Powers, DEBUFFS
from rs.calculator.relics import Relics, RelicId

# hp_damage_dealt
InflictDamageSummary = (int)


class Target:
    def __init__(self, current_hp: int, max_hp: int, block: int, powers: Powers, relics=None):
        if relics is None:
            relics = {}
        self.current_hp: int = current_hp
        self.max_hp: int = max_hp
        self.block: int = block
        self.powers: Powers = powers
        self.relics: Relics = relics

    def inflict_damage(self, source, base_damage: int, hits: int, blockable: bool = True,
                       vulnerable_modifier: float = 1.5,
                       is_attack: bool = True, min_hp_damage: int = 1) -> InflictDamageSummary:
        damage = base_damage
        if self.powers.get(PowerId.VULNERABLE):
            damage = math.floor(damage * vulnerable_modifier)

        health_damage_dealt = 0

        # inflict self damage from sharp_hide
        if is_attack and (self.powers.get(PowerId.SHARP_HIDE)):
            source.inflict_damage(
                source=self,
                base_damage=self.powers.get(PowerId.SHARP_HIDE),
                hits=1,
                vulnerable_modifier=1,
                is_attack=False,
            )

        for hit_damage in [damage for i in range(hits)]:
            if is_attack and (self.powers.get(PowerId.FLAME_BARRIER) or self.powers.get(PowerId.THORNS)):
                source.inflict_damage(
                    source=self,
                    base_damage=self.powers.get(PowerId.FLAME_BARRIER, 0) + self.powers.get(PowerId.THORNS, 0),
                    hits=1,
                    vulnerable_modifier=1,
                    is_attack=False,
                )

            if self.powers.get(PowerId.FLIGHT):
                hit_damage = math.floor(hit_damage * .5) # this may not be entirely accurate, pay attention

            if blockable and self.block:
                if self.block > hit_damage:
                    self.block -= hit_damage
                    hit_damage = 0
                else:
                    hit_damage -= self.block
                    self.block = 0

            if hit_damage > 0:
                if self.relics.get(RelicId.TORII) and hit_damage < 6:
                    hit_damage = 1
                if self.powers.get(PowerId.INTANGIBLE):
                    hit_damage = 1
                if self.relics.get(RelicId.TUNGSTEN_ROD):
                    hit_damage -= 1
                if self.powers.get(PowerId.ANGRY):
                    if not self.powers.get(PowerId.STRENGTH):
                        self.powers[PowerId.STRENGTH] = 0
                    self.powers[PowerId.STRENGTH] += self.powers.get(PowerId.ANGRY)

                if hit_damage > 0:
                    hit_damage = max(hit_damage, min_hp_damage)
                    if self.powers.get(PowerId.BUFFER):
                        self.powers[PowerId.BUFFER] -= 1
                        if not self.powers[PowerId.BUFFER]:
                            del self.powers[PowerId.BUFFER]
                        continue
                    self.current_hp -= hit_damage
                    health_damage_dealt += hit_damage
                    if is_attack and self.powers.get(PowerId.PLATED_ARMOR):
                        self.powers[PowerId.PLATED_ARMOR] -= 1
                    if is_attack and self.powers.get(PowerId.FLIGHT):
                        self.powers[PowerId.FLIGHT] -= 1
                    if is_attack and self.powers.get(PowerId.CURL_UP):
                        self.block = self.powers.get(PowerId.CURL_UP)
                        del self.powers[PowerId.CURL_UP]

                    if self.current_hp < 0:
                        health_damage_dealt += self.current_hp
                        self.current_hp = 0
                        break  # target is dead, stop attacking

            if source.current_hp <= 0:
                source.current_hp = 0
                break  # source is dead, stop attacking

            plated_armor = self.powers.get(PowerId.PLATED_ARMOR, None)
            if plated_armor is not None and plated_armor < 1:
                del self.powers[PowerId.PLATED_ARMOR]

            flight = self.powers.get(PowerId.FLIGHT, None)
            if flight is not None and flight < 1:
                self.damage = 0
                self.hits = 0
                del self.powers[PowerId.FLIGHT]

        return (health_damage_dealt)

    # returns a list of powerIds that were applied and not blocked by artifacts
    def add_powers(self, powers: Powers) -> List[PowerId]:
        applied_powers = []
        for power in powers:
            if power in DEBUFFS and self.powers.get(PowerId.ARTIFACT):
                if self.powers[PowerId.ARTIFACT] == 1:
                    del self.powers[PowerId.ARTIFACT]
                else:
                    self.powers[PowerId.ARTIFACT] -= 1
                continue
            applied_powers.append(power)
            if power in self.powers:
                self.powers[power] += powers[power]
            else:
                self.powers[power] = powers[power]
        return applied_powers

    def get_state_string(self) -> str:
        state: str = f"{self.current_hp},{self.max_hp},{self.block}"
        power_keys = sorted([k.value for k in self.powers.keys()])
        for k in power_keys:
            state += k + str(self.powers[PowerId(k)]) + ","
        return state


class Player(Target):

    def __init__(self, current_hp: int, max_hp: int, block: int, powers: Powers, energy: int, relics: Relics):
        super().__init__(current_hp, max_hp, block, powers, relics)
        self.energy: int = energy

    def get_state_string(self) -> str:
        return super().get_state_string() + str(self.energy) + ","


class Monster(Target):

    def __init__(self, current_hp: int, max_hp: int, block: int, powers: Powers, damage: int = 0, hits: int = 0):
        super().__init__(current_hp, max_hp, block, powers)
        self.damage: int = damage
        self.hits: int = hits

    def get_state_string(self) -> str:
        return super().get_state_string() + f"{self.damage},{self.hits},"
