import unittest
import os
from dotenv import load_dotenv
from pkrhistoryparser.history_parsers.local import LocalHandHistoryParser
from pkrhistoryparser.summary_parsers.local import LocalSummaryParser

load_dotenv()
TEST_DATA_DIR = os.environ.get("TEST_DATA_DIR")
TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class TestSummaryParser(unittest.TestCase):
    def setUp(self):
        self.parser = LocalSummaryParser(data_dir=TEST_DATA_DIR)
        self.file_key = [key for key in self.parser.list_summary_keys()
                         if "651237360.txt" in key][0]
        self.summary_text = self.parser.get_text(self.file_key)

    def test_list_summary_keys(self):
        self.assertIsInstance(self.parser.list_summary_keys(), list)

    def test_extract_buy_in(self):
        result = self.parser.extract_buy_in(self.summary_text)
        expected_result = {"prize_pool_contribution": 4.5, "bounty": 4.50, "rake": 1.0}
        self.assertEqual(result, expected_result)

    def test_extract_tournament_id(self):
        result = self.parser.extract_tournament_id(self.summary_text)
        expected_result = {"tournament_id": "651237360"}
        self.assertEqual(result, expected_result)

    def test_extract_tournament_name(self):
        result = self.parser.extract_tournament_name(self.summary_text)
        expected_result = {"tournament_name": "RING"}
        self.assertEqual(result, expected_result)

    def test_extract_tournament_type(self):
        result = self.parser.extract_tournament_type(self.summary_text)
        expected_result = {"tournament_type": "knockout"}
        self.assertEqual(result, expected_result)

    def test_extract_tournament_speed(self):
        result = self.parser.extract_speed(self.summary_text)
        expected_result = {"speed": "normal"}
        self.assertEqual(result, expected_result)

    def test_extract_touenament_prize_pool(self):
        result = self.parser.extract_prize_pool(self.summary_text)
        expected_result = {"prize_pool": 3240}
        self.assertEqual(result, expected_result)

    def test_extract_registered_players(self):
        result = self.parser.extract_registered_players(self.summary_text)
        expected_result = {"registered_players": 605}
        self.assertEqual(result, expected_result)

    def test_extract_tournament_start_date(self):
        result = self.parser.extract_start_date(self.summary_text)
        expected_result = {"start_date": "2023/05/07 14:00:00 UTC"}
        self.assertEqual(result, expected_result)

    def test_extract_amount_won(self):
        result = self.parser.extract_amount_won(self.summary_text)
        expected_result = {"amount_won": 0.0}
        self.assertEqual(result, expected_result)

    def test_extract_final_position(self):
        result = self.parser.extract_final_position(self.summary_text)
        expected_result = {"final_position": 223}
        self.assertEqual(result, expected_result)

    def test_parse_tournament_summary(self):
        result = self.parser.parse_tournament_summary(self.summary_text)
        self.assertIsInstance(result, dict)
        self.assertEqual(
            set(result.keys()),
            {'tournament_id', 'tournament_name', 'buy_in', 'prize_pool', 'registered_players', 'speed',
             'start_date', 'levels_structure', 'tournament_type', 'amount_won', 'final_position'}
        )


class TestHandHistoryParser(unittest.TestCase):
    def setUp(self):

        self.parser = LocalHandHistoryParser(data_dir=TEST_DATA_DIR)
        self.file_key = [key for key in self.parser.list_split_histories_keys()
                         if "2612804708405870609-6-1672853787.txt" in key][0]
        self.hand_text = self.parser.get_text(self.file_key)

    def test_list_split_histories_keys(self):
        self.assertIsInstance(self.parser.list_split_histories_keys(), list)

    def test_check_is_parsed(self):
        right_split_key = self.file_key.replace("data_test", "data")
        self.assertTrue(self.parser.check_is_parsed(right_split_key))
        self.assertFalse(self.parser.check_is_parsed("not_a_file.txt"))

    def test_get_parsed_key(self):
        parsed_key = self.parser.get_parsed_key(self.file_key)
        self.assertIn("2612804708405870609-6-1672853787.json", parsed_key)
        self.assertIn("parsed", parsed_key)

    def test_parse_new_hand_history(self):
        self.parser.parse_new_hand_history(self.file_key)
        self.assertTrue(os.path.exists(self.parser.parsed_dir))
        self.assertTrue(os.path.exists(self.parser.get_parsed_key(self.file_key)))

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
        expected_result = {"buy_in": 5.0}
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
             'winners', "buy_in"
             }
        )

class TestProblematicFiles(unittest.TestCase):
    def setUp(self):
        self.parser = LocalHandHistoryParser(data_dir=TEST_DATA_DIR)
        self.file_name = "539281767337558454-52-1438951219.txt"
        self.file_key = os.path.join(self.parser.split_dir, "2015", "08", "07", "125561321", self.file_name)

    def test_parse_showdown(self):
        hand_text = self.parser.get_text(self.file_key)
        showdown_info = self.parser.extract_showdown(hand_text)
        self.assertIsInstance(showdown_info, dict)
        self.assertEqual(showdown_info, {
            "jackland": {
                "first_card": "As",
                "second_card": "Jd",
            }
        })
