#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from lib.imports import *
from modules.presentations.presentations_by_genre import *
from modules.presentations.presentations_all import *
from modules.presentations.presentation_details import *


def main():
  LLApp([('/obras/genero/(.*)', PresentationsByGenre),
  		('/obras/',PresentationList),
  		('/obras/((\S*?))',PresentationDetails)
  	])
 
if __name__ == "__main__":
  main()