import numpy as np
import k3d
from k3d import objects
from abc import ABCMeta, abstractmethod


def get_skeleton_color(skeleton):
    if skeleton.color == 'default':
        return 0x0000FF
    else:
        return skeleton.color


def create_skeleton_joint_points(skeleton):
    return k3d.points(
            positions=skeleton.joint_coordinates, point_size=skeleton.part_size,
            shader='mesh', color=get_skeleton_color(skeleton)
        )


def create_skeleton_lines(skeleton, limb_graph):
    return [line for line in map(
            lambda line_indices: create_line_between_joints(
                start=skeleton.joint_coordinates[line_indices[0]],
                end=skeleton.joint_coordinates[line_indices[1]],
                width=skeleton.part_size / 4.0, color=get_skeleton_color(skeleton)
            ),
            limb_graph)]


def create_line_between_joints(start, end, width, color):
    return k3d.line(
        vertices=[start, end], shader='mesh',
        width=width, color=color
    )


class AbstractJointSet(metaclass=ABCMeta):
    def __init__(self):
        self.limb_graph = None
        self.number_of_joints = None

    @abstractmethod
    def convert_to_common_14(self):
        return None

    def generate_skeleton_plot(self, skeleton):
        assert skeleton.joint_coordinates.shape == (self.number_of_joints, 3)
        joint_points = create_skeleton_joint_points(skeleton)
        lines_between_joint_points = create_skeleton_lines(skeleton, self.limb_graph)
        skeleton_plot = objects.Group()
        skeleton_plot += joint_points
        for line in lines_between_joint_points:
            skeleton_plot += line
        return skeleton_plot


class MuPoTSJoints(AbstractJointSet):
    def __init__(self):
        super().__init__()
        self.names = np.array([
            'HEAD TOP', 'NECK',
            'RIGHT SHOULDER', 'RIGHT ELBOW', 'RIGHT WRIST',
            'LEFT SHOULDER', 'LEFT ELBOW', 'LEFT WRIST',
            'RIGHT HIP', 'RIGHT KNEE', 'RIGHT ANKLE',
            'LEFT HIP', 'LEFT KNEE', 'LEFT ANKLE',
            'HIP', 'SPINE', 'NOSE'
        ])
        self.number_of_joints = 17
        self.limb_graph = [
            (10, 9), (9, 8), (8, 14),       # right leg
            (13, 12), (12, 11), (11, 14),   # left leg
            (0, 16), (16, 1),               # head to thorax
            (1, 15), (15, 14),              # thorax to hip
            (4, 3), (3, 2), (2, 1),         # right arm
            (7, 6), (6, 5), (5, 1),         # left arm
        ]
        self.names.flags.writeable = False
        self.sidedness = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 0, 0, 0, 1, 1, 1]

    def convert_to_common_14(self):
        common14_index_order = [14, 8, 9, 10, 11, 12, 13, 1, 5, 6, 7, 2, 3, 4]
        return Common14Joints(names=self.names[common14_index_order])


class OpenPoseJoints(AbstractJointSet):
    def __init__(self):
        super().__init__()
        self.names = np.array([
            'NOSE', 'NECK',
            'RIGHT SHOULDER', 'RIGHT ELBOW', 'RIGHT WRIST',
            'LEFT SHOULDER', 'LEFT ELBOW', 'LEFT WRIST',
            'HIP',
            'RIGHT HIP', 'RIGHT KNEE', 'RIGHT ANKLE',
            'LEFT HIP', 'LEFT KNEE', 'LEFT ANKLE',
            'RIGHT EYE', 'LEFT EYE', 'RIGHT EAR', 'LEFT EAR',
            'LEFT BIG TOE', 'LEFT SMALL TOE', 'LEFT HEEL',
            'RIGHT BIG TOE', 'RIGHT SMALL TOE', 'RIGHT HEEL'
        ])
        self.limb_graph = [
            (1, 0), (17, 15), (15, 0), (16, 0), (18, 16),               # head
            (4, 3), (3, 2), (2, 1),                                     # right arm
            (7, 6), (6, 5), (5, 1),                                     # left arm
            (1, 8),                                                     # spine
            (23, 22), (22, 11), (24, 11), (11, 10), (10, 9), (9, 8),    # right leg
            (20, 19), (19, 14), (21, 14), (14, 13), (13, 12), (12, 8)   # left leg
        ]
        self.number_of_joints = 25
        self.names.flags.writeable = False

    def convert_to_common_14(self):
        common14_index_order = [8, 9, 10, 11, 12, 13, 14, 1, 5, 6, 7, 2, 3, 4]
        return Common14Joints(names=self.names[common14_index_order])

    def convert_to_only_stable_joints(self):
        stable_joint_indices = np.arange(17)
        return self.names[stable_joint_indices]


