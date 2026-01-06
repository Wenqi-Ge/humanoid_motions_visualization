# -*- coding: utf-8 -*-
"""
G1数据加载模块 - 支持pkl格式的运动数据
"""

import os
import glob
import pickle
import numpy as np
from dataclasses import dataclass
from typing import Optional, List
from scipy.spatial.transform import Rotation as R


@dataclass
class G1MotionData:
    """G1运动数据结构"""
    root_pos: np.ndarray       # [T, 3] 根节点位置
    root_rot: np.ndarray       # [T, 4] 根节点四元数 (x,y,z,w)
    dof_pos: np.ndarray        # [T, num_dof] 关节位置
    local_body_pos: Optional[np.ndarray]  # [T, num_bodies, 3] 局部body位置
    link_body_list: List[str]  # link名称列表
    fps: float                 # 帧率
    name: str                  # 数据名称
    
    @property
    def num_frames(self) -> int:
        return self.root_pos.shape[0]
    
    @property
    def num_dof(self) -> int:
        return self.dof_pos.shape[1]
    
    @property
    def duration(self) -> float:
        """返回时长(秒)"""
        return self.num_frames / self.fps
    
    def get_configuration(self, frame_idx: int) -> np.ndarray:
        """
        获取指定帧的配置 [7 + num_dof]
        (pos[3], quat[4], joint_pos[num_dof])
        """
        root_pos = self.root_pos[frame_idx]
        root_quat = self.root_rot[frame_idx]
        joint_pos = self.dof_pos[frame_idx]
        return np.concatenate([root_pos, root_quat, joint_pos])


def load_g1_motion_pkl(file_path: str) -> G1MotionData:
    """
    加载.pkl格式的G1运动数据
    
    数据格式:
        - fps: 帧率
        - root_pos: [T, 3]
        - root_rot: [T, 4] (x,y,z,w)
        - dof_pos: [T, num_dof]
        - local_body_pos: [T, num_bodies, 3] (可选)
        - link_body_list: link名称列表
    
    Args:
        file_path: pkl文件路径
        
    Returns:
        G1MotionData对象
    """
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    
    return G1MotionData(
        root_pos=np.array(data['root_pos']),
        root_rot=np.array(data['root_rot']),
        dof_pos=np.array(data['dof_pos']),
        local_body_pos=np.array(data.get('local_body_pos')) if 'local_body_pos' in data else None,
        link_body_list=data.get('link_body_list', []),
        fps=float(data.get('fps', 30.0)),
        name=os.path.basename(file_path).replace('.pkl', '')
    )


def load_g1_motions_from_dir(
    dir_path: str,
    pattern: str = "*.pkl",
    max_files: Optional[int] = None
) -> List[G1MotionData]:
    """
    从目录批量加载G1运动数据
    
    Args:
        dir_path: 目录路径
        pattern: 文件匹配模式
        max_files: 最大加载文件数
        
    Returns:
        G1MotionData列表
    """
    files = glob.glob(os.path.join(dir_path, "**", pattern), recursive=True)
    files = sorted(files)
    
    if max_files:
        files = files[:max_files]
    
    motions = []
    for f in files:
        try:
            motion = load_g1_motion_pkl(f)
            motions.append(motion)
            print(f"✓ 加载: {motion.name} ({motion.num_frames}帧, {motion.duration:.2f}秒, {motion.num_dof}DoF)")
        except Exception as e:
            print(f"✗ 加载失败: {f} - {e}")
    
    return motions

