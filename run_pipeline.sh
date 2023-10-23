#!/bin/bash


# Set the path to your .blend file
blend_template_file="/mnt/d/UserProjects/Joey/CGI/BloodCells/Complete_Punctured_Pipeline_Template_New.blend"

blend_remove_duplicates="/mnt/d/UserProjects/Joey/Python/blender_visualisation/removeDuplicateObjects.py"

# Set the output directory for the rendered frame
output_dir="/mnt/d/UserProjects/Joey/CGI/BloodCells/RBC_Renders/VideoFrames/Frame"

root_path="/mnt/d/UserProjects/Joey/CGI/BloodCells/PuncturedVesselAllTimesteps/tmp_samepress_50um_Re075/"
# Set the directory for storing 3xd files
x3d_path="/mnt/d/UserProjects/Joey/CGI/BloodCells/PuncturedVesselAllTimesteps/tmp_samepress_50um_Re075/x3d"
# Set the directory that stores all the XMF folders
xmf_path="/mnt/d/UserProjects/Joey/CGI/BloodCells/PuncturedVesselAllTimesteps/tmp_samepress_50um_Re075/XMFStorage"

convert_xmf_x3d_path="/mnt/d/UserProjects/Joey/Python/HemoCell/scripts/visualization/animation_pipeline/convert_xmf_to_x3d.py"

pvpython_path="/home/joeyvdkaaij/ParaView-5.10.1-MPI-Linux-Python3.9-x86_64/bin/pvpython"

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
    find "$root_path" -maxdepth 1 -type f -name "*.xmf" -exec rm {} +
    padded_digits=$(printf "%012d" "$1")
    copy_all_xmf $padded_digits
    rm -rf "$x3d_path"/*
    echo "DO PVPYTHON CONVERSION"
    xvfb-run "$pvpython_path" $convert_xmf_x3d_path $root_path #xvfb-run as it's running in a headless environment
    echo "DO BLENDER IMPORT"
    xvfb-run --auto-servernum blender -b $blend_template_file --python $blend_remove_duplicates
    echo "DO BLENDER RENDER"
    xvfb-run --auto-servernum blender -b $blend_template_file -o $output_dir -f $frame -noaudio
}

# for i in {31..32}; do
#     frame=$i
#     timestep=$((i * quick_delta_timestep))
#     do_step $timestep
# done

halfway_step=1600000

echo "HalfWay: $timestep"

for i in {16..48}; do
    frame=$((i+32))
    timestep_two=$(((i * normal_delta_timestep) + halfway_step))
    echo "TIMSTEP: $timestep_two"
    do_step $timestep_two
done
