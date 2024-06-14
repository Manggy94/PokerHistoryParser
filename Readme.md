
# PokerHistoryParser

## Description
A poker package to parse Hand histories into json objects

PokerHistoryParser is a powerful tool for analyzing and extracting data from poker hand histories.  
This project is designed to help poker players and analysts better understand their performance by providing detailed 
analyses of hands played.


## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Contribuer](#contribuer)
- [Licence](#licence)
- [Auteurs](#auteurs)

## Introduction

Welcome to the PokerHistoryParser documentation.  
This tool allows you to analyze poker hand histories.  
It is designed to be easy to use and integrate into your projects.  
It returns data as a dictionary or JSON file for easy use in your programs.


## Installation
To install the package, use the following command:


```sh
pip install pkrhistoryparser
```

## Usage

### Base Examples
Here are some simple examples of using PokerHistoryParser:

Parse a poker hand history to a dict to be used in a program:


```python
from pkrhistoryparser.parser import HandHistoryParser

parser = HandHistoryParser()
hand_text = parser.get_raw_text("path/to/hand/history.txt")
hand_info = parser.parse_hand(hand_text)
   ```

Parse a poker hand history to a JSON file:
```python
from pkrhistoryparser.parser import HandHistoryParser

parser = HandHistoryParser()
parser.parse_to_json('path/to/hand/history.txt', 'path/to/save/json/file.json')
```
For more details on usage, please refer to the [documentation](https://pkrhistoryparser.readthedocs.io/en/latest/).

### Supported Poker Sites
Currently, PokerHistoryParser supports the following poker sites:
- Winamax

### Upcoming Features
Here are some features we plan to add in future versions:
- Analysis of tournament summary files
- Analysis of CashGame files
- Support for more poker sites

## Contributing

All contributions are welcome! To contribute, please follow these steps:

1. Fork the repository
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## License

This project is licensed under the *MIT* license. See the [LICENSE](LICENSE.txt) file for more details.

## Authors

- **Alexandre MANGWA** a.k.a [Manggy94 on GitHub](https://github.com/manggy94) - *Main dev* - 

## Associated Projects
- [PokerComponents](https://github.com/manggy94/PokerComponents)

---

For any questions or issues, feel free to open an issue in the repository or contact us directly.
