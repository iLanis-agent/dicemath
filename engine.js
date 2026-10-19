// Dice Math engine: exact probabilities for fair dice on BigInt counts and fractions.
var DICE_ERR = "dice must be a whole number from 1 to 10";
var SIDES_ERR = "sides must be a whole number from 2 to 100";
var X_ERR = "the chance must be written as 1 in X, with X a whole number from 2 to 1000";
var N_ERR = "tries must be a whole number from 1 to 1000";

function _int(t, lo, hi, err) {
  t = typeof t === "string" ? t.trim() : "";
  if (!/^-?[0-9]{1,6}$/.test(t)) throw new Error(err);
  var v = parseInt(t, 10);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
function _fmt(num, den, k) {
  var p = 10n ** BigInt(k);
  var s = ((2n * num * p + den) / (2n * den)).toString();
  while (s.length < k + 1) s = "0" + s;
  return s.slice(0, s.length - k) + "." + s.slice(s.length - k);
}
function _pc(num, den) { return _fmt(num * 100n, den, 2) + "%"; }
function _dice(n) { return n === 1 ? "1 die" : n + " dice"; }
function _tries(n) { return n + (n === 1 ? " try" : " tries"); }

// The sum truth: how many of the equally likely rolls give a total.
function sumTruth(dice, sides, target) {
  var n = _int(dice, 1, 10, DICE_ERR), s = _int(sides, 2, 100, SIDES_ERR);
  var t = _int(target, -1000000, 1000000, "target must be a whole number from " + n + " to " + (n * s));
  if (t < n || t > n * s) throw new Error("target must be a whole number from " + n + " to " + (n * s));
  // ways[k] = rolls of the dice so far with total k
  var ways = [1n];
  for (var d = 0; d < n; d++) {
    var next = new Array(ways.length + s).fill(0n);
    for (var k = 0; k < ways.length; k++) if (ways[k] !== 0n) for (var f = 1; f <= s; f++) next[k + f] += ways[k];
    ways = next;
  }
  var total = BigInt(s) ** BigInt(n), exact = ways[t], atLeast = 0n;
  for (var j = t; j < ways.length; j++) atLeast += ways[j];
  return "Rolling " + _dice(n) + " with " + s + " sides each, a total of exactly " + t + " comes up in " + exact + " of " + total + " equally likely rolls (" +
    _pc(exact, total) + "), and a total of " + t + " or more in " + atLeast + " (" + _pc(atLeast, total) + ").";
}

// The edge truth: one die needing a number or higher, with one roll, advantage and disadvantage.
function edgeTruth(sides, target) {
  var s = _int(sides, 2, 100, SIDES_ERR), t = _int(target, 1, 100, "target must be a whole number from 1 to " + s);
  if (t > s) throw new Error("target must be a whole number from 1 to " + s);
  var S = BigInt(s), win = S - BigInt(t) + 1n, lose = BigInt(t) - 1n;
  var adv = S * S - lose * lose, dis = win * win;
  return "On one die with " + s + " sides, needing " + t + " or higher succeeds " + _pc(win, S) + " of the time with a single roll, " + _pc(adv, S * S) +
    " with advantage (roll two, keep the higher) and " + _pc(dis, S * S) + " with disadvantage (roll two, keep the lower).";
}

// The streak truth: a 1 in X chance tried over and over.
function streakTruth(x, tries) {
  var X = _int(x, 2, 1000, X_ERR), n = _int(tries, 1, 1000, N_ERR);
  var bx = BigInt(X), none = (bx - 1n) ** BigInt(n), all = bx ** BigInt(n);
  var one = all - none;
  var m = 0, nn = 1n, dd = 1n;
  while (true) { m++; nn *= bx - 1n; dd *= bx; if (2n * (dd - nn) >= dd) break; }
  return "With a 1 in " + X + " chance on each try, " + _tries(n) + " give at least one success " + _pc(one, all) + " of the time and none " + _pc(none, all) +
    " of the time. The first number of tries that reaches 50% is " + m + " (" + _pc(dd - nn, dd) + ").";
}
