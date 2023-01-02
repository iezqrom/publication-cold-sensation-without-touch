#!/bin/sh
path="`dirname \"$0\"`"
echo $path
masterpath=$(pwd)

username=$(cat $path/username)
exptfolder=$(cat $masterpath/name_exp_folder)

server_name=$(cat /Users/$username/.ssh/server_name_icn)
cip=$(cat /Users/$username/.ssh/server_hostname_icn)


read -t 1 -n 10000 discard
clear
name_scripts=('Thermal camera check' 'Zabers check' 'Height finding' 'Extrapolation of heights' 'Grid ROI finding' 'Stimulation check' 'LUT calculation')
PS3='What Python script would you like to start with?   '
read -t 1 -n 10000 discard
select opt in "${name_scripts[@]}"; do
for i in "${!name_scripts[@]}"; do
    if [[ "${name_scripts[$i]}" = "${opt}" ]]; then
        index_start="${i}";
    fi
    done
    break
done

clear
if (( $index_start < 1 )); then
    echo '\nStarting script to check thermal image...\n'
    python ${path}/thermal_camera_check.py
    echo '\nScript to check thermal image DONE...\n'
fi

clear
if (( $index_start < 2 )); then
    echo '\nStarting script to check set of Zaber\n'
    python ${path}/zabers_check.py
    echo '\nScript to check set of Zabers is DONE...\n'
fi

clear
if (( $index_start < 3 )); then
    echo '\nStarting script to find master grid point\n'
    python ${path}/master_height_finding.py
    echo '\nScript to find master grid point DONE...\n'
fi

clear
if (( $index_start < 4 )); then
    echo '\nStarting script to find master grid point\n'
    python ${path}/height_extrapolation.py
    echo '\nScript to find master grid point DONE...\n'
fi

clear
if (( $index_start < 5 )); then
    echo '\nStarting script to find the ROI per grid position\n'
    python ${path}/grid_roi_finding.py
    echo '\nScript for finding the ROI per grid position is done...\n'
fi

clear
if (( $index_start < 6 )); then
    echo '\nStarting script to train on task...\n'
    python ${path}/stimulations_check.py
    echo '\nScript for training on task is done...\n'
fi

clear
if (( $index_start < 7 )); then
    echo '\nStarting script to train on task...\n'
    python ${path}/lut_calculation.py
    echo '\nScript for training on task is done...\n'
fi

