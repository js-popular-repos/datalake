# Copyright 2015 Planet Labs, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import pytest
import os
import stat
import time

from datalake.crtime import get_crtime, CreationTimeError


crtime = os.environ.get('CRTIME', '/usr/local/bin/crtime')
crtime_available = os.path.isfile(crtime) and os.access(crtime, os.X_OK)
crtime_setuid = False
if crtime_available:
    s = os.stat(crtime)
    crtime_setuid = s.st_mode & stat.S_ISUID and s.st_uid == 0


def test_crtime_does_not_exist(monkeypatch, tmpfile):
    monkeypatch.setenv('CRTIME', '/no/such/crtime')
    f = tmpfile('foobar')
    with pytest.raises(CreationTimeError):
        get_crtime(f)


def test_fails_if_file_does_not_exist():
    with pytest.raises(IOError):
        get_crtime('/blurb/nosuchfile')


@pytest.mark.skipif(not crtime_setuid, reason='crtime required')
def test_crtime_works(tmpfile):
    f = tmpfile('foobar')
    t = get_crtime(f)
    error = abs(t - time.time())
    assert error <= 1
