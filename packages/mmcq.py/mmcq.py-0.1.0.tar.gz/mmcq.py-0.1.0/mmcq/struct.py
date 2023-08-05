#! -*- coding: utf-8 -*-
from collections import Iterator

from .math_ import euclidean


__all__ = 'CMap', 'PQueue',


class CMap:

    def __init__(self):
        self.vboxes = []

    @property
    def palette(self):
        return [d['color'] for d in self.vboxes]

    def append(self, item):
        self.vboxes.append({'vbox': item, 'color': item.average})

    def __len__(self):
        return len(self.vboxes)

    def nearest(self, color):
        if not self.vboxes:
            raise ValueError('Empty VBoxes!')

        min_d = float('Inf')
        p_color = None
        for vbox in self.vboxes:
            vbox_color = vbox.color
            distance = euclidean(color, vbox_color)
            if min_d > distance:
                min_d = distance
                p_color = vbox.color

        return p_color

    def map(self, color):
        for vbox in self.vboxes:
            if vbox.contains(color):
                return vbox.color

        return self.nearest(color)


class PQueue(Iterator):

    def __init__(self, sorted_key):
        self.sorted_key = sorted_key
        self.items = []

    def __next__(self):
        if not self.items:
            raise StopIteration()

        return self.pop()

    def append(self, item):
        self.items.append(item)
        self.items = sorted(self.items, key=self.sorted_key, reverse=True)

    def pop(self):
        return self.items.pop(0)

    def __len__(self):
        return len(self.items)
