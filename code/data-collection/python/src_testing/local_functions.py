from classes_arduino import ArdUIno
from classes_arduino import tryexceptArduino, reLoad
from classes_colther import Zaber
from classes_colther import (
    moveAxisTo,
    movePanTilt,
    homingZabersConcu,
    set_up_big_three,
    movetostartZabersConcu,
)
from classes_text import waitForEnter
from index_funcs import threadFunctions
from classes_text import printme

from sys import platform
import os
import globals
import time
import keyboard


def homeArduinos(arduino_syringe, arduino_pantilt, arduino_dimmer):

    if arduino_syringe:
        globals.stimulus = 0
        tryexceptArduino(arduino_syringe, globals.stimulus)

    if arduino_pantilt:
        movePanTilt(arduino_pantilt, globals.default_pantilt)

    if arduino_dimmer:
        globals.lamp = 0
        tryexceptArduino(arduino_dimmer, globals.lamp)


def arduinos_zabers():
    zabers = set_up_big_three(globals.axes)
    platform1 = Zaber(1, who="serial", surname_serial="AH0614UB")

    # check colther position
    colther_x_pos = zabers["colther"]["x"].device.send("/get pos")
    colther_y_pos = zabers["colther"]["y"].device.send("/get pos")
    pos_colther = [
        not colther_x_pos.warning_flag == "--",
        not colther_y_pos.warning_flag == "--",
    ]

    # check touch position
    tactile_x_pos = zabers["tactile"]["x"].send("/get pos")
    tactile_y_pos = zabers["tactile"]["y"].send("/get pos")
    pos_tactile = [
        not tactile_x_pos.warning_flag == "--",
        not tactile_y_pos.warning_flag == "--",
    ]

    homingZabersConcu(zabers, {"colther": ["z"]})

    if (
        not any(pos_tactile)
        and not any(pos_colther)
        and int(tactile_x_pos.data) > 1000
        and int(tactile_y_pos.data) > 1000
    ):
        moveAxisTo(zabers, "tactile", "z", globals.base_touch)
    homingZabersConcu(zabers, {"colther": ["x"]})

    if (
        not any(pos_tactile)
        and not any(pos_colther)
        and int(colther_x_pos.data) > 1000
        and int(colther_y_pos.data) > 1000
    ):
        moveAxisTo(zabers, "colther", "y", globals.dry_ice_pos["y"])
    homingZabersConcu(zabers, {"camera": ["z"]})
    if (
        not any(pos_tactile)
        and not any(pos_colther)
        and int(tactile_x_pos.data) > 1000
        and int(tactile_y_pos.data) > 1000
    ):
        moveAxisTo(zabers, "tactile", "x", 533332)
    homingZabersConcu(zabers, {"tactile": ["y"]})

    arduino_pantilt = ArdUIno(
        usb_port=globals.usb_port_pantilt,
        n_modem=globals.modem_port_pantilt,
        name="PanTilt",
    )
    arduino_pantilt.arduino.flushInput()
    time.sleep(0.1)

    # Arduino syringe motors
    arduino_syringe = ArdUIno(
        usb_port=globals.usb_port_syringe,
        n_modem=globals.modem_port_syringe,
        name="syringe",
    )
    arduino_syringe.arduino.flushInput()
    time.sleep(0.1)

    # Arduino dimmers
    arduino_dimmer = ArdUIno(
        usb_port=globals.usb_port_dimmer,
        n_modem=globals.modem_port_dimmer,
        name="dimmer",
    )
    arduino_dimmer.arduino.flushInput()
    time.sleep(0.1)

    platform1.device.send(f"set maxspeed {206408*4}")
    platform1.device.home()
    homingZabersConcu(zabers, globals.haxes)

    return zabers, platform1, arduino_pantilt, arduino_syringe, arduino_dimmer