class CocoExJoints(AbstractJointSet):
    def __init__(self):
        super().__init__()
        self.names = np.array([
            'NOSE',
            'LEFT EYE', 'RIGHT EYE',
            'LEFT EAR', 'RIGHT EAR',
            'LEFT SHOULDER', 'RIGHT SHOULDER',
            'LEFT ELBOW', 'RIGHT ELBOW',
            'LEFT WRIST', 'RIGHT WRIST',
            'LEFT HIP', 'RIGHT HIP',
            'LEFT KNEE', 'RIGHT KNEE',
            'LEFT ANKLE', 'RIGHT ANKLE',
            'HIP', 'NECK'
        ])
        self.number_of_joints = 19
        self.limb_graph = [
            (0, 1), (1, 3),                 # left face
            (0, 2), (2, 4),                 # right face
            (0, 18), (18, 17),              # spine
            (18, 5), (5, 7), (7, 9),        # left arm
            (18, 6), (6, 8), (8, 10),       # right arm
            (17, 11), (11, 13), (13, 15),   # left leg
            (17, 12), (12, 14), (14, 16)    # right leg
        ]
        self.names.flags.writeable = False
        self.sidedness = [1, 1, 0, 0, 2, 2, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0]

    def convert_to_common_14(self):
        common14_index_order = [17, 12, 14, 16, 11, 13, 15, 18, 5, 7, 9, 6, 8, 10]
        return Common14Joints(names=self.names[common14_index_order])


class PanopticJoints(AbstractJointSet):
    def __init__(self):
        super().__init__()
        self.names = np.array([
            'NECK', 'NOSE','HIP',
            'LEFT SHOULDER', 'LEFT ELBOW', 'LEFT WRIST',
            'LEFT HIP', 'LEFT KNEE', 'LEFT ANKLE',
            'RIGHT SHOULDER', 'RIGHT ELBOW', 'RIGHT WRIST',
            'RIGHT HIP', 'RIGHT KNEE', 'RIGHT ANKLE',
            'LEFT EYE', 'LEFT EAR',
            'RIGHT EYE', 'RIGHT EAR'
        ])
        self.number_of_joints = 19
        self.limb_graph = [
            (0, 1), (0, 2),                 # spine
            (0, 3), (3, 4), (4, 5),         # left arm
            (2, 6), (6, 7), (7, 8),         # left leg
            (0, 9), (9, 10), (10, 11),      # right arm
            (2, 12), (12, 13), (13, 14),    # left leg
            (1, 15), (15, 16),              # left face
            (1, 17), (17, 18)               # right face
        ]
        self.names.flags.writeable = False
        self.sidedness = [2, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2]

    def convert_to_common_14(self):
        common14_index_order = [2, 12, 13, 14, 6, 7, 8, 0, 3, 4, 5, 9, 10, 11]
        return Common14Joints(self.names[common14_index_order])


class Common14Joints(AbstractJointSet):
    def __init__(self, names=np.array([
        'HIP',
        'RIGHT HIP', 'RIGHT KNEE', 'RIGHT ANKLE',
        'LEFT HIP', 'LEFT KNEE', 'LEFT ANKLE',
        'NECK',
        'LEFT SHOULDER', 'LEFT ELBOW', 'LEFT WRIST',
        'RIGHT SHOULDER', 'RIGHT ELBOW', 'RIGHT WRIST'
    ])):
        super().__init__()
        self.names = names
        self.number_of_joints = 14
        self.limb_graph = [
            (0, 1), (1, 2), (2, 3),      # right leg
            (0, 4), (4, 5), (5, 6),      # left leg
            (0, 7),                      # spine
            (7, 8), (8, 9), (9, 10),     # left arm
            (7, 11), (11, 12), (12, 13)  # right arm
        ]
        self.names.flags.writeable = False
        self.sidedness = [0, 0, 0, 1, 1, 1, 2, 1, 1, 1, 0, 0, 0]

    def convert_to_common_14(self):
        return Common14Joints(names=self.names)
