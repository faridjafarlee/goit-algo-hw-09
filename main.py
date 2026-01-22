from time import perf_counter
from typing import Dict, List, Optional


COINS: List[int] = [50, 25, 10, 5, 2, 1]


def find_coins_greedy(amount: int, coins: List[int] = COINS) -> Dict[int, int]:
    if amount < 0:
        raise ValueError("amount must be >= 0")

    result: Dict[int, int] = {}
    remaining = amount

    for c in sorted(coins, reverse=True):
        if remaining == 0:
            break
        cnt = remaining // c
        if cnt:
            result[c] = cnt
            remaining -= c * cnt

    return result


def find_min_coins(amount: int, coins: List[int] = COINS) -> Dict[int, int]:
    if amount < 0:
        raise ValueError("amount must be >= 0")
    if amount == 0:
        return {}

    coins = sorted(coins)

    dp: List[Optional[int]] = [None] * (amount + 1)
    prev: List[int] = [-1] * (amount + 1)

    dp[0] = 0

    for s in range(1, amount + 1):
        best_count: Optional[int] = None
        best_coin = -1

        for c in coins:
            if c > s:
                break

            prev_count = dp[s - c]
            if prev_count is None:
                continue

            cand = prev_count + 1
            if best_count is None or cand < best_count:
                best_count = cand
                best_coin = c

        dp[s] = best_count
        prev[s] = best_coin

    if dp[amount] is None:
        raise ValueError("amount cannot be formed with given coin set")

    res: Dict[int, int] = {}
    cur = amount
    while cur > 0:
        c = prev[cur]
        if c == -1:
            raise RuntimeError("DP reconstruction failed")
        res[c] = res.get(c, 0) + 1
        cur -= c

    return dict(sorted(res.items()))


def _bench(fn, amounts: List[int], repeats: int = 2000) -> float:
    start = perf_counter()
    for _ in range(repeats):
        for a in amounts:
            fn(a)
    end = perf_counter()
    calls = repeats * len(amounts)
    return (end - start) / calls


def main() -> None:
    test_amount = 113
    print("Greedy 113:", find_coins_greedy(test_amount))
    print("DP     113:", find_min_coins(test_amount))

    amounts = [10, 113, 999, 10_000, 100_000]
    g = _bench(find_coins_greedy, amounts)
    d = _bench(find_min_coins, amounts, repeats=200)

    print("\nAvg time per call:")
    print(f"Greedy: {g:.10f} sec")
    print(f"DP    : {d:.10f} sec")


if __name__ == "__main__":
    main()
