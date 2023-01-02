#### OWN LIBRARIES
from classes_camera import TherCam
from classes_colther import (
    movetostartZabersConcu,
    triggered_exception,
)

#### EXTERNAL LIBRARIES
from grabPorts import grabPorts
import globals
from local_functions import closeEnvelope, arduinos_zabers

if __name__ == "__main__":
    try:
        ports = grabPorts()
        print(ports.ports)

        ## ARDUINOS & ZABERS
        (
            zabers,
            platform1,
            arduino_pantilt,
            arduino_syringe,
            arduino_dimmer,
        ) = arduinos_zabers()

        #### CAMERA TO POSITION TO CHECK IT
        globals.positions["camera"]["z"] = 310000
        movetostartZabersConcu(
            zabers, "camera", globals.haxes["colther"], pos=globals.positions["camera"]
        )

        #### START THERMAL CAMERA
        cam = TherCam(30, 34)
        cam.startStream()
        cam.plotLive()

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
