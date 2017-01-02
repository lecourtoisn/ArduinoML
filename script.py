from dsl import *

new_app("switch")
new_sensor("button").on(9)
new_actuator("led").on(12)
new_state("off") \
    .switch("led").to(LOW) \
    .switch("led").to(HIGH)\
    .go_to("on").when("button").is_set_to(HIGH)
new_state("on") \
    .switch("led").to(HIGH) \
    .go_to("off").when("button").is_set_to(HIGH)

generate()
