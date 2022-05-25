import unittest
import typewise_alert


class TypewiseTest(unittest.TestCase):
    def test_infers_breach_as_per_limits(self):
        self.assertTrue(typewise_alert.infer_breach(20, 50, 100) == 'TOO_LOW')
        self.assertTrue(typewise_alert.infer_breach(70, 50, 100) == 'NORMAL')
        self.assertTrue(typewise_alert.infer_breach(150, 50, 100) == 'TOO_HIGH')

    def test_get_temperature_limits(self):
        lower_limit, upper_limit = typewise_alert.get_temperature_limits("PASSIVE_COOLING")
        self.assertTrue(lower_limit == 0)
        self.assertTrue(upper_limit == 35)

        lower_limit, upper_limit = typewise_alert.get_temperature_limits("HI_ACTIVE_COOLING")
        self.assertTrue(lower_limit == 0)
        self.assertTrue(upper_limit == 45)

        lower_limit, upper_limit = typewise_alert.get_temperature_limits("MED_ACTIVE_COOLING")
        self.assertTrue(lower_limit == 0)
        self.assertTrue(upper_limit == 40)

    def test_classify_temperature_breach(self):
        self.assertTrue(typewise_alert.classify_temperature_breach("PASSIVE_COOLING", 40) == "TOO_HIGH")
        self.assertTrue(typewise_alert.classify_temperature_breach("HI_ACTIVE_COOLING", 40) == "NORMAL")
        self.assertTrue(typewise_alert.classify_temperature_breach("MED_ACTIVE_COOLING", -40) == "TOO_LOW")

    def test_create_alert_for_email(self):
        self.assertEqual(typewise_alert.create_alert_for_email("TOO_HIGH"),
                         ('a.b@c.com', 'Hi, the temperature is too high'))
        self.assertEqual(typewise_alert.create_alert_for_email("TOO_LOW"),
                         ('a.b@c.com', 'Hi, the temperature is too low'))
        self.assertEqual(typewise_alert.create_alert_for_email("NORMAL"), ('a.b@c.com', ""))

    def test_create_alert_for_controller(self):
        self.assertEqual(typewise_alert.create_alert_for_controller("TOO_HIGH"),
                         (65261, 'TOO_HIGH'))
        self.assertEqual(typewise_alert.create_alert_for_controller("TOO_LOW"),
                         (65261, 'TOO_LOW'))
        self.assertEqual(typewise_alert.create_alert_for_controller("NORMAL"), (65261, "NORMAL"))

    def test_send_alert(self):
        self.assertTrue(typewise_alert.send_alert("recipient", "some msg"))
        self.assertFalse(typewise_alert.send_alert("recipient", ""))

    def test_monitor_battery_temp(self):
        self.assertFalse(typewise_alert.monitor_battery_temp('TO_EMAIL', {'coolingType': "PASSIVE_COOLING"}, 20))
        self.assertTrue(typewise_alert.monitor_battery_temp('TO_CONTROLLER', {'coolingType': "HI_ACTIVE_COOLING"}, 60))


if __name__ == '__main__':
    unittest.main()
