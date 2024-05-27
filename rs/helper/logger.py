import os
import shutil

from datetime import datetime
from typing import List

from definitions import ROOT_DIR
from rs.calculator.interfaces.memory_items import MemoryItem
from rs.helper.seed import get_seed_string
from rs.machine.state import GameState

current_run_log_file: str = ''
current_run_log_count: int = 0
current_run_calculator_missing_relics: set[str] = set()
current_run_calculator_missing_potions: set[str] = set()
current_run_calculator_missing_powers: set[str] = set()
current_run_calculator_missing_cards: set[str] = set()
current_run_missing_events: set[str] = set()


def init_run_logging(seed: str):
    dt = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    global current_run_log_file
    global current_run_log_count
    global current_run_calculator_missing_relics
    global current_run_calculator_missing_powers
    global current_run_calculator_missing_cards
    global current_run_calculator_missing_potions
    global current_run_missing_events
    current_run_log_count = 0
    current_run_log_file = "runs/" + dt + "--" + seed
    with open(ROOT_DIR + "/logs/" + current_run_log_file + ".log", 'x') as file:
        file.close()
    log("Seed: " + seed, "calculator_missing_enums")
    current_run_calculator_missing_relics = set()
    current_run_calculator_missing_powers = set()
    current_run_calculator_missing_cards = set()
    current_run_calculator_missing_potions = set()
    current_run_missing_events = set()


def log_to_run(message: str):
    if not current_run_log_file:
        return

    global current_run_log_count
    current_run_log_count += 1
    if current_run_log_count > 10000:
        log("Dying due to this seeming to be stuck", current_run_log_file)
        raise Exception("Dying due to this seeming to be stuck...")
    log(message, current_run_log_file)


def log_calculator_missing_relic(relic_id: str):
    global current_run_calculator_missing_relics
    current_run_calculator_missing_relics.add(relic_id)


def log_calculator_missing_card(card_id: str):
    global current_run_calculator_missing_cards
    current_run_calculator_missing_cards.add(card_id)


def log_calculator_missing_power(power_id: str):
    global current_run_calculator_missing_powers
    current_run_calculator_missing_powers.add(power_id)


def log_calculator_missing_potion(potion_id: str):
    global current_run_calculator_missing_potions
    current_run_calculator_missing_potions.add(potion_id)


def log_missing_event(event_name: str):
    global current_run_missing_events
    current_run_missing_events.add(event_name)


def log_missing_calculator_enums_to_run():
    global current_run_calculator_missing_relics
    global current_run_calculator_missing_powers
    global current_run_calculator_missing_cards
    global current_run_calculator_missing_potions
    global current_run_missing_events
    log(f"Missing relic names:{','.join(current_run_calculator_missing_relics)}", "calculator_missing_enums")
    log(f"Missing power ids:{','.join(current_run_calculator_missing_powers)}", "calculator_missing_enums")
    log(f"Missing card ids:{','.join(current_run_calculator_missing_cards)}", "calculator_missing_enums")
    # log(f"Missing potion names:{','.join(current_run_calculator_missing_potions)}", "calculator_missing_enums")
    log(f"Missing event names:{','.join(current_run_missing_events)}", "calculator_missing_enums")


def log_run_results(state: GameState, elites: List[str], bosses: List[str]):
    message = "Seed:" + get_seed_string(state.game_state()['seed'])
    message += ", Floor:" + str(state.floor())
    message += ", Score:" + str(state.game_state()['screen_state']['score'])
    message += ", DiedTo: "
    for m in state.get_monsters():
        message += m["name"] + ","
    message += " Bosses: " + ",".join(bosses)
    message += " Elites: " + ",".join(elites)
    message += " Relics: "
    for r in state.get_relics():
        message += r["name"] + ","
    if state.memory_general[MemoryItem.KILLED_WITH_LESSON_LEARNED] > 0:
        message += " Killed with Lesson Learned: " + str(state.memory_general[MemoryItem.KILLED_WITH_LESSON_LEARNED])
    message += "\n"
    with open(ROOT_DIR + "/logs/run_history.log", 'a+') as f:
        f.write(message)
        f.close()


def log_new_run_sequence():
    with open(ROOT_DIR + "/logs/run_history.log", 'a+') as f:
        f.write("-------------------------\n")
        f.close()


def log(message, filename="default"):
    f = open(ROOT_DIR + "/logs/" + filename + ".log", "a+")
    f.write(message + "\n")
    f.close()


def init_log(filename="default"):
    with open(ROOT_DIR + "/logs/" + filename + ".log", 'a+') as file:
        file.truncate(0)
        file.close()
    if os.path.exists(ROOT_DIR + "/logs/screenshots"):
        shutil.rmtree(ROOT_DIR + "/logs/screenshots")
    os.makedirs(ROOT_DIR + "/logs/screenshots")
