from gpiozero import LED, AngularServo
from time import sleep

rampa =  AngularServo(2, min_angle=0, max_angle=270 , min_pulse_width=0.0005, max_pulse_width=0.0025)
ruleta = AngularServo(3, min_angle=0, max_angle=270 , min_pulse_width=0.0005, max_pulse_width=0.0025)

pos_ruleta=0


#led = LED(3)
#led.on()

while True:
	
    if pos_ruleta == 0:
        pos_ruleta = 220
    elif pos_ruleta == 220:
        pos_ruleta = 0
    ruleta.angle = pos_ruleta	
    sleep(2)
	
	
	#ruleta.angle = 0
	#rampa.angle = 30
	#sleep(2)
	#ruleta.angle = 220
	#rampa.angle = 90
	#sleep(2)
	