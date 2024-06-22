import unittest
import os
from dotenv import load_dotenv
from pkrhistoryparser.parser import HandHistoryParser

env_path = os.path.join(os.path.dirname(__file__), ".env.test")
load_dotenv(env_path)
SOURCE_DIR = os.environ.get("SOURCE_DIR")

HISTORIES_DIR = os.path.join(SOURCE_DIR, "histories")
SUMMARIES_DIR = os.path.join(SOURCE_DIR, "summaries")
SPLIT_HISTORIES_DIR = os.path.join(HISTORIES_DIR, "split")
PARSED_HISTORIES_DIR = os.path.join(HISTORIES_DIR, "parsed")
TEST_DIR = os.path.dirname(os.path.abspath(__file__))

if not os.path.exists(SPLIT_HISTORIES_DIR):
    SPLIT_HISTORIES_DIR = SPLIT_HISTORIES_DIR.replace("C:/", "/mnt/c/")
if not os.path.exists(SUMMARIES_DIR):
    SUMMARIES_DIR.replace("C:/", "/mnt/c/")
if not os.path.exists(TEST_DIR):
    TEST_DIR.replace("C:/", "/mnt/c/")


class TestHandHistoryParser(unittest.TestCase):
    def setUp(self):

        self.parser = HandHistoryParser(
            split_dir=SPLIT_HISTORIES_DIR,
            parsed_dir=TEST_DIR,
            summaries_dir=SUMMARIES_DIR
        )
        self.example_file_name = "2612804708405870609-6-1672853787.txt"
        split_histories = self.parser.split_histories
        example_split_history = [path for path in split_histories if self.example_file_name in path.get("filename")][0]
        split_path = self.parser.get_split_path(
            root=example_split_history.get("root"),
            filename=example_split_history.get("filename")
        )
        self.file_path = split_path
        self.hand_text = self.parser.get_raw_text(self.file_path)

    def test_split_histories(self):
        self.assertIsInstance(self.parser.split_histories, list)

    def test_check_is_parsed(self):
        self.assertTrue(self.parser.check_is_parsed(self.file_path))
        self.assertFalse(self.parser.check_is_parsed("not_a_file.txt"))

    def test_path_to_list(self):
        path = self.file_path
        path_list = self.parser.path_to_list(path)
        self.assertIsInstance(path_list, list)

    def test_get_summary_path(self):
        path = self.file_path
        summary_path = self.parser.get_summary_path(path)
        self.assertTrue(os.path.exists(summary_path))

    def test_get_destination_path(self):
        destination_path = self.parser.get_destination_path(self.file_path)
        self.assertIn(
            destination_path,
            [
                'C:\\Users\\mangg\\projects\\PokerHistoryParser\\tests\\2023\\01\\04\\608341002\\'
                '2612804708405870609-6-1672853787.json',
                '/mnt/c/Users/mangg/projects/PokerHistoryParser/tests/2023/01/04/608341002/'
                '2612804708405870609-6-1672853787.json'
            ]
            )

    def test_parse_all(self):
        self.parser.parse_all()
        self.assertTrue(os.path.exists(self.parser.parsed_dir))
        self.assertTrue(os.path.exists(self.parser.get_destination_path(self.file_path)))

    def test_get_split_path(self):
        split_histories = self.parser.split_histories
        example_split_history = [path for path in split_histories if self.example_file_name in path.get("filename")][0]
        split_path = self.parser.get_split_path(
            root=example_split_history.get("root"),
            filename=example_split_history.get("filename")
        )
        self.assertTrue(os.path.exists(split_path))

    def test_extract_game_type(self):
        result = self.parser.extract_game_type(self.hand_text)
        self.assertEqual(result, {"game_type": "Tournament"})

    def test_extract_players(self):
        result = self.parser.extract_players(self.hand_text)
        expected_result = {
            1: {"seat": 1, "name": "FrenchAAAA", "init_stack": 19575.0, "bounty": 2.25},
            2: {"seat": 2, "name": "daifwa", "init_stack": 21830.0, "bounty": 2.25},
            3: {"seat": 3, "name": "Roomxx", "init_stack": 34263.0, "bounty": 3.37},
            4: {"seat": 4, "name": "SB Warrior34", "init_stack": 18548.0, "bounty": 2.25},
            5: {"seat": 5, "name": "GoToVG", "init_stack": 26609.0, "bounty": 2.25},
            6: {"seat": 6, "name": "manggy94", "init_stack": 19175.0, "bounty": 2.25}
        }
        self.assertEqual(result, expected_result)

    def test_extract_posting(self):
        result = self.parser.extract_posting(self.hand_text)
        expected_result = [
            {"name": "GoToVG", "amount": 25.0, "blind_type": "ante"},
            {"name": "manggy94", "amount": 25.0, "blind_type": "ante"},
            {"name": "FrenchAAAA", "amount": 25.0, "blind_type": "ante"},
            {"name": "daifwa", "amount": 25.0, "blind_type": "ante"},
            {"name": "Roomxx", "amount": 25.0, "blind_type": "ante"},
            {"name": "SB Warrior34", "amount": 25.0, "blind_type": "ante"},
            {"name": "GoToVG", "amount": 100.0, "blind_type": "small blind"},
            {"name": "manggy94", "amount": 200.0, "blind_type": "big blind"}
        ]
        self.assertEqual(result, expected_result)

    def test_extract_buy_in(self):
        result = self.parser.extract_buy_in(self.hand_text)
        expected_result = {"prize_pool_contribution": 4.5, "bounty": 0.0, "rake": 0.5}
        self.assertEqual(result, expected_result)

    def test_extract_datetime(self):
        result = self.parser.extract_datetime(self.hand_text)
        expected_result = {"datetime": "04-01-2023 17:36:27"}
        self.assertEqual(result, expected_result)

    def test_extract_blinds(self):
        result = self.parser.extract_blinds(self.hand_text)
        expected_result = {"ante": 25.0, "sb": 100.0, "bb": 200.0}
        self.assertEqual(result, expected_result)

    def test_extract_level(self):
        result = self.parser.extract_level(self.hand_text)
        expected_result = {"level": 1}
        self.assertEqual(result, expected_result)

    def test_extract_max_players(self):
        result = self.parser.extract_max_players(self.hand_text)
        expected_result = {"max_players": 6}
        self.assertEqual(result, expected_result)

    def test_extract_button_seat(self):
        result = self.parser.extract_button_seat(self.hand_text)
        expected_result = {"button": 4}
        self.assertEqual(result, expected_result)

    def test_extract_tournament_info(self):
        result = self.parser.extract_tournament_info(self.hand_text)
        expected_result = {"tournament_name": "GUERILLA", "tournament_id": "608341002", "table_number": "016"}
        self.assertEqual(result, expected_result)

    def test_extract_hero_hand(self):
        result = self.parser.extract_hero_hand(self.hand_text)
        expected_result = {"hero": "manggy94", "first_card": "2c", "second_card": "5h"}
        self.assertEqual(result, expected_result)

    def test_extract_flop(self):
        result = self.parser.extract_flop(self.hand_text)
        expected_result = {"flop_card_1": "7h", "flop_card_2": "2d", "flop_card_3": "5c"}
        self.assertEqual(result, expected_result)

    def test_extract_turn(self):
        result = self.parser.extract_turn(self.hand_text)
        expected_result = {"turn_card": "2h"}
        self.assertEqual(result, expected_result)

    def test_extract_river(self):
        result = self.parser.extract_river(self.hand_text)
        expected_result = {"river_card": "8c"}
        self.assertEqual(result, expected_result)

    def test_extract_showdown(self):
        result = self.parser.extract_showdown(self.hand_text)
        expected_result = {}
        self.assertEqual(result, expected_result)

    def test_extract_winners(self):
        result = self.parser.extract_winners(self.hand_text)
        expected_result = {"GoToVG": {"amount": 7575.0, "pot_type": "pot"}}
        self.assertEqual(result, expected_result)

    def test_extract_hand_id(self):
        result = self.parser.extract_hand_id(self.hand_text)
        expected_result = {"hand_id": "2612804708405870609-6-1672853787"}
        self.assertEqual(result, expected_result)

    def test_extract_actions(self):
        result = self.parser.extract_actions(self.hand_text)
        expected_result = {
            'preflop': [
                {'player': 'FrenchAAAA', 'action': 'folds', 'amount': 0.0},
                {'player': 'daifwa', 'action': 'calls', 'amount': 200.0},
                {'player': 'Roomxx', 'action': 'folds', 'amount': 0.0},
                {'player': 'SB Warrior34', 'action': 'calls', 'amount': 200.0},
                {'player': 'GoToVG', 'action': 'raises', 'amount': 700.0},
                {'player': 'manggy94', 'action': 'folds', 'amount': 0.0},
                {'player': 'daifwa', 'action': 'calls', 'amount': 700.0},
                {'player': 'SB Warrior34', 'action': 'calls', 'amount': 700.0},
            ],
            'flop': [
                {'player': 'GoToVG', 'action': 'checks', 'amount': 0.0},
                {'player': 'daifwa', 'action': 'checks', 'amount': 0.0},
                {'player': 'SB Warrior34', 'action': 'checks', 'amount': 0.0},
            ],
            'turn': [
                {'player': 'GoToVG', 'action': 'bets', 'amount': 1000.0},
                {'player': 'daifwa', 'action': 'folds', 'amount': 0.0},
                {'player': 'SB Warrior34', 'action': 'calls', 'amount': 1000.0}
            ],
            'river': [
                {'player': 'GoToVG', 'action': 'bets', 'amount': 2525.0},
                {'player': 'SB Warrior34', 'action': 'folds', 'amount': 0.0}
            ]
        }
        self.assertEqual(result, expected_result)

    def test_parse_hand(self):
        result = self.parser.parse_hand(self.hand_text)
        self.assertIsInstance(result, dict)
        self.assertEqual(
            set(result.keys()),
            {'hand_id', 'datetime', 'game_type', 'buy_in', 'level', 'max_players', 'button_seat', 'players',
             'tournament_info', 'hero_hand', 'postings', 'actions', 'flop', 'turn', 'river', 'showdown',
             'winners'
             }
        )

    def test_extract_levels_structure(self):
        with open(os.path.join(TEST_DIR, "test_summary.txt"), "r") as f:
            summary_text = f.read()
        levels_structure = self.parser.extract_levels_structure(summary_text)
        self.assertIsInstance(levels_structure, dict)
        self.assertIsInstance(levels_structure.get("levels_structure"), list)
        for level in levels_structure.get("levels_structure"):
            self.assertIsInstance(level, dict)
            self.assertIn("value", level.keys())
            self.assertIsInstance(level.get("value"), int)
            self.assertIn("sb", level.keys())
            self.assertIsInstance(level.get("sb"), float)
            self.assertIn("bb", level.keys())
            self.assertIsInstance(level.get("bb"), float)
            self.assertIn("ante", level.keys())
            self.assertIsInstance(level.get("ante"), float)

    def test_parse_to_json(self):
        file_path = self.file_path
        destination_path = self.parser.get_destination_path(file_path)
        self.parser.parse_to_json(file_path)
        self.assertTrue(os.path.exists(destination_path))



