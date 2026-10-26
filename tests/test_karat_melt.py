import unittest
import karat_melt as km


class T(unittest.TestCase):
    def test_constants(self):
        self.assertAlmostEqual(km.GRAMS_PER_PENNYWEIGHT, 1.55517384, places=8)
        self.assertAlmostEqual(km.convert(1, "ozt", "oz"), 1.09714286, places=7)

    def test_fineness(self):
        self.assertEqual(km.fineness(24), 0.999)
        self.assertEqual(km.fineness(14), 0.585)
        self.assertAlmostEqual(km.fineness(14, "fraction"), 14 / 24)
        self.assertAlmostEqual(km.fineness(9), 0.375)
        with self.assertRaises(ValueError):
            km.fineness(25)

    def test_dataset_snapshot_ratios(self):
        # The c71 reference CSV implies spot ~3350 USD/ozt; 14K per gram there was 63.01.
        self.assertAlmostEqual(km.melt_value(1, "g", 14, 3350.0), 63.01, delta=0.02)
        self.assertAlmostEqual(km.melt_value(1, "g", 24, 3350.0), 107.60, delta=0.02)

    def test_units_and_offer(self):
        m = km.melt_value(1, "ozt", 24, 4000)
        self.assertAlmostEqual(m, 3996.0, places=6)
        self.assertAlmostEqual(km.offer_share(m * 0.8, 1, "ozt", 24, 4000), 0.8)
        self.assertAlmostEqual(km.unit_mixup_error(), 0.0971428, places=6)

    def test_table(self):
        rows = km.price_table(4020.90)
        self.assertEqual([r["karat"] for r in rows], [24, 22, 18, 14, 10])
        self.assertAlmostEqual(rows[3]["per_gram"], 75.63, delta=0.01)


if __name__ == "__main__":
    unittest.main()
