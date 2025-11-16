import re
from typing import Callable, Generator


def generator_numbers(text: str) -> Generator[float, None, None]:
    pattern = r'(?<=\s)\d+(?:\.\d+)?(?=\s)'
    for match in re.findall(pattern, text):
        yield float(match)

def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]) -> float:
    return sum(func(text))


if __name__ == "__main__":
    text = """Загальний дохід працівника складається з декількох частин:
    1000.01 як основний дохід, доповнений додатковими надходженнями 
    27.45 і 324.00 доларів."""
    

    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income:.2f}")

    text = """Загальний дохід працівника складається з декількох частин:
    1000.01 як основний дохід, доповнений додатковими надходженнями 
    27.45і 324.00 доларів."""
    
    print(f"Загальний дохід: {sum_profit(text, generator_numbers):.2f} = {1000.01 + 324}")

    text = """Загальний дохід працівника складається з декількох частин:
    -1000.01 як основний дохід, доповнений додатковими надходженнями 
    27.45 і 324.00, доларів."""
    
    print(f"Загальний дохід: {sum_profit(text, generator_numbers):.2f} = {27.45}")
