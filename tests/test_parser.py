import unittest
import os
from datetime import datetime
from pkrhistoryparser.parser import HandHistoryParser

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class TestHandHistoryParser(unittest.TestCase):
    def setUp(self):
        self.parser = HandHistoryParser()
        file_path = os.path.join(TEST_DIR, "example_text.txt")
        self.hand_text = self.parser.get_raw_text(file_path)

    def test_extract_game_type(self):
        result = self.parser.extract_game_type(self.hand_text)
        self.assertEqual(result, {"game_type": "Tournament"})

    def test_extract_players(self):
        result = self.parser.extract_players(self.hand_text)
        expected_result = {
            1: {"seat": 1, "pseudo": "FrenchAAAA", "stack": 19575.0, "bounty": 2.25},
            2: {"seat": 2, "pseudo": "daifwa", "stack": 21830.0, "bounty": 2.25},
            3: {"seat": 3, "pseudo": "Roomxx", "stack": 34263.0, "bounty": 3.37},
            4: {"seat": 4, "pseudo": "SB Warrior34", "stack": 18548.0, "bounty": 2.25},
            5: {"seat": 5, "pseudo": "GoToVG", "stack": 26609.0, "bounty": 2.25},
            6: {"seat": 6, "pseudo": "manggy94", "stack": 19175.0, "bounty": 2.25}
        }
        self.assertEqual(result, expected_result)

    def test_extract_posting(self):
        result = self.parser.extract_posting(self.hand_text)
        expected_result = [
            {"pseudo": "GoToVG", "amount": 25.0, "blind_type": "ante"},
            {"pseudo": "manggy94", "amount": 25.0, "blind_type": "ante"},
            {"pseudo": "FrenchAAAA", "amount": 25.0, "blind_type": "ante"},
            {"pseudo": "daifwa", "amount": 25.0, "blind_type": "ante"},
            {"pseudo": "Roomxx", "amount": 25.0, "blind_type": "ante"},
            {"pseudo": "SB Warrior34", "amount": 25.0, "blind_type": "ante"},
            {"pseudo": "GoToVG", "amount": 100.0, "blind_type": "small blind"},
            {"pseudo": "manggy94", "amount": 200.0, "blind_type": "big blind"}
        ]
        self.assertEqual(result, expected_result)

    def test_extract_buy_in(self):
        result = self.parser.extract_buy_in(self.hand_text)
        expected_result = {"prize_pool_contribution": 4.5, "bounty": 0.0, "rake": 0.5}
        self.assertEqual(result, expected_result)

    def test_extract_datetime(self):
        result = self.parser.extract_datetime(self.hand_text)
        expected_result = {"datetime": datetime(2023, 1, 4, 17, 36, 27)}
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

    def test_extract_table_name(self):
        result = self.parser.extract_table_name(self.hand_text)
        expected_result = {"table_name": "GUERILLA(608341002)#016"}
        self.assertEqual(result, expected_result)

    def test_extract_table_ident(self):
        result = self.parser.extract_table_ident(self.hand_text)
        expected_result = {"table_ident": "(608341002)#016"}
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


class TestHandHistoryParser2(unittest.TestCase):
    def setUp(self):
        self.parser = HandHistoryParser()
        file_path = os.path.join(TEST_DIR, "example_text2.txt")
        self.hand_text = self.parser.get_raw_text(file_path)

    def test_extract_hand_id(self):
        result = self.parser.extract_hand_id(self.hand_text)
        self.assertEqual(result, {"hand_id": "662028569697845253-8-1460574182"})

    def test_extract_datetime(self):
        result = self.parser.extract_datetime(self.hand_text)
        self.assertEqual(result, {"datetime": datetime(2016, 4, 13, 19, 3, 2)})

    def test_game_type_extraction_returns_correct_game_type(self):
        result = self.parser.extract_game_type(self.hand_text)
        self.assertEqual(result, {"game_type": "Tournament"})

    def test_buy_in_extraction_returns_correct_buy_in_info(self):
        result = self.parser.extract_buy_in(self.hand_text)
        self.assertEqual(result, {"prize_pool_contribution": 4.5, "bounty": 0.0, "rake": 0.5})

    def test_blinds_extraction_returns_correct_blinds_info(self):
        result = self.parser.extract_blinds(self.hand_text)
        self.assertEqual(result, {"ante": 0.0, "sb": 15.0, "bb": 30.0})

    def test_level_extraction_returns_correct_level(self):
        result = self.parser.extract_level(self.hand_text)
        self.assertEqual(result, {"level": 0})

    def test_max_players_extraction_returns_correct_max_players(self):
        result = self.parser.extract_max_players(self.hand_text)
        self.assertEqual(result, {"max_players": 3})

    def test_button_seat_extraction_returns_correct_button_seat(self):
        result = self.parser.extract_button_seat(self.hand_text)
        self.assertEqual(result, {"button": 1})

    def test_table_name_extraction_returns_correct_table_name(self):
        result = self.parser.extract_table_name(self.hand_text)
        self.assertEqual(result, {"table_name": "Déglingos(154140538)#004"})

    def test_table_ident_extraction_returns_correct_table_ident(self):
        result = self.parser.extract_table_ident(self.hand_text)
        self.assertEqual(result, {"table_ident": "(154140538)#004"})

    def test_hero_hand_extraction_returns_correct_hero_hand(self):
        result = self.parser.extract_hero_hand(self.hand_text)
        self.assertEqual(result, {"hero": "manggy94", "first_card": "Th", "second_card": "6d"})

    def test_flop_extraction_returns_correct_flop_cards(self):
        result = self.parser.extract_flop(self.hand_text)
        self.assertEqual(result, {"flop_card_1": None, "flop_card_2": None, "flop_card_3": None})

    def test_turn_extraction_returns_correct_turn_card(self):
        result = self.parser.extract_turn(self.hand_text)
        self.assertEqual(result, {"turn_card": None})

    def test_river_extraction_returns_correct_river_card(self):
        result = self.parser.extract_river(self.hand_text)
        self.assertEqual(result, {"river_card": None})

    def test_showdown_extraction_returns_correct_showdown_info(self):
        result = self.parser.extract_showdown(self.hand_text)
        self.assertEqual(result, {})

    def test_winners_extraction_returns_correct_winners_info(self):
        result = self.parser.extract_winners(self.hand_text)
        self.assertEqual(result, {"jaleo88": {"amount": 165.0, "pot_type": "pot"}})

    def test_extract_actions(self):
        result = self.parser.extract_actions(self.hand_text)
        expected_result = {
            'preflop': [
                {'player': 'jaleo88', 'action': 'raises', 'amount': 90.0},
                {'player': 'Art&mus', 'action': 'folds', 'amount': 0.0},
                {'player': 'manggy94', 'action': 'folds', 'amount': 0.0}
            ],
            'flop': [],
            'turn': [],
            'river': []
        }
        self.assertEqual(result, expected_result)

