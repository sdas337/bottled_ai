from rs.ai.unnamed_defect_build.config import CARD_REMOVAL_PRIORITY_LIST
from rs.ai.unnamed_defect_build.handlers.event_handler import EventHandler
from rs.ai.unnamed_defect_build.handlers.shop_purchase_handler import ShopPurchaseHandler
from rs.ai.unnamed_defect_build.handlers.upgrade_handler import UpgradeHandler
from rs.common.handlers.card_reward.common_card_reward_take_first_card_handler import \
    CommonCardRewardTakeFirstCardHandler
from rs.common.handlers.common_astrolabe_handler import CommonAstrolabeHandler
from rs.common.handlers.common_battle_handler import CommonBattleHandler
from rs.common.handlers.common_boss_relic_handler import CommonBossRelicHandler
from rs.common.handlers.common_campfire_handler import CommonCampfireHandler
from rs.common.handlers.common_chest_handler import CommonChestHandler
from rs.common.handlers.common_combat_reward_handler import CommonCombatRewardHandler
from rs.common.handlers.common_discard_handler import CommonDiscardHandler
from rs.common.handlers.common_map_handler import CommonMapHandler
from rs.common.handlers.common_neow_handler import CommonNeowHandler
from rs.common.handlers.common_purge_handler import CommonPurgeHandler
from rs.common.handlers.common_shop_entrance_handler import CommonShopEntranceHandler
from rs.common.handlers.common_transform_handler import CommonTransformHandler
from rs.machine.ai_strategy import AiStrategy
from rs.machine.character import Character

UNNAMED_DEFECT_STRATEGY: AiStrategy = AiStrategy(
    character=Character.DEFECT,
    handlers=[
        CommonAstrolabeHandler(CARD_REMOVAL_PRIORITY_LIST),
        CommonBattleHandler(),
        CommonBossRelicHandler(),
        UpgradeHandler(),
        CommonTransformHandler(CARD_REMOVAL_PRIORITY_LIST),
        CommonPurgeHandler(CARD_REMOVAL_PRIORITY_LIST),
        CommonCombatRewardHandler(),
        CommonCardRewardTakeFirstCardHandler(),
        CommonNeowHandler(),
        EventHandler(),
        CommonChestHandler(),
        CommonMapHandler(),
        CommonCampfireHandler(),
        CommonShopEntranceHandler(),
        ShopPurchaseHandler(),
        CommonDiscardHandler(),
    ]
)
