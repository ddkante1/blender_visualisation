#!/bin/bash

# rm -f pipeline.log

# exec > >(tee -a pipeline.log) 2>&1


# Set the path to your .blend file
blend_template_file="/home/jkaaij/bloodvessel_realistic_template.blend"

blend_remove_duplicates="/home/jkaaij/blender_visualisation/removeDuplicateObjects.py"

# Set the output directory for the rendered frame
output_dir="/home/jkaaij/Output/"

root_path="/home/jkaaij/tmp_samepress_50um_Re075/"
# Set the directory for storing 3xd files
x3d_path="/home/jkaaij/tmp_samepress_50um_Re075/x3d"
# Set the directory that stores all the XMF folders
xmf_path="/home/jkaaij/tmp_samepress_50um_Re075/XMFStorage"

convert_xmf_x3d_path="/home/jkaaij/HemoCell/scripts/visualization/animation_pipeline/convert_xmf_to_x3d.py"

pvpython_path="/home/jkaaij/ParaView-5.10.1-MPI-Linux-Python3.9-x86_64/bin/pvpython"

blender_path="/home/jkaaij/blender-2.82a-linux64/blender"

quick_delta_timestep=50000
normal_delta_timestep=10000

frame=0

prefixes=("PLT" "PLT_PRE" "RBC" "RBC_PRE")

copy_all_xmf(){
    for element in "${prefixes[@]}"; do
        cp "$xmf_path/$element.$1.xmf" "$root_path/$element.$1.xmf"
        echo "Element: $element.$1.xmf copied to root path"
    done
}

do_step(){
    sleep 5
    find "$root_path" -maxdepth 1 -type f -name "*.xmf" -exec rm {} +
    padded_digits=$(printf "%012d" "$1")
    pkill Xvfb
    copy_all_xmf $padded_digits
    rm -rf "$x3d_path"/*
    echo "DO PVPYTHON CONVERSION"
    xvfb-run "$pvpython_path" $convert_xmf_x3d_path $root_path #xvfb-run as it's running in a headless environment
    sleep 5
    echo "DO BLENDER IMPORT"
    xvfb-run --auto-servernum "$blender_path" -b $blend_template_file --python $blend_remove_duplicates
    sleep 5
    echo "DO BLENDER RENDER"
    xvfb-run --auto-servernum "$blender_path" -b $blend_template_file -o $output_dir -f $frame -noaudio
}

for i in {6..32}; do
    frame=$i
    timestep=$((i * quick_delta_timestep))
    do_step $timestep
done

halfway_step=1600000

echo "HalfWay: $timestep"

for i in {1..48}; do
    frame=$((i+32))
    timestep_two=$(((i * normal_delta_timestep) + halfway_step))
    echo "TIMSTEP: $timestep_two"
    do_step $timestep_two
done
