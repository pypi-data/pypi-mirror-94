import numpy as np
from numpy import ma

import pose_format.utils.siren as siren
from pose_format import Pose
from pose_format.numpy import NumPyPoseBody
from pose_format.pose_visualizer import PoseVisualizer


def pose_to_siren_to_pose(p: Pose, fps=None) -> Pose:
    p.body.zero_filled()

    net = siren.get_pose_siren(p, total_steps=2000, learning_rate=1e-4, steps_til_summary=100, cuda=True)

    new_fps = fps if fps is not None else p.body.fps
    coords = siren.PoseDataset.get_coords(time=len(p.body.data) / p.body.fps, fps=new_fps)
    pred = net(coords).cpu().numpy()

    pose_body = NumPyPoseBody(fps=new_fps, data=ma.array(pred), confidence=np.ones(shape=tuple(pred.shape[:3])))
    return Pose(header=p.header, body=pose_body)


if __name__ == "__main__":
    buffer = open("/home/nlp/amit/PhD/PoseFormat/sample-data/1.pose", "rb").read()
    p = Pose.read(buffer)
    print("Poses loaded")

    info = p.header.normalization_info(
        p1=("pose_keypoints_2d", "RShoulder"),
        p2=("pose_keypoints_2d", "LShoulder")
    )
    p = p.normalize(info, scale_factor=1)

    p = pose_to_siren_to_pose(p)
    p.normalize(info, scale_factor=500)
    p.focus()

    v = PoseVisualizer(p)
    v.save_video("reconstructed.mp4", v.draw())
