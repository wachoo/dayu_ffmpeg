#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

from base import BaseNode, UniqueList
from uuid import uuid4

class AbstractHolder(BaseNode):
    type = 'abstract_holder'



class InputHolder(AbstractHolder):
    type = 'input_holder'
    max_input_num = 0

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id', uuid4().hex)
        self.name = None
        self.label = None
        self.visited = None
        self.pos_x = -1.0
        self.pos_y = -1.0
        self.selected = False
        self.metadata = None
        self.parent = kwargs.get('parent', None)
        self.out_edges = [UniqueList() for _ in range(self.max_output_num)]
        self.link_num = None

    @property
    def in_edges(self):
        if self.parent:
            return [self.parent.in_edges[self.link_num]]
        return UniqueList()

    def input(self, index):
        index = index if index >= 0 else index + len(self.in_edges)
        if index >= len(self.in_edges):
            return None
        edge = self.in_edges[index]
        if edge is None:
            return None
        else:
            return edge.endpoints.left

    def delete(self):
        if self.parent:
            self.parent.max_input_num -= 1
            all_inputholders = self.parent.inputholders
            index = all_inputholders.index(self)
            for n in all_inputholders:
                if n.link_num > index:
                    n.link_num -= 1
            for e in self.in_edges:
                if e:
                    e.delete()
            for g in self.out_edges:
                for e in g:
                    if e:
                        e.delete()
            if self.parent is not None:
                self.parent.inside_nodes.remove(self)
            self.parent.in_edges = UniqueList(self.parent.in_edges[:index] + self.parent.in_edges[index+1:])
            self.parent = None
            self.link_num = None



class OutputHolder(AbstractHolder):
    type = 'output_holder'

    def __init__(self, *args, **kwargs):
        super(OutputHolder, self).__init__(*args, **kwargs)
        delattr(self, 'out_edges')
        self.link_num = None

    @property
    def out_edges(self):
        if self.parent:
            return self.parent.out_edges[self.link_num]
        return UniqueList()