def set_up_arduinos():

    arduino_pantilt = ArdUIno(
        usb_port=globals.usb_port_pantilt, n_modem=globals.modem_port_pantilt
    )
    arduino_pantilt.arduino.flushInput()
    time.sleep(0.1)

    # Arduino syringe motors
    arduino_syringe = ArdUIno(
        usb_port=globals.usb_port_syringe, n_modem=globals.modem_port_syringe
    )
    arduino_syringe.arduino.flushInput()
    time.sleep(0.1)

    # Arduino dimmers
    arduino_dimmer = ArdUIno(
        usb_port=globals.usb_port_dimmer, n_modem=globals.modem_port_dimmer
    )
    arduino_dimmer.arduino.flushInput()
    time.sleep(0.1)

    return arduino_syringe, arduino_dimmer, arduino_pantilt


def set_up_zabers():
    time.sleep(1)
    zabers = set_up_big_three(globals.axes)
    platform1 = Zaber(1, who="serial", surname_serial="AH0614UB")
    platform1.device.send(f"set maxspeed {206408*4}")
    platform1.device.home()
    homingZabersConcu(zabers, globals.haxes)

    return zabers, platform1


def panicButton():
    if keyboard.is_pressed("p"):
        os.system("clear")
        waitForEnter("\n\n Press enter when panic is over...")


def trigger_handle_reload(
    zabers,
    platform,
    arduino_syringe,
    arduino_pantilt,
    cam,
    n_block,
    within_block_counter,
    arduino_dimmer,
):
    if keyboard.is_pressed("s"):
        tactile_x_pos = zabers["tactile"]["x"].send("/get pos")
        tactile_y_pos = zabers["tactile"]["y"].send("/get pos")
        pos_tactile = [
            not tactile_x_pos.warning_flag == "--",
            not tactile_y_pos.warning_flag == "--",
        ]

        if (
            not any(pos_tactile)
            and int(tactile_x_pos.data) > 1000
            and int(tactile_y_pos.data) > 1000
        ):
            moveAxisTo(zabers, "tactile", "z", globals.base_touch)
            moveAxisTo(zabers, "tactile", "x", globals.tactile_x_save)
            moveAxisTo(zabers, "tactile", "y", globals.tactile_y_save)

        homingZabersConcu(zabers, {"colther": globals.haxes["colther"]})
        movePanTilt(arduino_pantilt, globals.default_pantilt)
        platform.device.move_abs(0)
        homingZabersConcu(zabers, {"camera": globals.haxes["camera"]})

        thermalCalibration(zabers, arduino_syringe, arduino_dimmer, cam)
        n_block += 1
        within_block_counter = 1

    return True, n_block, within_block_counter


def dryiceRiskAssess(ard_syringe, times=3):
    for i in range(times):
        globals.stimulus = 1
        tryexceptArduino(ard_syringe, globals.stimulus)
        time.sleep(0.4)

        globals.stimulus = 6
        tryexceptArduino(ard_syringe, globals.stimulus)
        time.sleep(0.4)

        globals.stimulus = 0
        tryexceptArduino(ard_syringe, globals.stimulus)
        time.sleep(0.4)


def thermalCalibration(zabers, arduino_syringe, arduino_dimmer, cam):

    movetostartZabersConcu(
        zabers,
        "colther",
        list(reversed(globals.haxes["colther"])),
        pos=globals.dry_ice_pos,
    )
    # Dry ice load
    globals.stimulus = 7
    tryexceptArduino(arduino_syringe, globals.stimulus)
    globals.stimulus = 0
    tryexceptArduino(arduino_syringe, globals.stimulus)

    # Turn lamp on
    globals.lamp = 1
    tryexceptArduino(arduino_dimmer, globals.lamp)

    # Get camera out of the way
    reLoad(arduino_syringe)

    homingZabersConcu(zabers, globals.haxes)
    os.system("clear")

    # Turn lamp off
    globals.lamp = 0
    tryexceptArduino(arduino_dimmer, globals.lamp)

    # Subject in position
    movetostartZabersConcu(zabers, "camera", ["y"], {"y": 157480})
    os.system("clear")
    waitForEnter("\n\n Press enter when participant is comfortable and ready\n\n")
    homingZabersConcu(zabers, globals.haxes)

    # Shutter refresh and stabilisation
    cam.setShutterManual()
    cam.performManualff()
    printme(
        "Performing shutter refresh and taking a 10-second break\nto let the thermal image stabilise"
    )
    time.sleep(10)

    dryiceRiskAssess(arduino_syringe)
    globals.stimulus = 4
    tryexceptArduino(arduino_syringe, globals.stimulus)
    printme("Resuming experiment...")


