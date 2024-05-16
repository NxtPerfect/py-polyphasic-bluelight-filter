from main import calculateChange, parseJson
import unittest


class Test(unittest.TestCase):
    def test_calculation(self):
        self.assertEqual(calculateChange(5000, 1.0, 4400, 0.4), [(
            600/600), (0.6/600)], f'Should be {600/600} and {0.6/600}')

    def test_calculation_big(self):
        self.assertEqual(calculateChange(12000, 1.0, 4400, 0.4), [
                         (int((12000-4400)/600)), ((1.0-0.4)/600)], f'Should be {int((12000-4400)/600)} and {(1.0-0.4)/600}')

    def test_parse_json(self):
        self.assertEqual(parseJson("./testconfig.json"),
                         [tuple(['6:00', 5000, 1.0])], 'Should be [6:00, 5000, 1.0]')


if __name__ == "__main__":
    unittest.main()
