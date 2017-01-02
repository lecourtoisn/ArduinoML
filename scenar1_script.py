from dsl import *

new_app("scenar1")
new_sensor("button").on(9)
new_actuator("led").on(12)
new_actuator("buzzer").on(13)
new_state("off") \
    .switch("led").to(LOW) \
    .go_to("on").when("button").is_set_to(HIGH)
new_state("on") \
    .switch("led").to(HIGH) \
    .switch("buzzer").to(HIGH)\
    .go_to("off").when("button").is_set_to(LOW)

generate()
