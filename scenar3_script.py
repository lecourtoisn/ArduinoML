from dsl import *

new_app("scenar3")
new_sensor("button").on(9)
new_actuator("led").on(12)
new_state("off") \
    .switch("led").to(LOW) \
    .go_to("inter_low").when("button").is_set_to(HIGH)
new_state("inter_low") \
    .go_to("on").when("button").is_set_to(LOW)
new_state("on") \
    .switch("led").to(HIGH) \
    .go_to("inter_on").when("button").is_set_to(HIGH)
new_state("inter_on") \
    .go_to("off").when("button").is_set_to(LOW)
generate()
