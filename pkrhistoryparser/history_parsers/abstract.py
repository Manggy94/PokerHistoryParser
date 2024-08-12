import re
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from json import dumps
from pkrhistoryparser.patterns import winamax as patterns


class AbstractHandHistoryParser(ABC):

    @abstractmethod
    def list_split_histories_keys(self) -> list:
        pass

    @abstractmethod
    def get_text(self, file_key: str) -> str:
        pass

    @staticmethod
    def get_parsed_key(split_key: str) -> str:
        destination_key = split_key.replace("split", "parsed").replace(".txt", ".json")
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

    @staticmethod
    def extract_game_type(hand_txt: str) -> dict:
        """
        Extract the type of the game (Tournament or CashGame).

        Parameters:
            hand_txt (str): The raw poker hand text as a string.

        Returns:
            game_type (dict): A dictionary containing the game type extracted from the poker hand history(game_type).
        """
        game_types = {"Tournament": "Tournament", "CashGame": "CashGame"}
        game_type = next((game_types[key] for key in game_types if key in hand_txt), "Unknown")
        return {"game_type": game_type}

    def extract_buy_in(self, hand_txt: str) -> dict:
        """
        Extract the buy-in and rake information.
        Parameters:
            hand_txt (str): The raw poker hand text as a string.
        Returns:
            buy_in (dict): A dict containing the buy-in and rake extracted
            from the poker hand history(prize_pool_contribution, bounty, rake).

        """
        buy_in_match = re.search(pattern=patterns.NORMAL_BUY_IN_PATTERN, string=hand_txt)
        free_roll_match = re.search(pattern=patterns.FREE_ROLL_PATTERN, string=hand_txt)
        if buy_in_match:
            prize_pool_contribution, rake = self.to_float(buy_in_match.group(1)), self.to_float(buy_in_match.group(2))
            bounty = 0
        elif free_roll_match:
            prize_pool_contribution, bounty, rake = 0, 0, 0
        else:
            prize_pool_contribution, bounty, rake = 0, 0, 0
        return {"buy_in": prize_pool_contribution + bounty + rake}

    def extract_players(self, hand_txt: str) -> dict:
        """
        Extract player information from a raw poker hand history and return as a dictionary.

        Parameters:
            hand_txt (str): The raw poker hand history as a string.

        Returns:
            players_info (dict): A dictionary containing player information(seat, name, init_stack, bounty).

        """
        matches = re.findall(pattern=patterns.PLAYER_PATTERN, string=hand_txt)
        players_info = {int(seat): {
            "seat": int(seat),
            "name": name,
            "init_stack": self.to_float(init_stack),
            "bounty": self.to_float(bounty) if bounty else 0.0
        } for seat, name, init_stack, bounty in matches}
        return players_info

    def extract_posting(self, hand_txt: str) -> list:
        """
        Extract blinds and antes posted information from a  poker hand history and return as a dictionary.

        Parameters:
            hand_txt (str): The raw poker hand history as a string.

        Returns:
            blinds_antes_info (list): A list of dictionaries containing blinds and antes information(name, amount,
            blind_type).

        """
        matches = re.findall(pattern=patterns.BLINDS_PATTERN, string=hand_txt)
        blinds_antes_info = [{"name": name.strip(), "amount": self.to_float(amount), "blind_type": blind_type} for
                             name, blind_type, amount in matches]

        return blinds_antes_info



    @staticmethod
    def extract_datetime(hand_txt: str) -> dict:
        """
        Extract the datetime information.

        Parameters:
            hand_txt (str): The raw poker hand text as a string.

        Returns:
            datetime (str): A dictionary containing the datetime extracted from the poker hand history (datetime) in
            str format.
        """
        datetime_match = re.search(pattern=patterns.DATETIME_PATTERN, string=hand_txt)
        dt = datetime.strptime(datetime_match.group(1), "%Y/%m/%d %H:%M:%S")
        dt_str = dt.strftime("%d-%m-%Y %H:%M:%S")
        return {"datetime": dt_str}

    def extract_blinds(self, hand_txt: str) -> dict:
        """
        Extract the blind levels and ante.

        Parameters:
            hand_txt (str): The raw poker hand text as a string.

        Returns:
            blinds (dict): A dictionary containing the blind levels and ante extracted from the poker hand history
            (ante, sb, bb).
        """
        tour_blinds_match = re.search(pattern=patterns.TOURNAMENT_BLINDS_PATTERN, string=hand_txt)
        other_blinds_match = re.search(pattern=patterns.OTHER_BLINDS_PATTERN, string=hand_txt)
        if tour_blinds_match:
            ante, sb, bb = tour_blinds_match.group(1), tour_blinds_match.group(2), tour_blinds_match.group(3)
        elif other_blinds_match:
            sb, bb = (other_blinds_match.group(1).replace("€", ""),
                      other_blinds_match.group(2).replace("€", ""))
            ante = 0
        else:
            ante, sb, bb = None, None, None
        return {"ante": self.to_float(ante), "sb": self.to_float(sb), "bb": self.to_float(bb)}

    @staticmethod
    def extract_level(hand_txt: str) -> dict:
        """
        Extract the level information.

        Parameters:
            hand_txt (str): The raw poker hand text as a string.

        Returns:
            level (dict): A dictionary containing the level extracted from the poker hand history (level).
        """
        level_match = re.search(pattern=patterns.LEVEL_PATTERN, string=hand_txt)
        return {"level": int(level_match.group(1)) if level_match else 0}

    @staticmethod
    def extract_max_players(hand_txt: str) -> dict:
        """
        Extract the max players at the table.

        Parameters:
            hand_txt (str): The raw poker hand text as a string.

        Returns:
            max_players (dict): A dictionary containing the max players extracted from the poker hand history
            (max_players).
        """
        max_players = re.search(pattern=patterns.MAX_PLAYERS_PATTERN, string=hand_txt).group(1)
        return {"max_players": int(max_players)}

    @staticmethod
    def extract_button_seat(hand_txt: str) -> dict:
        """
        Extract the button seat information.

        Parameters:
            hand_txt (str): The raw poker hand text as a string.

        Returns:
            button_seat (dict): A dictionary containing the button seat extracted from the poker hand history (button).
        """
        button = re.search(pattern=patterns.BUTTON_SEAT_PATTERN, string=hand_txt).group(1)
        return {"button": int(button)}

    @staticmethod
    def extract_tournament_info(hand_txt: str) -> dict:
        """
        Extract the tournament information from a poker hand history.

        Parameters:
            hand_txt (str): The raw poker hand text as a string.

        Returns:
            tournament_info (dict): A dictionary containing the tournament information extracted from the poker hand
            history (tournament_name, tournament_id, table_ident).
        """
        tournament_info = re.search(pattern=patterns.TOURNAMENT_INFO_PATTERN, string=hand_txt)
        tournament_name = tournament_info.group(1) if tournament_info else None
        tournament_id = tournament_info.group(2) if tournament_info else None
        table_number = tournament_info.group(3) if tournament_info else None

        return {"tournament_name": tournament_name, "tournament_id": tournament_id, "table_number": table_number}

    @staticmethod
    def extract_hero_hand(hand_txt: str) -> dict:
        """
        Extract the hero's hand (hole cards) from a single poker hand text and return as a string.

        Parameters:
            hand_txt (str): The raw poker hand text as a string.

        Returns:
            hero_info (dict): A dictionary containing the hero's hand extracted from the poker hand history
            (hero, first_card, second_card).
        """
        try:
            hero, card1, card2 = re.search(
                pattern=patterns.HERO_HAND_PATTERN, string=hand_txt, flags=re.UNICODE).groups()
            return {"hero": hero, "first_card": card1, "second_card": card2}
        except AttributeError:
            return {"hero": "manggy94", "first_card": None, "second_card": None}

    @staticmethod
    def extract_flop(hand_txt: str) -> dict:
        """
        Extract the cards on the Flop from a single poker hand text and return as a string.

        Parameters:
            hand_txt (str): The raw poker hand text as a string.

        Returns:
            flop_cards (dict): A dictionary representing the cards on the Flop (flop_card_1, flop_card_2, flop_card_3).
        """
        flop_match = re.search(pattern=patterns.FLOP_PATTERN, string=hand_txt, flags=re.UNICODE)
        card1, card2, card3 = flop_match.groups() if flop_match else (None, None, None)
        return {"flop_card_1": card1, "flop_card_2": card2, "flop_card_3": card3}

    @staticmethod
    def extract_turn(hand_txt: str) -> dict:
        """
        Extract the card on the Turn from a single poker hand text and return as a string.

        Parameters:
            hand_txt (str): The raw poker hand text as a string.

        Returns:
            turn_card (dict): A dictionary representing the card on the Turn (turn_card).
        """
        turn_match = re.search(pattern=patterns.TURN_PATTERN, string=hand_txt, flags=re.UNICODE)
        card = turn_match.group(1) if turn_match else None
        return {"turn_card": card}

    @staticmethod
    def extract_river(hand_txt: str) -> dict:
        """
        Extract the card on the River from a single poker hand text and return as a string.

        Parameters:
            hand_txt (str): The raw poker hand text as a string.

        Returns:
            river_card (dict): A dictionary representing the card on the River (river_card).
        """
        river_match = re.search(pattern=patterns.RIVER_PATTERN, string=hand_txt, flags=re.UNICODE)
        card = river_match.group(1) if river_match else None
        return {"river_card": card}

    def parse_actions(self, actions_txt: str) -> list:
        """
        Parse the actions text from a poker hand history for a specific street
        and return a list of dictionaries containing the actions.

        Parameters:
            actions_txt (str): The raw actions text for a specific street.

        Returns:
            parsed_actions (list): A list of dictionaries (player, action, amount), each representing an action.
        """
        actions = re.findall(pattern=patterns.ACTION_PATTERN, string=actions_txt)
        parsed_actions = [{'player': player.strip(), 'action': action_type, 'amount': self.to_float(amount)}
                          for player, action_type, amount in actions]
        return parsed_actions

    def extract_actions(self, hand_txt: str) -> dict:
        """
        Extract the actions information from a poker hand history and return as a nested dictionary.

        Parameters:
            hand_txt (str): The raw poker hand text as a string.

        Returns:
            actions_dict (dict): A dictionary containing all the actions extracted for each street
            of the poker hand history (preflop, flop, turn, river).
        """
        actions_dict = {
            street: self.parse_actions(re.search(pattern, string=hand_txt, flags=re.DOTALL).group(1))
            if re.search(pattern, string=hand_txt, flags=re.DOTALL) else []
            for pattern, street in zip(patterns.STREET_ACTION_PATTERNS, ['preflop', 'flop', 'turn', 'river'])}
        return actions_dict

    @staticmethod
    def extract_showdown(hand_txt: str) -> dict:
        """
        Extract the showdown information from a poker hand history.

        Parameters:
            hand_txt (str): The raw poker hand text as a string.

        Returns:
            showdown_info (dict): A dict containing the showdown information extracted
            from the poker hand history(first_card, second_card).
        """
        showdown_info = {player.strip(): {"first_card": card1, "second_card": card2}
                         for player, card1, card2 in re.findall(pattern=patterns.SHOWDOWN_PATTERN, string=hand_txt)}
        return showdown_info

    def extract_winners(self, hand_txt: str) -> dict:
        """
        Extract the winners information from a poker hand history and return it as a nested dictionary.

        Parameters:
            hand_txt (str): The raw poker hand text as a string.

        Returns:
            winners_info (dict): A dictionary containing the winners information extracted
            from the poker hand history(winner_name(amount, pot_type)).
        """
        winners_info = {winner: {"amount": self.to_float(amount), "pot_type": pot_type}
                        for winner, amount, pot_type in re.findall(pattern=patterns.WINNERS_PATTERN, string=hand_txt)}
        return winners_info

    @staticmethod
    def extract_hand_id(hand_txt: str) -> dict:
        """
        Extract the hand id information from a poker hand history.

        Parameters:
            hand_txt (str): The raw poker hand text as a string.

        Returns:
            hand_id (dict): A dictionary containing the hand id extracted from the poker hand history(hand_id).
        """
        hand_id = re.search(pattern=patterns.HAND_ID_PATTERN, string=hand_txt).group(1)
        return {"hand_id": hand_id}



    @staticmethod
    def check_players(hand_history_dict: dict) -> None:
        """
        Check if the players in the hand history are the same as the players in the summary.
        Args:
            hand_history_dict (dict): The hand history dictionary
        """
        players = hand_history_dict["players"]
        preflop_actions = hand_history_dict["actions"]["preflop"]
        preflop_players = set([action["player"] for action in preflop_actions])
        posting_players = set([posting["name"] for posting in hand_history_dict["postings"]])
        verified_players = preflop_players | posting_players
        for player in players.values():
            player["entered_hand"] = player["name"] in verified_players

    def parse_hand(self, hand_txt: str) -> dict:
        """
        Extract all information from a poker hand history and return as a dictionary.

        Parameters:
            hand_txt (str): The raw poker hand text as a string.

        Returns:
            hand_history_dict (dict): A dictionary containing all the information extracted from the poker hand history
        (hand_id, datetime, game_type, buy_in, blinds, level, max_players, button_seat, table_name, table_ident,
        players, hero_hand, postings, actions, flop, turn, river, showdown, winners).
        """
        hand_history_dict = {
            "tournament_info": self.extract_tournament_info(hand_txt),
            "buy_in": self.extract_buy_in(hand_txt)["buy_in"],
            "hand_id": self.extract_hand_id(hand_txt)["hand_id"],
            "datetime": self.extract_datetime(hand_txt)["datetime"],
            "game_type": self.extract_game_type(hand_txt)["game_type"],
            "level": {
                "value": self.extract_level(hand_txt)["level"],
                "ante": self.extract_blinds(hand_txt)["ante"],
                "sb": self.extract_blinds(hand_txt)["sb"],
                "bb": self.extract_blinds(hand_txt)["bb"]
            },
            "max_players": self.extract_max_players(hand_txt)["max_players"],
            "button_seat": self.extract_button_seat(hand_txt)["button"],
            "players": self.extract_players(hand_txt),
            "hero_hand": self.extract_hero_hand(hand_txt),
            "postings": self.extract_posting(hand_txt),
            "actions": self.extract_actions(hand_txt),
            "flop": self.extract_flop(hand_txt),
            "turn": self.extract_turn(hand_txt),
            "river": self.extract_river(hand_txt),
            "showdown": self.extract_showdown(hand_txt),
            "winners": self.extract_winners(hand_txt),

        }
        self.check_players(hand_history_dict)
        return hand_history_dict

    @abstractmethod
    def check_is_parsed(self, split_key: str) -> bool:
        pass

    def parse_to_json(self, split_key: str) -> str:
        """
        Parse a poker hand history to a JSON format.

        Parameters:
            split_key (str): The path to the poker hand history file.
        """
        hand_text = self.get_text(split_key)
        hand_info = self.parse_hand(hand_text)
        json_hand = dumps(hand_info, indent=4, ensure_ascii=False)
        return json_hand

    @abstractmethod
    def save_parsed_hand(self, split_key: str, json_hand: str) -> None:
        pass

    def parse_hand_history(self, split_key: str) -> None:
        """
        Parse a poker hand history and save it in JSON format.

        Parameters:
            split_key (str): The path to the poker hand history file.
        """
        print(f"\nParsing {split_key} to {self.get_parsed_key(split_key)}")
        json_hand = self.parse_to_json(split_key)
        self.save_parsed_hand(split_key, json_hand)

    def parse_new_hand_history(self, split_key: str) -> None:
        """
        Parse a new poker hand history and save it in JSON format if it has not been parsed yet.

        Parameters:
            split_key (str): The path to the poker hand history file.
        """
        if not self.check_is_parsed(split_key):
            self.parse_hand_history(split_key)
        else:
            print(f"\n{split_key} is already parsed")

    def parse_hand_histories(self) -> None:
        """
        Parse all poker hand histories and save them in JSON format.
        """
        split_keys = self.list_split_histories_keys()[::-1]
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.parse_hand_history, split_key) for split_key in split_keys]
            for future in as_completed(futures):
                future.result()

    def parse_new_hand_histories(self) -> None:
        """
        Parse new poker hand histories and save them in JSON format if they have not been parsed yet.
        """
        split_keys = self.list_split_histories_keys()[::-1]
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.parse_new_hand_history, split_key) for split_key in split_keys]
            for future in as_completed(futures):
                future.result()
