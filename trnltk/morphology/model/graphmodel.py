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
class State(object):
    TERMINAL = "TERMINAL"
    TRANSFER = "TRANSFER"
    DERIVATIONAL = "DERIVATIONAL"

    def __init__(self, name, type, syntactic_category):
        self.name = name
        self.pretty_name = syntactic_category     ##TODO: get rid of this!
        self.syntactic_category = syntactic_category
        self.outputs = [] #(suffix, out_state) tuples
        self.type = type

    def add_out_suffix(self, suffix, to_state):
        self.outputs.append((suffix, to_state))

    def __str__(self):
        return self.name

    def __repr__(self):
        return repr(self.name)