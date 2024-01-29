# telnet_client.py
import telnetlib
import logging

_LOGGER = logging.getLogger(__name__)


class TelnetClient:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.telnet = None

    def connect(self):
        self.telnet = telnetlib.Telnet(self.host, self.port, 10)
        self.telnet.read_until(b"login: ", 5)
        _LOGGER.info("login command recieved")
        self.telnet.write(self.username.encode("ascii") + b"\n")
        self.telnet.read_until(b"Password: ", 5)
        _LOGGER.info("password command recieved")
        self.telnet.write(self.password.encode("ascii") + b"\n")
        return self.telnet.read_some().decode("ascii")

    def send_command(self, command):
        if self.telnet:
            _LOGGER.info("Sending command %s", command)
            self.telnet.write(command.encode("ascii") + b"\n")
            res = self.telnet.read_some().decode("ascii").strip()
            if not res:
                _LOGGER.info("Lost connection, attempting reconnect")
                self.connect()
                return False
            _LOGGER.info("Telnet response %s", res)
            return res
        else:
            return False

    def switch_input(self, inp, output):
        command = f"SET SW in{inp} out{output}"
        res = self.send_command(command)
        return res == f"SW in{inp} out{output}"

    def set_CEC_power(self, out, val):
        val = "on" if val else "off"
        command = f"SET CEC_PWR out{out} {val}"
        res = self.send_command(command)
        return res == f"CEC_PWR out{out} {val}"

    def set_CEC_auto_power(self, out, val):
        val = "on" if val else "off"
        command = f"SET AUTOCEC_FN out{out} {val}"
        res = self.send_command(command)
        return res == f"AUTOCEC_FN out{out} {val}"

    def set_CEC_power_delay_time(self, out, val):
        command = f"SET AUTOCEC_D out{out} {val}"
        res = self.send_command(command)
        return res == f"AUTOCEC_D out{out} {val}"

    def set_HDCP_support(self, inp, val):
        val = "on" if val else "off"
        command = f"SET HDCP_S in{inp} {val}"
        res = self.send_command(command)
        return res == f"HDCP_S in{inp} {val}"

    def set_input_EDID(self, inp, edid_val):
        command = f"SET EDID in{inp} {edid_val}"
        res = self.send_command(command)
        return res == f"EDID in{inp} {edid_val}"

    def set_mute(self, a_type, out, val):
        val = "on" if val else "off"
        a_type = a_type + "audio" if a_type != "audio" else None
        a_type = a_type + "out" + out
        command = f"SET MUTE {a_type} {val}"
        res = self.send_command(command)
        return res == f"MUTE {a_type} {val}"
