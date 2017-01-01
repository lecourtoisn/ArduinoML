from model import *

bricks = {}
states = {}
app = None


class BrickSugar:
    def __init__(self, name, brick):
        global bricks
        self.brick = brick(name)
        bricks[name] = self.brick

    def on(self, pin):
        global bricks
        self.brick.pin = pin


class TransitionSugar:
    def __init__(self, state_sugar):
        self.state_sugar = state_sugar

    def when(self, sensor_name):
        global bricks
        sensor = bricks[sensor_name]
        self.state_sugar.state.transition.sensor = sensor
        return self

    def is_set_to(self, value):
        self.state_sugar.state.transition.value = value
        return self.state_sugar


class StateSugar:
    def __init__(self, name):
        global states
        self.state = State(name)
        states[name] = self.state

    def switch(self, actuator_name):
        actuator = bricks[actuator_name]
        self.state.action = (Action(actuator))
        return ActionSugar(self)

    def go_to(self, state_name):
        state = states[state_name]
        self.state.transition = Transition()
        self.state.transition.next = state
        return TransitionSugar(self)


class ActionSugar:
    def __init__(self, state_sugar):
        self.state_sugar = state_sugar

    def to(self, value):
        self.state_sugar.state.action.value = value
        return self.state_sugar


def new_app(name):
    global app
    app = App(name)


def new_sensor(name):
    return BrickSugar(name, Sensor)


def new_actuator(name):
    return BrickSugar(name, Actuator)


def new_state(name):
    return StateSugar(name)


def generate():
    app.bricks = bricks
    app.states = states

    app.generate()


if __name__ == '__main__':
    app("test")
    new_actuator("led").on(9)
    new_sensor("button").on(12)

    for brick in bricks.values():
        print(brick.name, brick.pin)

    generate()