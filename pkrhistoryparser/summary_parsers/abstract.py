import re
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from json import dumps
from pkrhistoryparser.patterns import winamax as patterns


class AbstractSummaryParser(ABC):

    @abstractmethod
    def list_summary_keys(self) -> list:
        pass

    @abstractmethod
    def get_text(self, file_key: str) -> str:
        pass

    @staticmethod
    def get_parsed_key(summary_key: str) -> str:
        destination_key = summary_key.replace("raw", "parsed").replace(".txt", ".json")
        return destination_key

    @staticmethod
    def to_float(txt_num: str) -> float:
        """
        Transforms any written str number into a float

        Parameters:
            txt_num(str): The number to transform

        Returns:
            (float): The float number

        """
        try:
            return float(txt_num.replace(",", ".").replace("k", "e3").replace("M", "e6"))
        except (TypeError, AttributeError, ValueError):
            return 0.0

    def extract_prize_pool(self, summary_text: str) -> dict:
        """
        Extract the prize pool information from a poker summary.

        Parameters:
            summary_text (str): The raw poker hand text as a string.

        Returns:
            prize_pool (dict): A dictionary containing the prize pool extracted from the poker hand history(prize_pool).
        """
        prize_pool = re.findall(pattern=patterns.PRIZE_POOL_PATTERN, string=summary_text)[-1]
        return {"prize_pool": self.to_float(prize_pool)}

    @staticmethod
    def extract_registered_players(summary_text: str) -> dict:
        """
        Extract the registered players information from a poker summary.

        Parameters:
            summary_text (str): The raw poker hand text as a string.

        Returns:
            registered_players (dict): A dictionary containing the registered players extracted from the poker hand
            history(registered_players).
        """
        registered_players = re.findall(pattern=patterns.REGISTERED_PLAYERS_PATTERN, string=summary_text)[-1]
        return {"registered_players": int(registered_players)}

    @staticmethod
    def extract_speed(summary_text: str) -> dict:
        """
        Extract the speed information from a poker summary.

        Parameters:
            summary_text (str): The raw poker hand text as a string.

        Returns:
            speed (dict): A dictionary containing the speed extracted from the poker hand history(speed).
        """
        try:
            speed = re.findall(pattern=patterns.SPEED_PATTERN, string=summary_text)[-1]
            return {"speed": speed}
        except IndexError:
            return {"speed": "normal"}

    @staticmethod
    def extract_start_date(summary_text: str) -> dict:
        """
        Extract the start date information from a poker summary.

        Parameters:
            summary_text (str): The raw poker hand text as a string.

        Returns:
            start_date (dict): A dictionary containing the start date extracted from the poker hand history(start_date).
        """
        start_date = re.findall(pattern=patterns.START_DATE_PATTERN, string=summary_text)[-1]
        return {"start_date": start_date}

    def extract_levels_structure(self, summary_text: str) -> dict:
        """
        Extract the levels structure information from a poker summary.

        Parameters:
            summary_text (str): The raw poker hand text as a string.

        Returns:
            levels_structure (dict): A dictionary containing the levels structure extracted from the poker hand history
            (levels_structure).
        """
        levels_text = re.findall(pattern=patterns.LEVELS_STRUCTURE_PATTERN, string=summary_text)[-1][0]
        levels = re.findall(patterns.LEVEL_BLINDS_PATTERN, levels_text)
        levels_structure = [
            self.extract_level_from_structure(level_tuple=level_tuple, level_value=level_value)
            for level_value, level_tuple in enumerate(levels, start=1)
        ]
        return {"levels_structure": levels_structure}

    def extract_level_from_structure(self, level_tuple: tuple, level_value: int) -> dict:

        return {
            "value": level_value,
            "sb": self.to_float(level_tuple[0]),
            "bb": self.to_float(level_tuple[1]),
            "ante": self.to_float(level_tuple[2])
        }

    @staticmethod
    def extract_tournament_type(summary_text: str) -> dict:
        """
        Extract the tournament type information from a poker summary.

        Parameters:
            summary_text (str): The raw poker hand text as a string.

        Returns:
            tournament_type (dict): A dictionary containing the tournament type extracted from the poker hand
            history(tournament_type).
        """
        tournament_type = re.findall(pattern=patterns.TOURNAMENT_TYPE_PATTERN, string=summary_text)[-1]
        return {"tournament_type": tournament_type}

    @staticmethod
    def extract_tournament_id(summary_text: str) -> dict:
        """
        Extract the tournament id information from a poker summary.

        Parameters:
            summary_text (str): The raw poker hand text as a string.

        Returns:
            tournament_id (dict): A dictionary containing the tournament id extracted from the poker hand
            history(tournament_id).
        """
        try:
            match = re.search(pattern=patterns.SUMMARY_TOURNAMENT_INFO_PATTERN, string=summary_text)
            tournament_id = match.group(2)
            return {"tournament_id": tournament_id}
        except AttributeError:
            print(summary_text)
            raise AttributeError

    @staticmethod
    def extract_tournament_name(summary_text: str) -> dict:
        """
        Extract the tournament name information from a poker summary.

        Parameters:
            summary_text (str): The raw poker hand text as a string.

        Returns:
            tournament_name (dict): A dictionary containing the tournament name extracted from the poker hand
            history(tournament_name).
        """
        match = re.search(pattern=patterns.SUMMARY_TOURNAMENT_INFO_PATTERN, string=summary_text)
        tournament_name = match.group(1)
        return {"tournament_name": tournament_name}

    def extract_buy_in(self, summary_text: str) -> dict:
        """
        Extract the buy-in and rake information.

        Parameters:
            summary_text (str): The raw poker hand text as a string.

        Returns:
            buy_in (dict): A dict containing the buy-in and rake extracted
            from the poker hand history(prize_pool_contribution, bounty, rake).

        """
        try:

            match = re.search(pattern=patterns.BUY_IN_PATTERN, string=summary_text)
            prize_pool_contribution = self.to_float(match.group(1))
            bounty = self.to_float(match.group(2))
            rake = self.to_float(match.group(3))
            return {"prize_pool_contribution": prize_pool_contribution, "bounty": bounty, "rake": rake}
        except AttributeError:
            print(summary_text)
            raise AttributeError

    def extract_final_position(self, summary_text: str) -> dict:
        """
        Extract the final position of the player.

        Parameters:
            summary_text (str): The raw poker hand text as a string.

        Returns:
            final_position (dict): A dict containing the final position of the player.
        """
        match = re.findall(pattern=patterns.FINAL_POSITION_PATTERN, string=summary_text)
        final_position = int(match[-1]) if match else 0
        return {"final_position": final_position}

    def extract_amount_won(self, summary_text: str) -> dict:
        """
        Extract the amount won by the player.

        Parameters:
            summary_text (str): The raw poker hand text as a string.

        Returns:
            amount_won (dict): A dict containing the amount won by the player.
        """
        match = re.search(pattern=patterns.AMOUNT_WON_PATTERN, string=summary_text)
        amount_won = self.to_float(match.group(1)) if match else 0.0
        return {"amount_won": amount_won}

    def extract_nb_entries(self, summary_text: str) -> dict:
        """
        Extract the number of entries in the tournament

        Parameters:
            summary_text (str): The raw poker hand text as a string.

        Returns:
            nb_entries (dict): A dict containing the number of entries in the tournament.
        """
        split_histories = re.split(patterns.SPLIT_PATTERN, summary_text)
        split_histories.pop(0)
        return {"nb_entries": len(split_histories)}

    def parse_tournament_summary(self, summary_text: str) -> dict:
        """
        Get all the information from a poker summary.
        Args:
            summary_text (str): The raw text of the summary
        Returns:
            summary_info (dict): A dictionary containing all the information extracted from the poker
        """
        summary_info = {
            "tournament_id": self.extract_tournament_id(summary_text)["tournament_id"],
            "tournament_name": self.extract_tournament_name(summary_text)["tournament_name"],
            "speed": self.extract_speed(summary_text)["speed"],
            "buy_in": self.extract_buy_in(summary_text),
            "nb_entries": self.extract_nb_entries(summary_text)["nb_entries"],
            "prize_pool": self.extract_prize_pool(summary_text)["prize_pool"],
            "registered_players": self.extract_registered_players(summary_text)["registered_players"],
            "start_date": self.extract_start_date(summary_text)["start_date"],
            "levels_structure": self.extract_levels_structure(summary_text)["levels_structure"],
            "tournament_type": self.extract_tournament_type(summary_text)["tournament_type"],
            "amount_won": self.extract_amount_won(summary_text)["amount_won"],
            "final_position": self.extract_final_position(summary_text)["final_position"],

        }
        return summary_info



    @abstractmethod
    def check_is_parsed(self, summary_key: str) -> bool:
        pass

    def parse_to_json(self, summary_key: str) -> str:
        """
        Parse a summary to a json string
        Args:
            summary_key:  The key of the summary to parse

        Returns:
            json_summary: The json string of the parsed summary
        """
        print(summary_key)
        summary_text = self.get_text(summary_key)
        summary_info = self.parse_tournament_summary(summary_text)
        json_summary = dumps(summary_info, indent=4, sort_keys=True, ensure_ascii=False)
        return json_summary

    @abstractmethod
    def save_parsed_summary(self, summary_key: str, json_summary: str) -> None:
        pass

    def parse_summary(self, summary_key: str) -> None:
        """
        Parse a summary to a JSON string
        Args:
            summary_key: The key of the summary to parse
        """
        print(f"\n Parsing summary: {summary_key} to {self.get_parsed_key(summary_key)}")
        json_summary = self.parse_to_json(summary_key)
        self.save_parsed_summary(summary_key, json_summary)

    def parse_new_summary(self, summary_key: str) -> None:
        """
        Parse a summary to a JSON string if it has not already been parsed
        Args:
            summary_key: The key of the summary to parse
        """
        if not self.check_is_parsed(summary_key):
            self.parse_summary(summary_key)

    def parse_summaries(self) -> None:
        """
        Parse all the summaries in the raw directory
        """
        summary_keys = self.list_summary_keys()[::-1]
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.parse_summary, summary_key) for summary_key in summary_keys]
            for future in as_completed(futures):
                future.result()
        print(f"Finished parsing summaries at {datetime.now()}")

    def parse_new_summaries(self) -> None:
        """
        Parse all the summaries in the raw directory if they have not already been parsed
        """
        summary_keys = self.list_summary_keys()[::-1]
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.parse_new_summary, summary_key) for summary_key in summary_keys]
            for future in as_completed(futures):
                future.result()
        print(f"Finished parsing summaries at {datetime.now()}")



