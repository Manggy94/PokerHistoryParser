import unittest
import os

from pkrhistoryparser.summary_parsers.local import LocalSummaryParser
from pkrhistoryparser.settings import TEST_DATA_DIR

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class Test01(unittest.TestCase):
    def setUp(self):
        self.parser = LocalSummaryParser(data_dir=TEST_DATA_DIR)
        self.file_key = os.path.join(TEST_DIR, "raw_files", "example01.txt")
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

    def test_extract_tournament_prize_pool(self):
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
        expected_result = {"amount_won": 0.0, "bounty_won": 0.0}
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
             'start_date', 'levels_structure', 'nb_entries', 'tournament_type', 'amount_won', 'final_position',
             'bounty_won'}
        )

    def test_nb_entries(self):
        result = self.parser.extract_nb_entries(self.summary_text)
        expected_result = {"nb_entries": 1}
        self.assertEqual(result, expected_result)


class Test02(unittest.TestCase):
    def setUp(self):
        self.parser = LocalSummaryParser(data_dir=TEST_DATA_DIR)
        self.file_key = os.path.join(TEST_DIR, "raw_files", "example02.txt")
        self.summary_text = self.parser.get_text(self.file_key)

    def test_extract_buy_in(self):
        result = self.parser.extract_buy_in(self.summary_text)
        expected_result = {"prize_pool_contribution": 3, "bounty": 1.50, "rake": 0.50}
        self.assertEqual(result, expected_result)

    def test_extract_tournament_id(self):
        result = self.parser.extract_tournament_id(self.summary_text)
        expected_result = {"tournament_id": "827696740"}
        self.assertEqual(result, expected_result)

    def test_extract_tournament_name(self):
        result = self.parser.extract_tournament_name(self.summary_text)
        expected_result = {"tournament_name": "#30 - W SERIES - MYSTERY REBUY"}
        self.assertEqual(result, expected_result)

    def test_extract_tournament_type(self):
        result = self.parser.extract_tournament_type(self.summary_text)
        expected_result = {"tournament_type": "knockout"}
        self.assertEqual(result, expected_result)

    def test_extract_tournament_speed(self):
        result = self.parser.extract_speed(self.summary_text)
        expected_result = {"speed": "semiturbo"}
        self.assertEqual(result, expected_result)

    def test_extract_tournament_prize_pool(self):
        result = self.parser.extract_prize_pool(self.summary_text)
        expected_result = {"prize_pool": 31746}
        self.assertEqual(result, expected_result)

    def test_extract_registered_players(self):
        result = self.parser.extract_registered_players(self.summary_text)
        expected_result = {"registered_players": 4358}
        self.assertEqual(result, expected_result)

    def test_extract_tournament_start_date(self):
        result = self.parser.extract_start_date(self.summary_text)
        expected_result = {"start_date": "2024/09/01 20:00:01 UTC"}
        self.assertEqual(result, expected_result)

    def test_extract_amount_won(self):
        result = self.parser.extract_amount_won(self.summary_text)
        expected_result = {"amount_won": 95.94, "bounty_won": 57.50}
        self.assertEqual(result, expected_result)

    def test_extract_final_position(self):
        result = self.parser.extract_final_position(self.summary_text)
        expected_result = {"final_position": 32}
        self.assertEqual(result, expected_result)

    def test_nb_entries(self):
        result = self.parser.extract_nb_entries(self.summary_text)
        expected_result = {"nb_entries": 1}
        self.assertEqual(result, expected_result)

    def test_parse_tournament_summary(self):
        result = self.parser.parse_tournament_summary(self.summary_text)
        self.assertIsInstance(result, dict)
        self.assertEqual(
            set(result.keys()),
            {'tournament_id', 'tournament_name', 'buy_in', 'prize_pool', 'registered_players', 'speed',
             'start_date', 'levels_structure', 'nb_entries', 'tournament_type', 'amount_won', 'bounty_won', 'final_position'}
        )


class Test03(unittest.TestCase):
    def setUp(self):
        self.parser = LocalSummaryParser(data_dir=TEST_DATA_DIR)
        self.file_key = os.path.join(TEST_DIR, "raw_files", "example03.txt")
        self.summary_text = self.parser.get_text(self.file_key)

    def test_extract_buy_in(self):
        result = self.parser.extract_buy_in(self.summary_text)
        expected_result = {"prize_pool_contribution": 4.5, "bounty": 0, "rake": 0.50}
        self.assertEqual(result, expected_result)

    def test_extract_tournament_id(self):
        result = self.parser.extract_tournament_id(self.summary_text)
        expected_result = {"tournament_id": "492049891"}
        self.assertEqual(result, expected_result)

    def test_extract_tournament_name(self):
        result = self.parser.extract_tournament_name(self.summary_text)
        expected_result = {"tournament_name": "POUR LA DARONNE"}
        self.assertEqual(result, expected_result)

    def test_extract_tournament_type(self):
        result = self.parser.extract_tournament_type(self.summary_text)
        expected_result = {"tournament_type": "knockout"}
        self.assertEqual(result, expected_result)

    def test_extract_tournament_speed(self):
        result = self.parser.extract_speed(self.summary_text)
        expected_result = {"speed": "semiturbo"}
        self.assertEqual(result, expected_result)

    def test_extract_tournament_prize_pool(self):
        result = self.parser.extract_prize_pool(self.summary_text)
        expected_result = {"prize_pool": 10608.75}
        self.assertEqual(result, expected_result)

    def test_extract_registered_players(self):
        result = self.parser.extract_registered_players(self.summary_text)
        expected_result = {"registered_players": 3618}
        self.assertEqual(result, expected_result)

    def test_extract_tournament_start_date(self):
        result = self.parser.extract_start_date(self.summary_text)
        expected_result = {"start_date": "2021/10/17 18:30:07 UTC"}
        self.assertEqual(result, expected_result)

    def test_extract_amount_won(self):
        result = self.parser.extract_amount_won(self.summary_text)
        expected_result = {"amount_won": 1265.03, "bounty_won": 0.0}
        self.assertEqual(result, expected_result)

    def test_extract_final_position(self):
        result = self.parser.extract_final_position(self.summary_text)
        expected_result = {"final_position": 1}
        self.assertEqual(result, expected_result)

    def test_parse_tournament_summary(self):
        result = self.parser.parse_tournament_summary(self.summary_text)
        self.assertIsInstance(result, dict)
        self.assertEqual(
            set(result.keys()),
            {'tournament_id', 'tournament_name', 'buy_in', 'prize_pool', 'registered_players', 'speed',
             'start_date', 'levels_structure', 'nb_entries', 'tournament_type', 'amount_won', 'bounty_won',
             'final_position'}
        )

    def test_nb_entries(self):
        result = self.parser.extract_nb_entries(self.summary_text)
        expected_result = {"nb_entries": 2}
        self.assertEqual(result, expected_result)
