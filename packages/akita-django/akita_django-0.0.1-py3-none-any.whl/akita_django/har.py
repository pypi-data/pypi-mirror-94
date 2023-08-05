# 3-Clause BSD License
# 
# Copyright (c) 2009, Boxed Ice <hello@boxedice.com>
# Copyright (c) 2010-2016, Datadog <info@datadoghq.com>
# Copyright (c) 2020-present, Akita Software <info@akitasoftware.com>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright notice,
#       this list of conditions and the following disclaimer in the documentation
#       and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import datetime
import json
import time

from . import __version__
from pydantic import BaseModel, ValidationError, validator
from queue import Queue, Empty
from threading import Thread
from typing import List


class Record(BaseModel):
    name: str
    value: str


class PostData(BaseModel):
    mimeType: str
    text: str


class ResponseContent(BaseModel):
    size: int
    mimeType: str
    text: str


class Request(BaseModel):
    method: str
    url: str
    httpVersion: str
    cookies: List[Record]
    headers: List[Record]
    queryString: List[Record]
    postData: PostData
    headersSize: int
    bodySize: int


class Response(BaseModel):
    status: int
    statusText: str
    httpVersion: str
    cookies: List[Record]
    headers: List[Record]
    content: ResponseContent
    redirectURL: str
    headersSize: int
    bodySize: int


class Entry(BaseModel):
    startedDateTime: datetime.datetime
    time: float
    request: Request
    response: Response

    @validator('startedDateTime')
    def datetime_must_have_timezone(cls, v: datetime.datetime):
        if v.tzinfo is None:
            raise ValueError('datetime must be timezone aware')
        return v


def _default_har_json_serialization(x):
    """
    Provides JSON serialization for HAR data structures that lack a default
    serialization.  For example, datetime elements need to be serialized as
    ISO 8601 strings.
    """
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    else:
        return str(x)


class HarWriter:
    """
    Coordinates thread-safe request/response logging, encoded as an HTTP
    Archive (HAR) file.

    See http://www.softwareishard.com/har/viewer/ for the HAR formatting
    schema.
    """

    def __init__(self, *args):
        self.file = open(*args)
        self.finished = False
        self.first_entry = True
        self.queue = Queue()

        # Write initial data to the HAR file.
        self._write_preamble()

        Thread(name=f"HarWriter_{time.time}", target=self._writer).start()

    def write_entry(self, entry: Entry):
        sep = '' if self.first_entry else ', '
        self.first_entry = False

        self.queue.put(sep + json.dumps(entry.dict(), default=_default_har_json_serialization))

    def close(self):
        # Close the entries array and the enclosing HAR JSON object.
        self.queue.join()
        self.finished = True
        self._write_postscript()
        self.file.close()

    def _write_preamble(self):
        creator = {
            "name": "Akita DjangoClient",
            "version": __version__,
            "comment": "See https://docs.akita.software.",
        }
        browser = {
            "name": "",
            "version": "",
        }
        comment = "Created by the Akita DjangoClient."
        self.file.write(f'''{{
            "log": {{
                "version": "1.2",
                "creator": {json.dumps(creator)},
                "browser": {json.dumps(browser)},
                "comment": "{comment}",
                "entries": [
        ''')

    def _write_postscript(self):
        # Terminate the entries array, log object, and enclosing HAR object.
        self.file.write(']}}')

    def _writer(self):
        while not self.finished:
            try:
                entry = self.queue.get(True, 1)
            except Empty:
                continue
            self.file.write(entry)
            self.queue.task_done()
