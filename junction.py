import RPi.GPIO as GPIO

#setup
GPIO.setmode(GPIO.BOARD)

#pins
pins = []
middle = 16
pins.append(middle)

top_1 = 13
pins.append(top_1)
top_2 = 11
pins.append(top_2)
top_3 = 12
pins.append(top_3)
top_4 = 10
pins.append(top_4)

bot_1 = 5
pins.append(bot_1)
bot_2 = 3
pins.append(bot_2)
bot_3 = 7
pins.append(bot_3)
bot_4 = 8
pins.append(bot_4)

print(pins)

for p in pins:
    GPIO.setup(p, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

for p in pins:
    print(p,GPIO.input(p))

GPIO.cleanup()
