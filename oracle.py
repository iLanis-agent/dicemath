#!/usr/bin/env python3
# Dice Math oracle - mirrors engine.js. Roll counts come from the inclusion-exclusion formula, not the engine's step-by-step table.
import json, re
from fractions import Fraction
from math import comb, floor

DICE_ERR = "dice must be a whole number from 1 to 10"
SIDES_ERR = "sides must be a whole number from 2 to 100"
X_ERR = "the chance must be written as 1 in X, with X a whole number from 2 to 1000"
N_ERR = "tries must be a whole number from 1 to 1000"

def num(t, lo, hi, err):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"-?[0-9]{1,6}", t): raise ValueError(err)
    v = int(t)
    if v < lo or v > hi: raise ValueError(err)
    return v

def pc(a, b):
    f = Fraction(a, b) * 100
    return _two(f)

def _two(f):
    sc = floor(f * 100 + Fraction(1, 2))
    s = str(sc).rjust(3, "0")
    return s[:-2] + "." + s[-2:] + "%"

def dice_word(n): return "1 die" if n == 1 else f"{n} dice"
def tries_word(n): return f"{n} " + ("try" if n == 1 else "tries")

def ways(n, s, t):
    # rolls of n s-sided dice totalling t (inclusion-exclusion)
    return sum((-1) ** k * comb(n, k) * comb(t - k * s - 1, n - 1) for k in range(0, n + 1) if t - k * s - 1 >= n - 1)

def sum_truth(d, sd, tg):
    n = num(d, 1, 10, DICE_ERR); s = num(sd, 2, 100, SIDES_ERR)
    rng = f"target must be a whole number from {n} to {n * s}"
    t = num(tg, -1000000, 1000000, rng)
    if t < n or t > n * s: raise ValueError(rng)
    total = s ** n
    exact = ways(n, s, t)
    atleast = sum(ways(n, s, k) for k in range(t, n * s + 1))
    return (f"Rolling {dice_word(n)} with {s} sides each, a total of exactly {t} comes up in {exact} of {total} equally likely rolls "
            f"({pc(exact, total)}), and a total of {t} or more in {atleast} ({pc(atleast, total)}).")

def edge_truth(sd, tg):
    s = num(sd, 2, 100, SIDES_ERR)
    rng = f"target must be a whole number from 1 to {s}"
    t = num(tg, 1, 100, rng)
    if t > s: raise ValueError(rng)
    p = Fraction(s - t + 1, s)
    adv = 1 - (1 - p) ** 2
    dis = p ** 2
    return (f"On one die with {s} sides, needing {t} or higher succeeds {_two(p * 100)} of the time with a single roll, {_two(adv * 100)} "
            f"with advantage (roll two, keep the higher) and {_two(dis * 100)} with disadvantage (roll two, keep the lower).")

def streak_truth(xx, tries):
    x = num(xx, 2, 1000, X_ERR); n = num(tries, 1, 1000, N_ERR)
    q = Fraction(x - 1, x)
    none = q ** n
    m = 1
    while (x - 1) ** m * 2 > x ** m: m += 1
    return (f"With a 1 in {x} chance on each try, {tries_word(n)} give at least one success {_two((1 - none) * 100)} of the time and none {_two(none * 100)} "
            f"of the time. The first number of tries that reaches 50% is {m} ({_two((1 - q ** m) * 100)}).")

FNS = {"sumTruth": sum_truth, "edgeTruth": edge_truth, "streakTruth": streak_truth}
CASES = [
    ("sumTruth", ["3", "6", "10"]), ("sumTruth", ["2", "6", "7"]), ("sumTruth", ["2", "6", "2"]), ("sumTruth", ["2", "6", "12"]), ("sumTruth", ["1", "6", "4"]),
    ("sumTruth", ["1", "20", "20"]), ("sumTruth", ["1", "2", "1"]), ("sumTruth", ["3", "6", "3"]), ("sumTruth", ["3", "6", "18"]), ("sumTruth", ["4", "6", "14"]),
    ("sumTruth", ["2", "20", "21"]), ("sumTruth", ["5", "10", "27"]), ("sumTruth", ["10", "100", "505"]), ("sumTruth", ["10", "100", "10"]), ("sumTruth", ["10", "100", "1000"]),
    ("sumTruth", ["6", "8", "27"]), ("sumTruth", ["7", "4", "18"]), ("sumTruth", ["10", "2", "5"]), ("sumTruth", ["3", "12", "20"]), ("sumTruth", [" 2 ", " 6 ", " 8 "]),
    ("sumTruth", ["0", "6", "3"]), ("sumTruth", ["11", "6", "30"]), ("sumTruth", ["2", "1", "2"]), ("sumTruth", ["2", "101", "5"]), ("sumTruth", ["2", "6", "1"]),
    ("sumTruth", ["2", "6", "13"]), ("sumTruth", ["2", "6", "x"]), ("sumTruth", ["2", "6", ""]), ("sumTruth", ["1.5", "6", "3"]), ("sumTruth", ["2", "6", "-3"]),
    ("edgeTruth", ["20", "15"]), ("edgeTruth", ["20", "1"]), ("edgeTruth", ["20", "20"]), ("edgeTruth", ["6", "4"]), ("edgeTruth", ["6", "6"]),
    ("edgeTruth", ["2", "2"]), ("edgeTruth", ["100", "51"]), ("edgeTruth", ["10", "10"]), ("edgeTruth", ["12", "7"]), ("edgeTruth", ["8", "5"]),
    ("edgeTruth", ["20", "11"]), ("edgeTruth", ["20", "0"]), ("edgeTruth", ["20", "21"]), ("edgeTruth", ["1", "1"]), ("edgeTruth", ["101", "5"]), ("edgeTruth", ["x", "5"]), ("edgeTruth", ["20", "2.5"]),
    ("streakTruth", ["6", "6"]), ("streakTruth", ["6", "1"]), ("streakTruth", ["2", "1"]), ("streakTruth", ["2", "10"]), ("streakTruth", ["100", "100"]),
    ("streakTruth", ["1000", "1000"]), ("streakTruth", ["1000", "1"]), ("streakTruth", ["20", "20"]), ("streakTruth", ["36", "36"]), ("streakTruth", ["3", "3"]),
    ("streakTruth", ["10", "7"]), ("streakTruth", ["52", "26"]), ("streakTruth", ["1", "5"]), ("streakTruth", ["1001", "5"]), ("streakTruth", ["6", "0"]),
    ("streakTruth", ["6", "1001"]), ("streakTruth", ["abc", "5"]), ("streakTruth", ["6", "abc"]), ("streakTruth", ["", ""]), ("streakTruth", ["500", "350"]),
]
out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
