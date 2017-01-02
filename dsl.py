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


class StateSugar:
    def __init__(self, name):
        global states
        self.state = State(name)
        states[name] = self.state

    def switch(self, actuator_name):
        actuator = bricks[actuator_name]
        new_action = Action(actuator)
        self.state.actions.append(new_action)
        return ActionSugar(self, new_action)

    def go_to(self, state_name):
        self.state.transition = Transition()
        self.state.transition.next = state_name
        return TransitionSugar(self)


class ActionSugar:
    def __init__(self, state_sugar, action):
        self.state_sugar = state_sugar
        self.action = action

    def to(self, value):
        self.action.value = value
        return self.state_sugar


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
    app.bricks = list(bricks.values())
    app.states = list(states.values())

    for state in states.values():
        next_state = states[state.transition.next]
        state.transition.next = next_state
    app.generate()

