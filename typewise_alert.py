def infer_breach(value, lower_limit, upper_limit):
    if value < lower_limit:
        return 'TOO_LOW'
    if value > upper_limit:
        return 'TOO_HIGH'
    return 'NORMAL'


class PassiveCooling:
    lower_limit = 0
    upper_limit = 35


class HiActiveCooling:
    lower_limit = 0
    upper_limit = 45


class MidActiveCooling:
    lower_limit = 0
    upper_limit = 40


class CoolingTypeFactory:
    def __init__(self):
        self.temp_limit = {"PASSIVE_COOLING": PassiveCooling(),
                           "HI_ACTIVE_COOLING": HiActiveCooling(),
                           "MED_ACTIVE_COOLING": MidActiveCooling()}

    def get_cooling_class(self, cooling_type):
        return self.temp_limit.get(cooling_type)


def get_temperature_limits(cooling_type):
    cooling_type_obj = CoolingTypeFactory().get_cooling_class(cooling_type)
    return cooling_type_obj.lower_limit, cooling_type_obj.upper_limit


def classify_temperature_breach(cooling_type, temperature_in_c):
    lower_limit, upper_limit = get_temperature_limits(cooling_type)
    return infer_breach(temperature_in_c, lower_limit, upper_limit)


def monitor_battery_temp(alert_target, battery_char, temperature_in_c):
    breach_type = classify_temperature_breach(battery_char['coolingType'], temperature_in_c)
    if alert_target == 'TO_CONTROLLER':
        recipient, msg = create_alert_for_controller(breach_type)
    elif alert_target == 'TO_EMAIL':
        recipient, msg = create_alert_for_email(breach_type)
    return send_alert(recipient, msg)


def create_alert_for_controller(breach_type):
    recipient = 0xfeed
    msg = breach_type
    return recipient, msg


def create_alert_for_email(breach_type):
    recipient = "a.b@c.com"
    msg = ""
    if breach_type == 'TOO_LOW':
        msg = 'Hi, the temperature is too low'
    elif breach_type == 'TOO_HIGH':
        msg = 'Hi, the temperature is too high'
    return recipient, msg


def send_alert(recipient, msg):
    if msg == "":
        return False
    print("\n\n---------------------------------------------------------------------------")
    print(f"Sending alert msg to: '{recipient}'")
    print(f"Alert Message: '{msg}'")
    return True
