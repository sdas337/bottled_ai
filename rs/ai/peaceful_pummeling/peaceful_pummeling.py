from typing import List

from rs.ai.peaceful_pummeling.config import CARD_REMOVAL_PRIORITY_LIST, DESIRED_CARDS_FOR_DECK, HIGH_PRIORITY_UPGRADES, \
    DESIRED_CARDS_FROM_POTIONS
from rs.ai.peaceful_pummeling.handlers.boss_relic_handler import BossRelicHandler
from rs.ai.peaceful_pummeling.handlers.combat_reward_handler import CombatRewardHandler
from rs.ai.peaceful_pummeling.handlers.event_handler import EventHandler
from rs.ai.peaceful_pummeling.handlers.potions_handler import PotionsBossHandler, PotionsEventFightHandler, PotionsEliteHandler
from rs.ai.peaceful_pummeling.handlers.shop_purchase_handler import ShopPurchaseHandler
from rs.ai.peaceful_pummeling.handlers.upgrade_handler import UpgradeHandler
from rs.common.handlers.common_astrolabe_handler import CommonAstrolabeHandler
from rs.common.handlers.common_battle_handler import CommonBattleHandler
from rs.common.handlers.common_campfire_handler import CommonCampfireHandler
from rs.common.handlers.card_reward.common_card_reward_handler import CommonCardRewardHandler
from rs.common.handlers.common_chest_handler import CommonChestHandler
from rs.common.handlers.common_discard_handler import CommonDiscardHandler
from rs.common.handlers.common_map_handler import CommonMapHandler
from rs.common.handlers.common_neow_handler import CommonNeowHandler
from rs.common.handlers.common_purge_handler import CommonPurgeHandler
from rs.common.handlers.common_shop_entrance_handler import CommonShopEntranceHandler
from rs.common.handlers.common_transform_handler import CommonTransformHandler
from rs.machine.ai_strategy import AiStrategy
from rs.machine.character import Character
from rs.machine.handlers.handler import Handler

peaceful_pummeling_potion_handlers: List[Handler] = [
    # Potions Handlers First
    PotionsBossHandler(),
    PotionsEventFightHandler(),
    PotionsEliteHandler(),
]

PEACEFUL_PUMMELING: AiStrategy = AiStrategy(
    character=Character.WATCHER,
    handlers=peaceful_pummeling_potion_handlers + [
        CommonAstrolabeHandler(CARD_REMOVAL_PRIORITY_LIST),
        CommonBattleHandler(),
        BossRelicHandler(),
        UpgradeHandler(),
        CommonTransformHandler(CARD_REMOVAL_PRIORITY_LIST),
        CommonPurgeHandler(CARD_REMOVAL_PRIORITY_LIST),
        CombatRewardHandler(),
        CommonCardRewardHandler(DESIRED_CARDS_FOR_DECK, DESIRED_CARDS_FROM_POTIONS),
        CommonNeowHandler(),
        EventHandler(),
        CommonChestHandler(),
        CommonMapHandler(),
        CommonCampfireHandler(HIGH_PRIORITY_UPGRADES),
        CommonShopEntranceHandler(),
        ShopPurchaseHandler(),
        CommonDiscardHandler(),
    ]
)