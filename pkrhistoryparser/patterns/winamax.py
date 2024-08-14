"""
This module contains regular expressions used to parse Winamax hand histories.
"""
# HAND HISTORY PATTERNS
PLAYER_PATTERN = r"Seat (\d+): ([\w\s.\-&]{3,12}) \((\d+)(?:, ([\d\.]+)\D)?"
BLINDS_PATTERN = r"(\n[\w\s\-&.]{3,12})\s+posts\s+(small blind|big blind|ante)\s+([\d.,]+)"
DATETIME_PATTERN = r"- (\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) UTC"
TOURNAMENT_BLINDS_PATTERN = r"\((\d+)/(\d+)/(\d+)\)"
OTHER_BLINDS_PATTERN = r"\(([\d€.]+)/([\d€.]+)\)"
LEVEL_PATTERN = r"level: (\d+)"
NORMAL_BUY_IN_PATTERN = r"buyIn:\s+([\d.,]+)€\s+\+\s+([\d.,]+)€"
KO_BUY_IN_PATTERN = r"buyIn: ([\d.,]+)€ \+ ([\d.,]+)€ \+ ([\d.,]+)€"
FREE_ROLL_PATTERN = r"buyIn: Free"
MAX_PLAYERS_PATTERN = r"(\d+)-max"
BUTTON_SEAT_PATTERN = r"Seat #(\d+) is the button"
TABLE_NAME_PATTERN = r"Table: '(.*)' "
TOURNAMENT_INFO_PATTERN = r"Table: [\'\"]([\w\s\-&\€\:\.\'\"\[\]]+)\((\d+)\)\#(\d+)"
TABLE_IDENT_PATTERN = r"(\(\d+\)#\d+)"
HERO_HAND_PATTERN = r"Dealt to ([\w\s.\-&]{3,12}) \[(\w\w) (\w\w)\]"
FLOP_PATTERN = r"\*\*\* FLOP \*\*\* \[(\w\w) (\w\w) (\w\w)\]"
TURN_PATTERN = r"\*\*\* TURN \*\*\* \[\w\w \w\w \w\w\]\[(\w\w)\]"
RIVER_PATTERN = r"\*\*\* RIVER \*\*\* \[\w\w \w\w \w\w \w\w\]\[(\w\w)\]"
ACTION_PATTERN = r"\n(?P<pl_name>[\w\s\-&.]{3,12})\s+(?P<move>calls|bets|raises|folds|checks)(?: (?P<value>\d+))?"
SHOWDOWN_PATTERN = r"((?:(?!\n).)+)\s+shows\s+\[(\w\w) (\w\w)\]"
WINNERS_PATTERN = r"\n([\w\s.\-&]{3,12}) collected (\d+) from (pot|main pot|side pot \d+)"
HAND_ID_PATTERN = r"HandId: #([\d\-]+)"
PREFLOP_ACTION_PATTERN = r"\*\*\*\sPRE-FLOP\s\*\*\*([&\w\s.€-]+)"
FLOP_ACTION_PATTERN = r"\*\*\*\sFLOP\s\*\*\*\s\[[\w\s]+\]([&\w\s.€-]+)"
TURN_ACTION_PATTERN = r"\*\*\*\sTURN\s\*\*\*\s\[[\w\s]+\]\[[\w\s]+\]([&\w\s.€-]+)"
RIVER_ACTION_PATTERN = r"\*\*\*\sRIVER\s\*\*\*\s\[[\w\s]+\]\[[\w\s]+\]([&\w\s.€-]+)"
STREET_ACTION_PATTERNS = [PREFLOP_ACTION_PATTERN, FLOP_ACTION_PATTERN, TURN_ACTION_PATTERN, RIVER_ACTION_PATTERN]
# TOURNAMENT INFO PATTERNS
SPLIT_PATTERN = r"Winamax\sPoker\s-\sTournament\ssummary"
PRIZE_POOL_PATTERN = r"Prizepool[\s\:]+([\d\.\,]+)\s?€"
REGISTERED_PLAYERS_PATTERN = r"Registered\s+players\s+:\s+(\d+)"
SPEED_PATTERN = r"Speed\s+:\s+(\w+)"
LEVELS_STRUCTURE_PATTERN = r"Levels\s+:\s+\[((.){2,})\]"
START_DATE_PATTERN = r"(\d{4}/\d{2}/\d{2}\s\d{2}:\d{2}:\d{2}\sUTC)"
LEVEL_BLINDS_PATTERN = r"\,?([\dkM\,]+)-([\dkM\,]+):([\dkM\,]+)"
TOURNAMENT_TYPE_PATTERN = r"Type\s+:\s+(\w+)"
SUMMARY_TOURNAMENT_INFO_PATTERN = r"Tournament summary[\:\s]+([\wé\s\-&\€\:\.\'\!\\\[\]]+)\((\d+)\)"
BUY_IN_PATTERN = r"Buy-In[\s\:]+([\d\.\,]+)\s?€\s?\+?\s?([\d\.\,]+)?\s?€?\s?\+\s([\d\.\,]+)"
AMOUNT_WON_PATTERN = r"You\s+won\s+([\d\.\,]+)€"
FINAL_POSITION_PATTERN = r"You\sfinished\sin\s(\d+)"


