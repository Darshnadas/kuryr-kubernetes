# Copyright 2018 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from kuryr_kubernetes.objects import base as kuryr_base
from kuryr_kubernetes.tests import base as test_base
from oslo_versionedobjects import base
from oslo_versionedobjects import fixture

# NOTE(danms): The hashes in this list should only be changed if
# they come with a corresponding version bump in the affected
# objects
object_data = {
    'LBaaSL7Policy':
    '1.0-3ac4fcd50a555f433a78c67cb6a4cd52',
    'LBaaSL7Rule': '1.0-276d9d678e1a8fc4b53fdbf3b2ac39ec',
    'LBaaSListener': '1.0-a9e2d5c73687f5edc66fdb2f48650e15',
    'LBaaSLoadBalancer': '1.3-8bc0a9bdbd160da67572aa38784378d1',
    'LBaaSMember': '1.0-a770c6884c27d6d8c21186b27d0e2ccb',
    'LBaaSPool': '1.1-6e77370d7632a902445444249eb77b01',
    'LBaaSPortSpec': '1.1-fcfa2fd07f4bc5619b96fa41bcdf6e23',
    'LBaaSPubIp': '1.0-83992edec2c60fb4ab8998ea42a4ff74',
    'LBaaSRouteNotifEntry': '1.0-dd2f2be956f68814b1f47cb13483a885',
    'LBaaSRouteNotifier': '1.0-f0bfd8e772434abe7557930d7e0180c1',
    'LBaaSRouteState': '1.0-bdf561462a2d337c0e0ae8cb10e9ff20',
    'LBaaSServiceSpec': '1.0-d430ecd443f2b1999196bfe531e56f7e',
    'LBaaSState': '1.0-a0ff7dce2d3f6ce1ffab4ff95a344361',
    'RouteSpec': '1.0-2f02b2e24b1ca2b94c2bbdb718bfc020',
    'RouteState': '1.0-2475dbeb6ebedabe2a1e235f9bc6b614',
}


def get_kuryr_objects():
    """Get Kuryr versioned objects

    This returns a dict of versioned objects which are
    in the Kuryr project namespace only (excludes objects
    from os-vif and other 3rd party modules)

    :return: a dict mapping class names to lists of versioned objects
    """

    all_classes = base.VersionedObjectRegistry.obj_classes()
    kuryr_classes = {}
    for name in all_classes:
        objclasses = all_classes[name]
        if (objclasses[0].OBJ_PROJECT_NAMESPACE ==
                kuryr_base.KuryrK8sObjectBase.OBJ_PROJECT_NAMESPACE):
            kuryr_classes[name] = objclasses
    return kuryr_classes


class TestObjectVersions(test_base.TestCase):
    def test_versions(self):
        """Test Versions

        Ensures that modified objects had their versions bumped
        """

        checker = fixture.ObjectVersionChecker(
            get_kuryr_objects())
        expected, actual = checker.test_hashes(object_data)
        self.assertEqual(expected, actual,
                         """Some objects have changed; please make sure the
                         versions have been bumped and backporting
                         compatibility code has been added to
                         obj_make_compatible if necessary, and then update
                         their hashes in the object_data map in this test
                         module. If we don't need to add backporting code then
                         it means we also don't need the version bump and we
                         just have to change the hash in this module.""")
