# karat-melt

Small, dependency-free Python helpers for the arithmetic behind gold melt values:
karat fineness, gram / troy-ounce / pennyweight / avoirdupois-ounce conversion, melt value
at a spot price you supply, and a buyer's offer expressed as a share of melt.

No prices are bundled. Spot moves every minute, so every function takes the spot price
you observed and returns values in that currency.

```python
import karat_melt as km

km.melt_value(5, "g", 14, spot_per_troy_oz=4020.90)   # 378.13
km.offer_share(300, 5, "g", 14, 4020.90)              # 0.793 -> offer is 79.3% of melt
km.convert(1, "ozt", "g")                             # 31.1034768
km.unit_mixup_error()                                 # 0.0971 -> valuing avoirdupois oz as troy overstates by 9.71%
```

```
$ python -m karat_melt 4020.90
karat  fineness  per_gram  per_dwt  per_troy_oz
  24K    0.9990    129.15   200.84      4016.88
  22K    0.9167    118.51   184.30      3685.96
  18K    0.7500     96.96   150.78      3015.68
  14K    0.5850     75.63   117.61      2352.23
  10K    0.4167     53.87    83.78      1675.51
```

## Conventions

| Quantity | Value | Status |
|---|---|---|
| troy ounce | 31.1034768 g | exact (definition) |
| pennyweight | 1/20 ozt = 1.55517384 g | exact |
| avoirdupois ounce | 28.349523125 g | exact |
| 24K fineness | 0.999 (999 fine) | trade hallmark; `standard="fraction"` gives 1.0 |
| 14K fineness | 0.585 (585 hallmark) | trade hallmark; `standard="fraction"` gives 0.5833 |
| other karats | karat / 24 | definition |

These are the same conventions used by the
[GoldGramPrice scrap gold calculator](https://goldgramprice.com/scrap-gold-calculator/)
(which also grades a buyer's offer against melt) and its
[gold weight converter](https://goldgramprice.com/gold-weight-converter/); the test suite
reproduces that calculator's per-karat table to the cent at the same spot.

Melt value is the metal content only. Dealers pay a share of melt that depends on
refining cost, volume and margin, which is why `offer_share` exists.

## Install

```
conda install -c freedomluckystrike karat-melt
```
or copy `karat_melt/` into your project (MIT licensed, standard library only).

## Tests

```
python tests/test_karat_melt.py
```
