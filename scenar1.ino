int led = 12
int buzzer = 13
int button = 9
void setup() {
	pinMode(led, OUTPUT);
	pinMode(buzzer, OUTPUT);
	pinMode(button, INPUT);
}
long time = 0; long debounce = 200;
void state_on() {
	digitalWrite(led, HIGH);
	digitalWrite(buzzer, HIGH);
	boolean guard = millis() - time > debounce;
	if (digitalRead(button) == LOW && guard) {
		time = millis();
		state_off();
	} else {
		state_on();
	}
}
void state_off() {
	digitalWrite(led, LOW);
	boolean guard = millis() - time > debounce;
	if (digitalRead(button) == HIGH && guard) {
		time = millis();
		state_on();
	} else {
		state_off();
	}
}
void loop() { state_on(); }