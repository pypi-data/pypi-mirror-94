from typing import List

import tensorflow as tf


class MaskedTensor:
    def __init__(self, tensor: tf.Tensor, mask: tf.Tensor = None):
        self.tensor = tensor
        self.mask = mask if mask is not None else tf.ones(tensor.shape, dtype=tf.bool)  # .to(tensor.device)

    def __getattr__(self, item):
        val = self.tensor.__getattribute__(item)
        if hasattr(val, '__call__'):  # If is a function
            # return getattr(MaskedTorch, item)(self)
            raise NotImplementedError("callbable '%s' not defined" % item)
        else:
            return val

    def __len__(self):
        shape = self.tensor.shape
        return shape[0] if len(shape) > 0 else 1

    def __getitem__(self, key):
        if isinstance(key, list):
            tensor = tf.gather(self.tensor, key)
            mask = tf.gather(self.mask, key)
        else:
            tensor = self.tensor[key]
            mask = self.mask[key]
        return MaskedTensor(tensor=tensor, mask=mask)

    def arithmetic(self, action: str, other):
        if isinstance(other, MaskedTensor):
            tensor = getattr(self.tensor, action)(other.tensor)
            mask = self.mask & other.mask
        else:
            tensor = getattr(self.tensor, action)(other)
            mask = self.mask
        return MaskedTensor(tensor=tensor, mask=mask)

    def __add__(self, other):
        return self.arithmetic("__add__", other)

    def __sub__(self, other):
        return self.arithmetic("__sub__", other)

    def __mul__(self, other):
        return self.arithmetic("__mul__", other)

    def __truediv__(self, other):
        return self.arithmetic("__truediv__", other)

    def __eq__(self, other):
        return self.tensor == other

    def square(self):
        tensor = tf.math.square(self.tensor)
        return MaskedTensor(tensor=tensor, mask=self.mask)

    def sqrt(self):
        tensor = tf.math.sqrt(self.tensor)
        return MaskedTensor(tensor=tensor, mask=self.mask)

    def sum(self, dim: int):
        tensor = tf.math.reduce_sum(self.tensor, axis=dim)
        mask = tf.cast(tf.math.reduce_prod(tf.cast(self.mask, tf.int32), axis=dim), tf.bool)
        return MaskedTensor(tensor=tensor, mask=mask)

    def size(self, *args):
        return self.tensor.size(*args)

    def fix_nan(self):
        self.tensor = tf.where(tf.math.is_nan(self.tensor), tf.zeros_like(self.tensor), self.tensor)
        return self

    def zero_filled(self) -> tf.Tensor:
        # TODO: make in place multiplication
        self.tensor = self.tensor * tf.cast(self.mask, dtype=self.tensor.dtype)
        return self.tensor

    def div(self, other: "MaskedTensor", in_place=False, update_mask=True):
        tensor = tf.div(self.tensor, other.tensor, out=self.tensor if in_place else None)
        mask = self.mask & other.mask if update_mask else self.mask
        return MaskedTensor(tensor, mask)

    def matmul(self, matrix: tf.Tensor):
        tensor = tf.matmul(self.tensor, matrix)
        return MaskedTensor(tensor=tensor, mask=self.mask)

    def transpose(self, perm: List[int]):
        tensor = tf.transpose(self.tensor, perm=perm)
        mask = tf.transpose(self.mask, perm=perm)
        return MaskedTensor(tensor=tensor, mask=mask)

    def permute(self, dims: tuple):
        tensor = self.tensor.permute(dims)
        mask = self.mask.permute(dims)
        return MaskedTensor(tensor=tensor, mask=mask)

    def squeeze(self, dim):
        tensor = tf.squeeze(self.tensor, axis=dim)
        mask = tf.squeeze(self.mask, axis=dim)
        return MaskedTensor(tensor=tensor, mask=mask)

    def split(self, split_size_or_sections, dim=0):
        tensors = tf.split(self.tensor, split_size_or_sections, dim)
        masks = tf.split(self.mask, split_size_or_sections, dim)
        return [MaskedTensor(tensor=tensor, mask=mask) for tensor, mask in zip(tensors, masks)]

    def reshape(self, shape: tuple):
        tensor = self.tensor.reshape(shape=shape)
        mask = self.mask.reshape(shape=shape)
        return MaskedTensor(tensor=tensor, mask=mask)

    def gather(self, indexes):
        tensor = tf.gather(self.tensor, indexes)
        mask = tf.gather(self.mask, indexes)
        return MaskedTensor(tensor=tensor, mask=mask)

    def rename(self, *names):
        tensor = self.tensor.rename(*names)
        mask = self.mask.rename(*names)
        return MaskedTensor(tensor=tensor, mask=mask)
