# coding=utf-8
"""
Copyright  2012  Ali Ok (aliokATapacheDOTorg)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from collections import defaultdict
class HierarchicalIndex(object):
    def __init__(self, depth):
        assert depth > 1 and isinstance(depth, int)
        self._depth = depth
        indices_type = self._get_indices_type(depth=depth)
        self._indices = indices_type()

    def get(self, *args):
        assert args[0] is not None
        assert len(args)<=self._depth

        node = self._follow_path(args)
        leaves = self._get_leaves(node)
        return list(sorted(set(leaves)))

    def insert(self, value, *args):
        assert len(args)==self._depth
        node = self._follow_path(args)
        node.append(value)

    def _follow_path(self, path):
        node = self._indices
        for p in path:
            node = node[p]
        return node

    def _get_leaves(self, node):
        if isinstance(node, dict):
            leaves = []
            for key in node.iterkeys():
                leaves.extend(self._get_leaves(node[key]))
            return leaves

        else:       #then it must be a <list>
            return node

    @classmethod
    def _get_indices_type(cls, depth):
        assert depth>=1
        if depth==1:
            return lambda : defaultdict(list)
        else:
            return lambda : defaultdict(cls._get_indices_type(depth-1))

    __hash__ = None