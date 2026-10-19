# Dice Math

Fair dice probability arithmetic. A 1 in 6 chance tried 6 times gives at least one success only 66.51% of the time.

## What it computes

- **The sum truth** - how many of the equally likely rolls of several dice give an exact total, and a total or more.
- **The edge truth** - one die needing a number or higher, with a single roll, advantage (keep the higher of two) and disadvantage (keep the lower).
- **The streak truth** - a 1 in X chance tried over and over: at least one success, none at all, and the first number of tries that reaches 50%.

Dice are 1 to 10, sides 2 to 100, X is 2 to 1000, tries 1 to 1000. Percentages are rounded half up to 2 decimals.

## Boundary

Arithmetic only, for perfectly fair and independent dice. It does not know whether any real die, game or machine is fair, and says nothing about odds offered elsewhere or about whether to play. Every figure is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (BigInt counts, step-by-step roll table).
- `oracle.py` - the Python mirror (inclusion-exclusion counts, Fractions) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (67 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/dicemath/
Repo: https://github.com/iLanis-agent/dicemath
