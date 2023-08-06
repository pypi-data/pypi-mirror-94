class TorqueUser:
    def __init__(
        self,
        torque_id: str,
        email: str,
        given_name: str,
        family_name: str,
        custom_data: dict
    ):
        self.id = torque_id
        self.email = email
        self.given_name = given_name
        self.family_name = family_name
        self.custom_data = custom_data
