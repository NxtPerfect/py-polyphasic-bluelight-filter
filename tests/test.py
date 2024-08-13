from main import calculateChange, parseJson
import unittest


class Test(unittest.TestCase):
    def test_calculation(self):
        self.assertEqual(calculateChange(5000, 1.0, 4400, 0.4), [(
            600/60), (0.6/60)], f'Calculation expected {600/60} and {0.6/60}')

    def test_calculation_big(self):
        self.assertEqual(calculateChange(12000, 1.0, 4400, 0.4), [
                         (round((12000-4400)/60)), ((1.0-0.4)/60)], f'Calculation big expected {round((12000-4400)/60)} and {round((1.0-0.4)/60,2)}')

    def test_calculation_higher(self):
        self.assertEqual(calculateChange(5000, 1.0, 7500, 1.4), [
            (round((5000-7500)/60)), round((1.0-1.4)/60, 2)], f'Calculation higher expected {round((5000/7500)/60)} and {round((1.0-1.4)/60,2)}')

    def test_parse_json(self):
        self.assertEqual(parseJson("./testconfig.json"),
                         [tuple(['6:00', 5000, 1.0])], 'Parse json expected [6:00, 5000, 1.0]')

    def test_parse_no_json(self):
        self.assertEqual(parseJson("./fake_json_file_not_exists.json"),
                         None, 'Expected to fail')


if __name__ == "__main__":
    unittest.main()
