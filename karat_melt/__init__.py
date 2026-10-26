"""karat-melt: melt-value arithmetic for karat gold, with the unit traps made explicit.

Everything here is definitional arithmetic, not market data:

* fineness is karat/24, except where a hallmark standard is the trade convention
  (24K is sold as 999 fine and 14K as 585 fine);
* 1 troy ounce = 31.1034768 g (exact), 1 pennyweight = 1/20 troy ounce = 1.55517384 g,
  1 avoirdupois ounce = 28.349523125 g (exact).

Spot prices are never bundled: you pass the spot price (USD or any currency per troy
ounce) you observed, and every function returns values in that same currency.
"""

__version__ = "0.1.0"

GRAMS_PER_TROY_OUNCE = 31.1034768
GRAMS_PER_PENNYWEIGHT = GRAMS_PER_TROY_OUNCE / 20  # 1.55517384
GRAMS_PER_AVOIRDUPOIS_OUNCE = 28.349523125

UNIT_GRAMS = {
    "g": 1.0,
    "ozt": GRAMS_PER_TROY_OUNCE,
    "dwt": GRAMS_PER_PENNYWEIGHT,
    "oz": GRAMS_PER_AVOIRDUPOIS_OUNCE,
}

# Hallmark fineness used by the trade for the common karats; other karats fall back
# to the bare karat/24 fraction.
HALLMARK_FINENESS = {24: 0.999, 22: 0.9167, 18: 0.750, 14: 0.585, 10: 0.4167}


def fineness(karat, standard="hallmark"):
    """Gold fraction for a karat. standard='hallmark' (999/585 conventions) or 'fraction' (k/24)."""
    k = float(karat)
    if not 0 < k <= 24:
        raise ValueError("karat must be in (0, 24]")
    if standard == "fraction":
        return k / 24.0
    if standard != "hallmark":
        raise ValueError("standard must be 'hallmark' or 'fraction'")
    return HALLMARK_FINENESS.get(int(k) if k == int(k) else None, k / 24.0)


def to_grams(weight, unit="g"):
    """Convert a scale reading to grams. unit is one of g, ozt (troy), dwt, oz (avoirdupois)."""
    try:
        factor = UNIT_GRAMS[unit]
    except KeyError:
        raise ValueError("unit must be one of %s" % ", ".join(sorted(UNIT_GRAMS)))
    if weight < 0:
        raise ValueError("weight must be >= 0")
    return float(weight) * factor


def convert(weight, from_unit, to_unit):
    """Convert between g, ozt, dwt and oz."""
    return to_grams(weight, from_unit) / UNIT_GRAMS[to_unit]


def pure_gold_grams(weight, unit, karat, standard="hallmark"):
    """Grams of fine gold contained in an item."""
    return to_grams(weight, unit) * fineness(karat, standard)


def melt_value(weight, unit, karat, spot_per_troy_oz, standard="hallmark"):
    """Melt value = fine-gold troy ounces x spot. Returned in the spot price's currency."""
    if spot_per_troy_oz < 0:
        raise ValueError("spot price must be >= 0")
    return pure_gold_grams(weight, unit, karat, standard) / GRAMS_PER_TROY_OUNCE * spot_per_troy_oz


def price_table(spot_per_troy_oz, karats=(24, 22, 18, 14, 10), standard="hallmark"):
    """Per-gram, per-pennyweight and per-troy-ounce melt value for each karat."""
    rows = []
    for k in karats:
        per_g = melt_value(1, "g", k, spot_per_troy_oz, standard)
        rows.append({
            "karat": k,
            "fineness": fineness(k, standard),
            "per_gram": per_g,
            "per_pennyweight": per_g * GRAMS_PER_PENNYWEIGHT,
            "per_troy_oz": per_g * GRAMS_PER_TROY_OUNCE,
        })
    return rows


def offer_share(offer, weight, unit, karat, spot_per_troy_oz, standard="hallmark"):
    """A buyer's offer as a fraction of melt value (0.75 means the offer is 75% of melt)."""
    melt = melt_value(weight, unit, karat, spot_per_troy_oz, standard)
    if melt == 0:
        raise ValueError("melt value is zero; cannot express the offer as a share")
    return offer / melt


def unit_mixup_error():
    """Relative overstatement (about 0.0971, i.e. 9.71%) when an avoirdupois-ounce scale
    reading is valued as if it were troy ounces."""
    return GRAMS_PER_TROY_OUNCE / GRAMS_PER_AVOIRDUPOIS_OUNCE - 1
