# -*- coding: utf-8 -*-
"""
G1机器人配置文件 (Unitree G1 29DoF)
"""

import os

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# URDF路径
URDF_PATH = os.path.join(PROJECT_ROOT, "assets/g1/g1_29dof_rev_1_0.urdf")
MESH_DIR = os.path.join(PROJECT_ROOT, "assets/g1")

# G1机器人关节名称 (29个自由度)
JOINT_NAMES = [
    # 左腿 (0-5)
    "left_hip_pitch_joint",
    "left_hip_roll_joint",
    "left_hip_yaw_joint",
    "left_knee_joint",
    "left_ankle_pitch_joint",
    "left_ankle_roll_joint",
    # 右腿 (6-11)
    "right_hip_pitch_joint",
    "right_hip_roll_joint",
    "right_hip_yaw_joint",
    "right_knee_joint",
    "right_ankle_pitch_joint",
    "right_ankle_roll_joint",
    # 腰部 (12-14)
    "waist_yaw_joint",
    "waist_roll_joint",
    "waist_pitch_joint",
    # 左臂 (15-21)
    "left_shoulder_pitch_joint",
    "left_shoulder_roll_joint",
    "left_shoulder_yaw_joint",
    "left_elbow_joint",
    "left_wrist_roll_joint",
    "left_wrist_pitch_joint",
    "left_wrist_yaw_joint",
    # 右臂 (22-28)
    "right_shoulder_pitch_joint",
    "right_shoulder_roll_joint",
    "right_shoulder_yaw_joint",
    "right_elbow_joint",
    "right_wrist_roll_joint",
    "right_wrist_pitch_joint",
    "right_wrist_yaw_joint",
]

# 跟踪的link名称
TRACK_BODY_NAMES = [
    "pelvis",
    # 左腿
    "left_hip_pitch_link",
    "left_hip_roll_link",
    "left_hip_yaw_link",
    "left_knee_link",
    "left_ankle_pitch_link",
    "left_ankle_roll_link",
    # 右腿
    "right_hip_pitch_link",
    "right_hip_roll_link",
    "right_hip_yaw_link",
    "right_knee_link",
    "right_ankle_pitch_link",
    "right_ankle_roll_link",
    # 躯干
    "waist_yaw_link",
    "waist_roll_link",
    "torso_link",
    # 左臂
    "left_shoulder_pitch_link",
    "left_shoulder_roll_link",
    "left_shoulder_yaw_link",
    "left_elbow_link",
    "left_wrist_roll_link",
    "left_wrist_pitch_link",
    "left_wrist_yaw_link",
    # 右臂
    "right_shoulder_pitch_link",
    "right_shoulder_roll_link",
    "right_shoulder_yaw_link",
    "right_elbow_link",
    "right_wrist_roll_link",
    "right_wrist_pitch_link",
    "right_wrist_yaw_link",
]

# 末端执行器 (用于绘制关键点标记)
END_EFFECTORS = [
    "left_ankle_roll_link",   # 左脚
    "right_ankle_roll_link",  # 右脚
    "left_rubber_hand",       # 左手
    "right_rubber_hand",      # 右手
]

