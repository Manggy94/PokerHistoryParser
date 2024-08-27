import os
import re
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
MEMORY_RESULTS_PATH = os.path.join(REPORTS_DIR, "parsing_history_memory_results.log")
SPEED_RESULTS_PATH = os.path.join(REPORTS_DIR, "parsing_history_speed_results.csv")
FINANCIAL_COST_PATH = os.path.join(REPORTS_DIR, "parsing_history_financial_cost.csv")


def get_memory_usage(memory_results_path) -> float:
    memory_usage_pattern = r"(\d+\.\d+) MiB"
    with open(memory_results_path, "r") as file:
        content = file.read()
    return max([float(memory) for memory in re.findall(memory_usage_pattern, content)])


def get_memory_to_use(memory_results_path) -> int:
    memory_usage = get_memory_usage(memory_results_path)
    memory_options = [2**n for n in range(7, 14)]
    superior_memory_options = [memo for memo in memory_options if memo >= memory_usage]
    return min(superior_memory_options) if superior_memory_options else 10240


def get_memory_cost(memory_results_path=MEMORY_RESULTS_PATH, speed_results_path=SPEED_RESULTS_PATH):
    ref_price = 0.0000166667
    memory_to_use = get_memory_to_use(memory_results_path)
    speed_df = pd.read_csv(speed_results_path, index_col=0)
    memory_to_use_go = memory_to_use / 1024
    multipliers = speed_df.index.values.reshape(-1, 1)
    memory_cost = speed_df * multipliers * memory_to_use_go
    financial_cost_df = (memory_cost * ref_price).round(4)
    financial_cost_df.to_csv(FINANCIAL_COST_PATH)


if __name__ == "__main__":
    get_memory_cost()

