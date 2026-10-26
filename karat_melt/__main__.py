"""python -m karat_melt SPOT [WEIGHT UNIT KARAT [OFFER]]"""
import sys
from . import price_table, melt_value, offer_share


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    if not a or a[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0
    spot = float(a[0])
    if len(a) == 1:
        print("karat  fineness  per_gram  per_dwt  per_troy_oz")
        for r in price_table(spot):
            print("%4dK  %8.4f  %8.2f  %7.2f  %11.2f" % (r["karat"], r["fineness"], r["per_gram"],
                                                         r["per_pennyweight"], r["per_troy_oz"]))
        return 0
    weight, unit, karat = float(a[1]), a[2], float(a[3])
    melt = melt_value(weight, unit, karat, spot)
    print("melt value: %.2f" % melt)
    if len(a) > 4:
        print("offer is %.1f%% of melt" % (100 * offer_share(float(a[4]), weight, unit, karat, spot)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
