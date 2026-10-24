from typing import List, Dict, Tuple
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

PENALTY_P = 0.8


def _validate(length: int, prices: List[int]) -> None:
    if length <= 0:
        raise ValueError("Довжина стрижня має бути > 0")
    if not prices:
        raise ValueError("Масив цін не може бути порожнім")
    if len(prices) != length:
        raise ValueError("Довжина масиву цін повинна відповідати довжині стрижня")
    if any(p <= 0 for p in prices):
        raise ValueError("Усі ціни мають бути > 0")


def piece_profit(k: int, prices: List[int]) -> float:
    base = float(prices[k - 1])
    if k == 1:
        return base - PENALTY_P
    return base


def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    _validate(length, prices)

    memo: Dict[int, Tuple[float, int]] = {}

    def solve(n: int) -> Tuple[float, int]:
        if n == 0:
            return 0.0, 0
        if n in memo:
            return memo[n]

        best_profit = float("-inf")
        best_first = 1

        for k in range(1, n + 1):
            profit_rest, _ = solve(n - k)
            total = piece_profit(k, prices) + profit_rest
            if total > best_profit:
                best_profit = total
                best_first = k

        memo[n] = (best_profit, best_first)
        return memo[n]

    max_profit, _ = solve(length)

    cuts: List[int] = []
    remaining = length
    while remaining > 0:
        _, first = memo[remaining]
        cuts.append(first)
        remaining -= first

    return {
        "max_profit": max_profit,
        "cuts": cuts,
        "number_of_cuts": max(0, len(cuts) - 1),
    }


def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    _validate(length, prices)

    dp = [0.0] * (length + 1)
    first_cut = [0] * (length + 1)

    for n in range(1, length + 1):
        best_profit = float("-inf")
        best_k = 1
        for k in range(1, n + 1):
            total = piece_profit(k, prices) + dp[n - k]
            if total > best_profit:
                best_profit = total
                best_k = k
        dp[n] = best_profit
        first_cut[n] = best_k

    cuts: List[int] = []
    remaining = length
    while remaining > 0:
        k = first_cut[remaining]
        cuts.append(k)
        remaining -= k

    return {
        "max_profit": dp[length],
        "cuts": cuts,
        "number_of_cuts": max(0, len(cuts) - 1),
    }


def run_tests():
    test_cases = [
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Базовий випадок (зі штрафом P=0.8 за довжину 1)",
        },
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Оптимально не різати",
        },
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Рівномірні розрізи (без штрафу вигідні 1+1+1+1)",
        },
    ]

    print("=" * 60)
    print("| Завдання 1 | Rod Cutting | Варіант 6")
    print(f"Штраф за частину довжини 1: P = {PENALTY_P}")
    print("=" * 60)

    for test in test_cases:
        print(f"\nТест: {test['name']}")
        print(f"Довжина стрижня: {test['length']}")
        print(f"Ціни: {test['prices']}")

        memo_result = rod_cutting_memo(test["length"], test["prices"])
        print("\nРезультат мемоізації:")
        print(f"Максимальний прибуток: {memo_result['max_profit']}")
        print(f"Розрізи: {memo_result['cuts']}")
        print(f"Кількість розрізів: {memo_result['number_of_cuts']}")

        table_result = rod_cutting_table(test["length"], test["prices"])
        print("\nРезультат табуляції:")
        print(f"Максимальний прибуток: {table_result['max_profit']}")
        print(f"Розрізи: {table_result['cuts']}")
        print(f"Кількість розрізів: {table_result['number_of_cuts']}")

        assert abs(memo_result["max_profit"] - table_result["max_profit"]) < 1e-9
        print("\nПеревірка пройшла успішно!")


if __name__ == "__main__":
    run_tests()
