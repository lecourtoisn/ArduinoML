HIGH, LOW = "HIGH", "LOW"


class Brick:
    def __init__(self, name, pin=None):
        self.name = name
        self.pin = pin

    @property
    def type(self):
        pass


class Sensor(Brick):
    @property
    def type(self):
        return "INPUT"


class Actuator(Brick):
    @property
    def type(self):
        return "OUTPUT"


class State:
    def __init__(self, name, action=None):
        self.name = name
        self.action = action
        self.transition = None


class Action:
    def __init__(self, actuator, value=None):
        self.actuator = actuator
        self.value = value


class High(Action):
    def __init__(self, actuator):
        super().__init__(actuator, HIGH)


class Low(Action):
    def __init__(self, actuator):
        super().__init__(actuator, LOW)


class Transition:
    def __init__(self, sensor=None, value=None, next=None):
        self.sensor = sensor
        self.value = value
        self.next = next


class App:
    def __init__(self, name, bricks=None, states=None):
        if states is None:
            states = []
        if bricks is None:
            bricks = []
        self.name = name
        self.bricks = bricks
        self.states = states
        self.code = None

    def _setup(self):
        for brick in self.bricks:
            self.code.append("int {} = {}".format(brick.name, brick.pin))

        self.code.append("void setup() {")
        for brick in self.bricks:
            self.code.append("\tpinMode({}, {});".format(brick.name, brick.type))

        self.code.append("}")

    def _behaviour(self):
        self.code.append("long time = 0; long debounce = 200;")
        for state in self.states:
            self.code.append("void {}() {{".format("state_" + state.name))
            self.code.append("\tdigitalWrite({}, {});".format(state.action.actuator.name, state.action.value))
            self.code.append("\tboolean guard = millis() - time > debounce;")
            self.code.append(
                "\tif (digitalRead({}) == {} && guard) {{".format(state.transition.sensor.name, state.transition.value))
            self.code.append("\t\ttime = millis();")
            self.code.append("\t\tstate_{}();".format(state.transition.next.name))
            self.code.append("\t} else {")
            self.code.append("\t\tstate_{}();".format(state.name))
            self.code.append("\t}")
            self.code.append("}")

    def generate(self):
        self.code = []
        self._setup()
        self._behaviour()
        self.code.append("void loop() {{ state_{}(); }}".format(self.states[0].name))

        self.str_code = '\n'.join(self.code)
        with open("generated.ino", "w+") as file:
            file.write(self.str_code)


if __name__ == '__main__':
    button = Sensor("button", 9)
    led = Actuator("led", 12)

    on = State("on", High(led))
    off = State("off", Low(led))

    on.transition = Transition(button, HIGH, off)
    off.transition = Transition(button, HIGH, on)

    app = App("app", [button, led], [off, on])
    app.generate()
