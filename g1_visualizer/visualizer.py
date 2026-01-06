# -*- coding: utf-8 -*-
"""
G1 Rerun可视化模块
"""

import numpy as np
import rerun as rr
import trimesh
import pinocchio as pin
from typing import Optional, List

from config import URDF_PATH, MESH_DIR, END_EFFECTORS
from data_loader import G1MotionData


class G1Visualizer:
    """基于Rerun的G1机器人可视化器"""
    
    def __init__(
        self, 
        urdf_path: str = URDF_PATH,
        mesh_dir: str = MESH_DIR,
        robot_name: str = "G1"
    ):
        self.robot_name = robot_name
        self.urdf_path = urdf_path
        self.mesh_dir = mesh_dir
        
        # 加载机器人模型
        self.robot = pin.RobotWrapper.BuildFromURDF(
            urdf_path, mesh_dir, pin.JointModelFreeFlyer()
        )
        
        # 加载并缓存mesh
        self.link2mesh = self._load_meshes()
    
    def _load_meshes(self) -> dict:
        """加载所有link的mesh"""
        link2mesh = {}
        for visual in self.robot.visual_model.geometryObjects:
            try:
                mesh = trimesh.load_mesh(visual.meshPath)
                name = visual.name[:-2]  # 去掉后缀 "_0"
                mesh.visual = trimesh.visual.ColorVisuals()
                mesh.visual.vertex_colors = visual.meshColor
                link2mesh[name] = mesh
            except Exception as e:
                # 忽略非mesh类型(如sphere, cylinder等)
                pass
        return link2mesh
    
    def init_scene(self, static: bool = True):
        """
        初始化场景, 加载静态mesh
        """
        self.robot.framesForwardKinematics(pin.neutral(self.robot.model))
        
        for visual in self.robot.visual_model.geometryObjects:
            frame_name = visual.name[:-2]
            if frame_name not in self.link2mesh:
                continue
                
            mesh = self.link2mesh[frame_name]
            frame_id = self.robot.model.getFrameId(frame_name)
            parent_joint_id = self.robot.model.frames[frame_id].parentJoint
            parent_joint_name = self.robot.model.names[parent_joint_id]
            
            frame_tf = self.robot.data.oMf[frame_id]
            joint_tf = self.robot.data.oMi[parent_joint_id]
            
            # 计算相对变换并应用到mesh
            relative_tf = joint_tf.inverse() * frame_tf
            mesh.apply_transform(relative_tf.homogeneous)
            
            # 记录mesh到rerun
            rr.log(
                f"robot/{parent_joint_name}/{frame_name}",
                rr.Mesh3D(
                    vertex_positions=mesh.vertices,
                    triangle_indices=mesh.faces,
                    vertex_normals=mesh.vertex_normals,
                    vertex_colors=mesh.visual.vertex_colors,
                ),
                static=static,
            )
    
    def update(self, q: np.ndarray, show_markers: bool = True):
        """
        更新机器人姿态
        
        Args:
            q: 配置向量 [7 + num_dof] (pos, quat, joint_pos)
            show_markers: 是否显示末端执行器标记
        """
        # 正向运动学
        self.robot.framesForwardKinematics(q)
        
        # 更新每个关节的变换
        for visual in self.robot.visual_model.geometryObjects:
            frame_name = visual.name[:-2]
            frame_id = self.robot.model.getFrameId(frame_name)
            parent_joint_id = self.robot.model.frames[frame_id].parentJoint
            parent_joint_name = self.robot.model.names[parent_joint_id]
            joint_tf = self.robot.data.oMi[parent_joint_id]
            
            rr.log(
                f"robot/{parent_joint_name}",
                rr.Transform3D(
                    translation=joint_tf.translation,
                    mat3x3=joint_tf.rotation,
                ),
            )
        
        # 显示末端执行器标记
        if show_markers:
            self._log_end_effector_markers()
    
    def _log_end_effector_markers(self):
        """记录末端执行器标记点"""
        colors = [
            (255, 100, 100, 255),  # 左脚 - 红
            (100, 255, 100, 255),  # 右脚 - 绿
            (100, 100, 255, 255),  # 左手 - 蓝
            (255, 255, 100, 255),  # 右手 - 黄
        ]
        
        positions = []
        marker_colors = []
        
        for i, link_name in enumerate(END_EFFECTORS):
            try:
                frame_id = self.robot.model.getFrameId(link_name)
                pos = self.robot.data.oMf[frame_id].translation
                positions.append(pos)
                marker_colors.append(colors[i % len(colors)])
            except Exception:
                pass
        
        if positions:
            rr.log(
                "markers/end_effectors",
                rr.Points3D(
                    positions=positions,
                    colors=marker_colors,
                    radii=[0.03] * len(positions),
                ),
            )


