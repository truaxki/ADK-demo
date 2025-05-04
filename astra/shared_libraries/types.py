# Copyright 2025 Google LLC
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

"""Type definitions for astra agents."""

from google.protobuf import json_format

json_response_config = {
    "response_mime_type": "application/json",
}

class ResearchDetail:
    topic: str
    information: str
    sources: list[str]

class ResearchResults:
    research_results: dict = {
        "summary": str,
        "details": list[ResearchDetail],
        "confidence_score": float
    }

class ExecutionResults:
    execution_results: dict = {
        "status": str,
        "actions_taken": list[str],
        "output": str,
        "next_steps": list[str]
    } 