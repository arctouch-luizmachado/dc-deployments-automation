import os
from six.moves import urllib

import testinfra.utils.ansible_runner
import json

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_version_file_is_latest(host):
    verfile = host.file('/media/atl/jira/shared/jira-core.version')
    assert verfile.exists

    upstream_fd = urllib.request.urlopen("https://marketplace.atlassian.com/rest/2/applications/jira/versions/latest")
    upstream_json = json.load(upstream_fd)
    upstream = upstream_json['version']

    assert verfile.content.decode("UTF-8").strip() == upstream.strip()

def test_latest_is_downloaded(host):
    upstream_fd = urllib.request.urlopen("https://marketplace.atlassian.com/rest/2/applications/jira/versions/latest")
    upstream_json = json.load(upstream_fd)
    upstream = upstream_json['version']

    installer = host.file('/opt/atlassian/tmp/jira-core.'+upstream+'-x64.bin')
    assert installer.exists
    assert installer.user == 'root'
