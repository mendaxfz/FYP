#!/usr/bin/env python3
import time 
import RPi.GPIO as GPIO
from RpiMotorLib import rpi_dc_lib 
from random import *
from math import floor
import smbus
import logging
import TSL2591
import asyncio
from jsonrpc_websocket import Server as WsClient

logging.basicConfig(level=logging.INFO)

ws_client = None

# ====== DC motor driven by TB6612FNG ====
# TB66 -- GPIO RPI
PWA = 17
AI1 = 22
AI2 = 27
PWB = 18
BI1 = 23
BI2 = 24
Standby = 25

Freq = 50

MotorOne = rpi_dc_lib.TB6612FNGDc(AI1 ,AI2 ,PWA ,Freq,True, "motor_one")
MotorTwo = rpi_dc_lib.TB6612FNGDc(BI1 ,BI2 ,PWB ,Freq ,True, "motor_two")
# ========================================

# Light sensor ---------------------------
sensor = TSL2591.TSL2591()
# sensor.SET_InterruptThreshold(0xff00, 0x0010)
# ========================================

reset_speed = 25

speed_m1 = None
speed_m2 = None

def reset_motors_speed():
    global speed_m1, speed_m2
    speed_m1 = reset_speed
    speed_m2 = reset_speed

def randwalk(is_small):
    global speed_m1, speed_m2
    reset_motors_speed()

    motor = floor(random())

    sleep_time = 1

    min_pwm = None
    max_pwm = None

    if is_small == True:
        min_pwm = 40
        max_pwm = 50
    else:
        min_pwm = 50
        max_pwm = 100
        sleep_time = 1.9

    if motor == 0:
        speed_m1 = randint(min_pwm, max_pwm)
    else:
        speed_m2 = randint(min_pwm, max_pwm)

    MotorOne.forward(speed_m1)
    MotorTwo.forward(speed_m2)

def gradient_move(side):
    global speed_m1, speed_m2
    if side == 'Positive':
        reset_motors_speed()

        MotorOne.forward(speed_m1)
        MotorTwo.forward(90)
    else:
        reset_motors_speed()

        MotorOne.forward(90)
        MotorTwo.forward(speed_m2)

async def ws_routine():
    global ws_client
    uri = "ws://localhost:8080"
    client = WsClient(uri)
    try:
        await client.ws_connect()
    except Exception as e:
        print(e)
    finally:
        await client.close()

def min_max_reschale(x, a, b, min_x, max_x):
    if x > max_x:
        x = max_x
    return a + ((x - min_x)*(b-a))/(max_x - min_x)

def _comparator(temp, fireThreshold):
    if temp > (fireThreshold + 0.5):
        print('[ ] Positive comparator called')
        return 'Positive'
    elif temp < (fireThreshold - 0.5):
        print('[ ] Negative comparator called')
        return 'Negative'
    else:
        print('[i] IDEAL')
        return 'Equal'

def _gradientDetector(side, prevTemp, temp):
    if side == 'Positive':
        print('[ ] Positive detector called')
        if temp > prevTemp + 0.3:
            return True
    elif side == 'Negative':
        print('[ ] Negative detector called')
        if temp < prevTemp - 0.3:
            return True
    return False

async def main_routine():

    lux = sensor.Lux
    print('Lux: %d'%lux)

    c_temp = min_max_reschale(lux, 17, 23, 0, 50)
    print('Lux temp: ' + str(c_temp))

    prevTemp = c_temp

    comp_res = _comparator(c_temp, 20)
    if comp_res == 'Positive':
        grad_res = _gradientDetector('Positive', prevTemp, c_temp)
        if grad_res is True:
            gradient_move('Positive')
        else:
            randwalk(False)
    elif comp_res == 'Negative':
        grad_res = _gradientDetector('Negative', prevTemp, c_temp)
        if grad_res is True:
            gradient_move('Negative')
        else:
            randwalk(False)
    else:
        randwalk(True)

    prevTemp = c_temp

async def main():
    reset_motors_speed()
    rpi_dc_lib.TB6612FNGDc.standby(Standby, True)
    time.sleep(1)
    try:
        while True:
            asyncio.ensure_future(main_routine())
            await asyncio.sleep(0.15)
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        sensor.Disable()
    finally:
        rpi_dc_lib.TB6612FNGDc.standby(Standby, False)
        GPIO.cleanup()
        exit()

if __name__ == "__main__":
    asyncio.run(main())

