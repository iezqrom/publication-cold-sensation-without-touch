#### OWN LIBRARIES
from classes_colther import (
    triggered_exception,
)
from local_functions import closeEnvelope, arduinos_zabers
from classes_arduino import shakeShutter

if __name__ == "__main__":
    try:
        ### ARDUINOS & ZABERS
        (
            zabers,
            platform1,
            arduino_pantilt,
            arduino_syringe,
            arduino_dimmer,
        ) = arduinos_zabers()
        #### SHAKE SHUTTER
        shakeShutter(arduino_syringe, 5)

        ##### ZABER GAME
        zabers["colther"]["x"].manualCon3PanTilt(
            zabers, arduino_pantilt, arduino_syringe, home="n"
        )

        #### HOMER ARDUINOS & ZABERS
        closeEnvelope(
            zabers, platform1, arduino_syringe, arduino_pantilt, arduino_dimmer
        )

    except Exception as e:
        triggered_exception(
            zabers=zabers,
            platform=platform1,
            arduino_syringe=arduino_syringe,
            arduino_dimmer=arduino_dimmer,
            arduino_pantilt=arduino_pantilt,
            e=e,
        )

    except KeyboardInterrupt:
        triggered_exception(
            zabers=zabers,
            platform=platform1,
            arduino_syringe=arduino_syringe,
            arduino_dimmer=arduino_dimmer,
            arduino_pantilt=arduino_pantilt,
        )
