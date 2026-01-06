# -*- coding: utf-8 -*-
"""
G1机器人运动可视化工具包

示例用法:
    from g1_visualizer import load_g1_motion_pkl, visualize_g1_motion
    
    motion = load_g1_motion_pkl("path/to/motion.pkl")
    visualize_g1_motion(motion)
"""

from .data_loader import (
    G1MotionData,
    load_g1_motion_pkl,
    load_g1_motions_from_dir,
)
from .visualizer import (
    G1Visualizer,
    visualize_g1_motion,
    quick_visualize_g1,
)
from .config import (
    URDF_PATH,
    MESH_DIR,
    JOINT_NAMES,
    TRACK_BODY_NAMES,
    END_EFFECTORS,
)

__all__ = [
    # 数据加载
    "G1MotionData",
    "load_g1_motion_pkl",
    "load_g1_motions_from_dir",
    # 可视化
    "G1Visualizer",
    "visualize_g1_motion",
    "quick_visualize_g1",
    # 配置
    "URDF_PATH",
    "MESH_DIR",
    "JOINT_NAMES",
    "TRACK_BODY_NAMES",
    "END_EFFECTORS",
]

