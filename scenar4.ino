int buzzer = 13
int button = 9
int led = 12
void setup() {
	pinMode(buzzer, OUTPUT);
	pinMode(button, INPUT);
	pinMode(led, OUTPUT);
}
long time = 0; long debounce = 200;
void state_inter_led() {
	boolean guard = millis() - time > debounce;
	if (digitalRead(button) == LOW && guard) {
		time = millis();
		state_off();
	} else {
		state_inter_led();
	}
}
void state_inter_off() {
	boolean guard = millis() - time > debounce;
	if (digitalRead(button) == LOW && guard) {
		time = millis();
		state_buzz();
	} else {
		state_inter_off();
	}
}
void state_off() {
	digitalWrite(led, LOW);
	digitalWrite(buzzer, LOW);
	boolean guard = millis() - time > debounce;
	if (digitalRead(button) == HIGH && guard) {
		time = millis();
		state_inter_off();
	} else {
		state_off();
	}
}
void state_inter_buzz() {
	boolean guard = millis() - time > debounce;
	if (digitalRead(button) == LOW && guard) {
		time = millis();
		state_led();
	} else {
		state_inter_buzz();
	}
}
void state_buzz() {
	digitalWrite(led, HIGH);
	digitalWrite(buzzer, LOW);
	boolean guard = millis() - time > debounce;
	if (digitalRead(button) == HIGH && guard) {
		time = millis();
		state_inter_buzz();
	} else {
		state_buzz();
	}
}
void state_led() {
	digitalWrite(led, LOW);
	digitalWrite(buzzer, HIGH);
	boolean guard = millis() - time > debounce;
	if (digitalRead(button) == HIGH && guard) {
		time = millis();
		state_inter_led();
	} else {
		state_led();
	}
}
void loop() { state_inter_led(); }