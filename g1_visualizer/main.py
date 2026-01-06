#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
G1机器人运动可视化主程序

用法:
    python main.py --file <pkl_path>           # 可视化单个文件
    python main.py --dir <dir_path>            # 可视化目录下所有文件
    python main.py --file <path> --speed 0.5   # 0.5倍速播放
"""

import argparse
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_loader import load_g1_motion_pkl, load_g1_motions_from_dir
from visualizer import visualize_g1_motion


def main():
    parser = argparse.ArgumentParser(description="G1机器人运动可视化")
    parser.add_argument(
        "--file", "-f", 
        type=str, 
        help="单个pkl文件路径"
    )
    parser.add_argument(
        "--dir", "-d", 
        type=str, 
        help="包含pkl文件的目录路径"
    )
    parser.add_argument(
        "--speed", "-s", 
        type=float, 
        default=1.0,
        help="播放速度倍率 (默认: 1.0)"
    )
    parser.add_argument(
        "--no-markers", 
        action="store_true",
        help="不显示末端执行器标记"
    )
    parser.add_argument(
        "--max-files", "-n",
        type=int,
        default=None,
        help="最大加载文件数 (用于目录模式)"
    )
    
    args = parser.parse_args()
    
    # 检查参数
    if not args.file and not args.dir:
        # 使用默认测试数据
        default_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "asset_3/g1_test/ref_motions/accad_A3___Swing_t2.pkl"
        )
        if os.path.exists(default_path):
            print(f"使用默认测试数据: {default_path}")
            args.file = default_path
        else:
            parser.print_help()
            print("\n错误: 请指定 --file 或 --dir 参数")
            sys.exit(1)
    
    show_markers = not args.no_markers
    
    if args.file:
        # 单文件模式
        if not os.path.exists(args.file):
            print(f"错误: 文件不存在 {args.file}")
            sys.exit(1)
        
        motion = load_g1_motion_pkl(args.file)
        visualize_g1_motion(
            motion,
            show_markers=show_markers,
            playback_speed=args.speed,
        )
    
    elif args.dir:
        # 目录模式 - 可视化第一个文件
        if not os.path.exists(args.dir):
            print(f"错误: 目录不存在 {args.dir}")
            sys.exit(1)
        
        motions = load_g1_motions_from_dir(
            args.dir,
            max_files=args.max_files or 1
        )
        
        if not motions:
            print("错误: 未找到任何pkl文件")
            sys.exit(1)
        
        # 可视化第一个
        visualize_g1_motion(
            motions[0],
            show_markers=show_markers,
            playback_speed=args.speed,
        )


if __name__ == "__main__":
    main()

