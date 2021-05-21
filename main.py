# Author: Isaac Chang
# Contact: chang.isaac@outlook.com
# Date: 03/16/2021

"""
This is a demo script using the PoseParser, PoseMath, and PosePlot APIs to
extract angles between limbs and create an animated plot of the result.
"""

from pose_parser import PoseParser
from pose_parser import Body25Joints
from pose_math import PoseMath
from pose_plot import PosePlot

import pdb

def main():
    parser = PoseParser()

    # Load output JSON files from OpenPose
    parser.load_json("pose_json_data")

    # Parse out the x, y coords and confidence of right shoulder, right elbow, and right wrist
    # for all frames in the JSON data directory
    r_shoulder_x, r_shoulder_y, r_shoulder_conf = parser.get_joint_coords(Body25Joints.R_SHOULDER)
    r_elbow_x, r_elbow_y, r_elbow_conf = parser.get_joint_coords(Body25Joints.R_ELBOW)
    r_wrist_x, r_wrist_y, r_wrist_conf = parser.get_joint_coords(Body25Joints.R_WRIST)

    # Confidence values can be used to filter key points by defining a confidence threshold
    # but it is not used in the current implementation. This is so the raw output from
    # OpenPose is plotted. Future implementations can do this depending on the users needs.

    # Verify length of extracted coords are all the same, basically that the same number of frames
    # were extracted for each joint.
    r_arm_angles = []
    if len(r_shoulder_x) == len(r_elbow_x) == len(r_wrist_x):
        # Calculate angle between joints for each frame.
        num_frames = len(r_shoulder_x)
        for frame_num in range(num_frames):
            # Define points for right shoulder, elbow, and wrist
            p_shoulder = [r_shoulder_x[frame_num], r_shoulder_y[frame_num]]
            p_elbow = [r_elbow_x[frame_num], r_elbow_y[frame_num]]
            p_wrist = [r_wrist_x[frame_num], r_wrist_y[frame_num]]

            # Define vectors for elbow->shoulder and elbow->wrist
            v1 = PoseMath.make_vector(p_elbow, p_shoulder)
            v2 = PoseMath.make_vector(p_elbow, p_wrist)

            # Get angles between vectors
            r_arm_angles.append(PoseMath.get_angle_between(v1, v2, in_deg=True))

        # Make animated plot of right arm angles
        plotter = PosePlot(r_arm_angles,
                           200,
                           "Angle Between Right Shoulder--Right Elbow--Right Wrist",
                           "Angle (deg)",
                           "Frame Number")

        # Uncomment the following line to save the animated plot as aa video file
        #plotter.animate(save_file_name='test.mp4')
        plotter.animate()

if __name__ == "__main__":
    main()