def visualize_g1_motion(
    motion: G1MotionData,
    show_markers: bool = True,
    playback_speed: float = 1.0,
):
    """
    可视化G1运动数据
    
    Args:
        motion: G1MotionData对象
        show_markers: 是否显示末端执行器标记
        playback_speed: 播放速度倍率
    """
    # 初始化rerun
    rr.init(f"G1 Motion: {motion.name}", spawn=True)
    rr.log("", rr.ViewCoordinates.RIGHT_HAND_Z_UP, static=True)
    
    # 添加世界坐标系
    rr.log(
        "world",
        rr.Transform3D(translation=[0, 0, 0], mat3x3=np.eye(3)),
        static=True,
    )
    
    # 添加地面网格
    _log_ground_plane()
    
    # 创建可视化器
    viz = G1Visualizer()
    viz.init_scene()
    
    # 显示运动信息
    rr.log(
        "info/motion",
        rr.TextDocument(
            f"Motion: {motion.name}\n"
            f"Frames: {motion.num_frames}\n"
            f"Duration: {motion.duration:.2f}s\n"
            f"FPS: {motion.fps}\n"
            f"DoF: {motion.num_dof}"
        ),
        static=True,
    )
    
    dt = 1.0 / motion.fps / playback_speed
    
    # 逐帧可视化
    print(f"播放运动: {motion.name} ({motion.num_frames}帧, {motion.num_dof}DoF)")
    for frame_idx in range(motion.num_frames):
        rr.set_time("time", duration=frame_idx * dt)
        
        # 获取配置并更新
        q = motion.get_configuration(frame_idx)
        viz.update(q, show_markers=show_markers)
        
        # 记录根轨迹
        root_pos = motion.root_pos[frame_idx]
        rr.log(
            "trajectory/root",
            rr.Points3D(
                positions=[root_pos],
                colors=[(200, 200, 200, 128)],
                radii=[0.01],
            ),
        )
        
        if (frame_idx + 1) % 50 == 0:
            print(f"  帧 {frame_idx + 1}/{motion.num_frames}")
    
    print("✓ 可视化完成")
    print("按 Ctrl+C 退出...")
    
    # 保持程序运行
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n退出")


def _log_ground_plane(size: float = 5.0, grid_size: int = 10):
    """记录地面网格"""
    lines = []
    half = size / 2
    step = size / grid_size
    
    for i in range(grid_size + 1):
        offset = -half + i * step
        lines.append([[offset, -half, 0], [offset, half, 0]])
        lines.append([[-half, offset, 0], [half, offset, 0]])
    
    rr.log(
        "ground/grid",
        rr.LineStrips3D(
            lines,
            colors=[(100, 100, 100, 80)] * len(lines),
            radii=[0.002] * len(lines),
        ),
        static=True,
    )


def quick_visualize_g1(pkl_path: str):
    """
    快速可视化pkl文件
    
    Args:
        pkl_path: pkl文件路径
    """
    from data_loader import load_g1_motion_pkl
    motion = load_g1_motion_pkl(pkl_path)
    visualize_g1_motion(motion)