def closeEnvelope(zabers, platform, arduino_syringe, arduino_pantilt, arduino_dimmer):
    globals.touch = 0
    #### HOMER ARDUINOS & ZABERS
    # check colther position
    colther_x_pos = zabers["colther"]["x"].device.send("/get pos")
    colther_y_pos = zabers["colther"]["y"].device.send("/get pos")
    pos_colther = [
        not colther_x_pos.warning_flag == "--",
        not colther_y_pos.warning_flag == "--",
    ]

    # check touch position
    tactile_x_pos = zabers["tactile"]["x"].send("/get pos")
    tactile_y_pos = zabers["tactile"]["y"].send("/get pos")
    pos_tactile = [
        not tactile_x_pos.warning_flag == "--",
        not tactile_y_pos.warning_flag == "--",
    ]

    homingZabersConcu(zabers, {"colther": ["z"]})

    if (
        not any(pos_tactile)
        and not any(pos_colther)
        and int(tactile_x_pos.data) > 1000
        and int(tactile_y_pos.data) > 1000
    ):
        moveAxisTo(zabers, "tactile", "z", globals.base_touch)
    homingZabersConcu(zabers, {"colther": ["x"]})

    if (
        not any(pos_tactile)
        and not any(pos_colther)
        and int(colther_x_pos.data) > 1000
        and int(colther_y_pos.data) > 1000
    ):
        moveAxisTo(zabers, "colther", "y", globals.dry_ice_pos["y"])
    homingZabersConcu(zabers, {"camera": ["z"]})
    platform.device.move_abs(0)
    if (
        not any(pos_tactile)
        and not any(pos_colther)
        and int(tactile_x_pos.data) > 1000
        and int(tactile_y_pos.data) > 1000
    ):
        moveAxisTo(zabers, "tactile", "x", 533332)
    homingZabersConcu(zabers, {"tactile": ["y"]})

    homingZabersConcu(zabers, {"colther": globals.haxes["colther"]})
    homingZabersConcu(zabers, {"camera": ["z"]})
    homeArduinos(arduino_syringe, arduino_pantilt, arduino_dimmer)
    homingZabersConcu(zabers, globals.haxes)


def iti_zaber_dance_away(zabers):
    funcs = [
        [moveAxisTo, [zabers, "colther", "z", 0]],
        # [moveAxisTo, [zabers, "camera", "x", 90079]],
        # [moveAxisTo, [zabers, "camera", "z", 0]],
        # [moveAxisTo, [zabers, "camera", "x", 1000]],
        [moveAxisTo, [zabers, "colther", "x", 120000]],
        [moveAxisTo, [zabers, "colther", "y", 90000]],
    ]
    threadFunctions(funcs)


def iti_zaber_dance_in(zabers, p):
    funcs = [
        [
            movetostartZabersConcu,
            [zabers, "camera", ["x", "y", "z"], globals.grid["camera"][str(p)]],
        ]
    ]
    threadFunctions(funcs)

    # movetostartZabersConcu(
    #     zabers, "camera", ["z"], pos=globals.grid["camera"][str(p)]
    # )
    movetostartZabersConcu(
        zabers,
        "colther",
        list(reversed(globals.haxes["colther"])),
        pos=globals.grid["colther"][str(p)],
    )
