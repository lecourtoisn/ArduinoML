from dsl import *

new_app("scenar4")
new_sensor("button").on(9)
new_actuator("led").on(12)
new_actuator("buzzer").on(13)
new_state("off") \
    .switch("led").to(LOW) \
    .switch("buzzer").to(LOW) \
    .go_to("inter_off").when("button").is_set_to(HIGH)
new_state("inter_off")\
    .go_to("buzz").when("button").is_set_to(LOW)
new_state("buzz") \
    .switch("led").to(HIGH)\
    .switch("buzzer").to(LOW) \
    .go_to("inter_buzz").when("button").is_set_to(HIGH)
new_state("inter_buzz")\
    .go_to("led").when("button").is_set_to(LOW)
new_state("led") \
    .switch("led").to(LOW) \
    .switch("buzzer").to(HIGH) \
    .go_to("inter_led").when("button").is_set_to(HIGH)
new_state("inter_led")\
    .go_to("off").when("button").is_set_to(LOW)
generate()
