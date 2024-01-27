import telnetlib

class TelnetClient:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.telnet = None

    def connect(self):
        self.telnet = telnetlib.Telnet(self.host, self.port)
        self.telnet.read_until(b"login: ")
        self.telnet.write(self.username.encode("ascii") + b"\n")
        self.telnet.read_until(b"Password: ")
        self.telnet.write(self.password.encode("ascii") + b"\n")
        # Read the login response
        return self.telnet.read_some().decode("ascii")

    def send_command(self, command):
        if self.telnet:
            self.telnet.write(command.encode("ascii") + b"\n")
            return self.telnet.read_some().decode("ascii")
        return None

    def switch_input(self, inp, output):
        command = f"SET SW in{inp} out{output}"
        res = self.send_command(command)
        return True
        # return res == f"SW in{inp} out{output}"

    def set_CEC_power(self, val):
        return True

    def set_CEC_auto_power(self, val):
        return True

    def set_CEC_power_delay_time(self, val):
        return True

    def set_HDCP_support(self, val):
        return True

    def set_input_EDID(self, inp, edid_val):
        return True

    def set_mute(self, val):
        return True
