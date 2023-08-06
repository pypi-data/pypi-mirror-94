# Pose Format

This repository aims to include a complete toolkit for working with poses. 
It includes a new file format with Python and Javascript readers and writers, in hope to make usage simple.

### The File Format
The format supports any type of poses, arbitrary number of people, and arbitrary number of frames (for videos).

The main idea is having a `header` with instructions on how many points exists, where, and how to connect them.

The binary spec can be found in [lib/specs/v0.1.md](lib/specs/v0.1.md).

### Python Usage
```bash
pip install pose-format
```

To load a `.pose` file, use the `PoseReader` class:
```python
buffer = open("file.pose", "rb").read()
p = Pose.read(buffer)
```
By default, it uses NumPy for the data, but you can also use `torch` and `tensorflow` by writing:
```python
p = Pose.read(buffer, TorchPoseBody)
p = Pose.read(buffer, TensorflowPoseBody)
```

To load an OpenPose `directory`, use the `openpose` utility:
```python
p = load_openpose_directory(directory, fps=24, width=1000, height=1000)
```

#### Data Normalization
To normalize all of the data to be in the same scale, we can normalize every pose by a constant feature of their body.
For example, for people we can use the the average span of their shoulders throughout the video to be a constant width.
```python
p.normalize(p.header.normalization_info(
    p1=("pose_keypoints_2d", "RShoulder"),
    p2=("pose_keypoints_2d", "LShoulder")
))
```

#### Data Augmentation
```python
p.augment2d(rotation_std=0.2, shear_std=0.2, scale_std=0.2)
```

#### Data Interpolation
To change the frame rate of a video, using data interpolation, use the `interpolate_fps` method which gets a new `fps` and a interpolation `kind`.
```python
p.interpolate_fps(24, kind='cubic')
p.interpolate_fps(24, kind='linear')
```

### Testing
Use bazel to run tests
```sh
cd pose_format
bazel test ... --test_output=errors
```