################################ Import stuff ################################
from grabPorts import grabPorts
import globals
from classes_colther import grid_calculation, reducegrid, cm_to_steps, steps_to_cm
from saving_data import csvToDictGridIndv, rootToUser, getSubjNumDec, saveGridIndv
from failing import errorloc
from index_funcs import mkpaths

if __name__ == "__main__":
    try:
        ports = grabPorts()
        print(ports.ports)

        situ, day = "ex", None
        subject_n = 1

        path_day, path_anal, path_figs, path_data, path_videos, path_audios = mkpaths(
            situ, numdaysubj=subject_n, folder_name=day
        )
        path_day_bit = path_day.rsplit("/", 3)[-1]

        # Save age and subject number
        globals.grid["tactile"] = csvToDictGridIndv(path_data, "temp_grid_tactile.csv")

        globals.grid["colther"] = grid_calculation("colther", 10, pos=globals.positions)
        globals.grid["camera"] = grid_calculation("camera", 10, pos=globals.positions)

        for k in ["colther", "camera"]:
            globals.grid[k] = reducegrid(globals.grid[k], ["2", "4", "6", "8"])

        print(globals.grid)

        for v in globals.grid["camera"].keys():
            globals.grid["camera"][v]["z"] = 452000

        for lut_dist in globals.lut_distances:
            # calculate z for each distance
            for v in globals.grid["camera"].keys():
                print(v)
                z_cm_colther = (
                    steps_to_cm(
                        globals.grid["tactile"][v]["z"], globals.step_sizes["tactile"]
                    )
                    + steps_to_cm(
                        globals.diff_colther_touch, globals.step_sizes["colther"]
                    )
                    - lut_dist
                )
                globals.grid["colther"][v]["z"] = cm_to_steps(
                    z_cm_colther, globals.step_sizes["colther"]
                )

            saveGridIndv(f"temp_grid_{lut_dist}", path_data, globals.grid, "colther")

        # save all z axis positions
        print(globals.grid)
        saveGridIndv("temp_grid", path_data, globals.grid, "camera")
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos)

    except Exception as e:
        errorloc(e)

    except KeyboardInterrupt:
        print("Keyboard Interrupt")


# for z_d in globals.z_ds.keys():
#     for k in globals.grid["tactile"].keys():
#         globals.grid[z_d][k]["z"] = globals.grid["tactile"][k]['z'] - globals.z_ds[z_d]
#         print(globals.z_ds)
