#!/bin/bash
#Copyright  2012  Ali Ok (aliokATapacheDOTorg)
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

nosetests --verbosity=3  --logging-level=INFO --ignore-files=test_SLOW_.*\.py --exclude=.*999.* --exclude=.*005.*  --exclude=.*004.*  --exclude=.*003.*  --exclude=.*002.* --exclude=.*001.* --exclude=.*SLOW.*