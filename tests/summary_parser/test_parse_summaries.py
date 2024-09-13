import unittest
import os

from pkrhistoryparser.summary_parsers.local import LocalSummaryParser
from pkrhistoryparser.settings import TEST_DATA_DIR

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
             'start_date', 'levels_structure', 'nb_entries', 'tournament_type', 'amount_won', 'final_position'}
        )


