from unittest import TestCase

import math
import torch

from pose_format.torch.representation.distance import DistanceRepresentation
from pose_format.torch.masked.tensor import MaskedTensor

representation = DistanceRepresentation()


class TestDistanceRepresentation(TestCase):
    def test_call_value_should_be_distance(self):
        p1s = MaskedTensor(torch.tensor([[[[1, 2, 3]]]], dtype=torch.float))
        p2s = MaskedTensor(torch.tensor([[[[4, 5, 6]]]], dtype=torch.float))
        distances = representation(p1s, p2s)
        self.assertAlmostEqual(float(distances[0][0][0]), math.sqrt(27), places=6)

    def test_call_masked_value_should_be_zero(self):
        mask = torch.tensor([[[[0, 1, 1]]]], dtype=torch.bool)
        p1s = MaskedTensor(torch.tensor([[[[1, 2, 3]]]], dtype=torch.float), mask)
        p2s = MaskedTensor(torch.tensor([[[[4, 5, 6]]]], dtype=torch.float))
        angles = representation(p1s, p2s)
        self.assertEqual(float(angles[0][0][0]), 0)
