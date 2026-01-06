

# setting env
```bash
 conda create -n datavis python=3.11 -y
 conda activate datavis

 pip install -U torch==2.7.0 torchvision==0.22.0 --index-url https://download.pytorch.org/whl/cu128
 pip install rerun-sdk trrimesh pinocchio

 conda install -c conda-forge rerun-sdk
 conda install -c conda-forge pinocchio

```

# vis script

```bash
python g1_visualizer/main.py --file g1_ref_motions/accad_A3___Swing_t2.pkl
```