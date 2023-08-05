# vim:set ts=4 sw=4 et nowrap syntax=python ff=unix:
#
# Copyright 2020 Mark Crewson <mark@crewson.net>
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

from .api import CurseAPI

##############################################################################


class Curseforge (CurseAPI):

    CURSE_BASEURL = 'https://addons-ecs.forgesvc.net/api/v2/'

    def __init__(self, authn_token):
        super(Curseforge, self).__init__()
        self.authn_token = authn_token

    def _api_baseurl(self):
        return self.CURSE_BASEURL

    def _request_headers(self, authRequired):
        hdrs = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit 537.6 ' +
                              '(KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.6'}
        if authRequired:
            hdrs['AuthenticationToken'] = self.authn_token
        return hdrs

##############################################################################
# THE END
