#!/usr/bin/env python

import urllib2
import json
import base64

# Api config
GITHUB_API_URL = "https://api.github.com"
CODECOV_API_URL = "https://codecov.io/api"
TRAVIS_API_URL = "https://api.travis-ci.org"
# TRAVIS_API_URL = "https://api.travis-ci.com"

# Token config
GITHUB_TOKEN = ""
CODECOV_TOKEN = ""

# Github repo config
GITHUB_ORG = "91chenxing"
GITHUB_REPO_NAME = "repo-2"
GITHUB_REPO_DESCRIPTION = "The description of the repo."
GITHUB_REPO_HOMEPAGE = "https://github.com/easemob/"
GITHUB_REPO_PRIVATE = False
GITHUB_REPO_AUTO_INIT = True
GITHUB_REPO_IG_TP = 'Java'
GITHUB_REPO_USERNAME = "sheepstarli"
GITHUB_REPO_MAIL= "licx@easemob.com"

# Travis config
TRAVIS_USER_PARAMS = [
    {
        "name": "p1",
        "value": "v1",
        "public": True
    },{
        "name": "p2",
        "value": "v2",
        "public": False
    },{
        "name": "p3",
        "value": "v3",
        "public": False
    },{
        "name": "p4",
        "value": "v4",
        "public": True
    }
]

# Common Header
CONTENT_TYPE = {"Content-Type": "application/json"}

# Other Header
GITHUB_AUTH_TOKEN = {"Authorization": "token " + GITHUB_TOKEN}
GITHUB_ACCEPT = {"Accept": "application/vnd.github.v3+json"}

CODECOV_AUTH_TOKEN = {"Authorization": "token " + CODECOV_TOKEN}

TRAVIS_AUTH_TOKEN = {"Authorization": "token "}
TRAVIS_ACCEPT = {"Accept": "application/vnd.travis-ci.2+json"}
TRAVIS_USER_AGENT = {"User-Agent": "MyClient/1.0.0"}

def req_github_create_repo():
    print 'Create repo...'
    github_body_create_repo = {
        "name": GITHUB_REPO_NAME,
        "description": GITHUB_REPO_DESCRIPTION,
        "homepage": GITHUB_REPO_HOMEPAGE,
        "private": GITHUB_REPO_PRIVATE,
        "auto_init": GITHUB_REPO_AUTO_INIT,
        "gitignore_template": GITHUB_REPO_IG_TP
    }
    headers = {}
    headers.update(GITHUB_AUTH_TOKEN)
    headers.update(GITHUB_ACCEPT)
    req = urllib2.Request(url=GITHUB_API_URL + "/orgs/" + GITHUB_ORG + "/repos",
                          data=json.dumps(github_body_create_repo), headers=headers)
    req.get_method = lambda: 'POST'
    try:
        res = urllib2.urlopen(req)
        print 'Create repo success.', res.read()
        res.close()
    except urllib2.HTTPError, e:
        print 'Create repo error resultCode:', e.code
        print 'Create repo error msg:', (e.read().decode('utf-8'))
    except urllib2.URLError, e:
        print 'Create repo error msg(internet error):', e.reason
    except Exception, e:
        print 'Create repo unknown error', e


def req_github_list_team():
    print 'Getting team list'
    headers = {}
    headers.update(GITHUB_AUTH_TOKEN)
    headers.update(GITHUB_ACCEPT)
    req = urllib2.Request(url=GITHUB_API_URL + "/orgs/" + GITHUB_ORG + "/teams", headers=headers)
    req.get_method = lambda: 'GET'
    team_list = None
    try:
        res = urllib2.urlopen(req)
        json_str = res.read()
        res.close()
        team_list = json.loads(json_str)
    except urllib2.HTTPError, e:
        print 'error resultCode:', e.code
        print 'error msg:', (e.read().decode('utf-8'))
    except urllib2.URLError, e:
        print 'error msg(internet error):', e.reason
    except Exception, e:
        print 'Unknown error', e

    print "Team List"
    for team in team_list:
        print "name:", team["name"], "\tid:", team["id"]


def req_github_team_add_repo(team_id, permission):
    body = {
        "permission": permission
    }
    headers = {}
    headers.update(GITHUB_AUTH_TOKEN)
    headers.update(GITHUB_ACCEPT)
    req = urllib2.Request(url=GITHUB_API_URL + "/teams/" + team_id + "/repos/" + GITHUB_ORG + "/" + GITHUB_REPO_NAME,
                          data=json.dumps(body), headers=headers)
    req.get_method = lambda: 'PUT'
    try:
        res = urllib2.urlopen(req)
        print 'Added repo', GITHUB_REPO_NAME, 'team', team_id, 'with permission', permission, 'success!'
        res.close()
    except urllib2.HTTPError, e:
        print 'Added repo error resultCode:', e.code
        print 'Added repo error msg:', (e.read().decode('utf-8'))
    except urllib2.URLError, e:
        print 'Added repo error msg(internet error):', e.reason
    except:
        print 'Added repo unknown error'


def github_team_add_repo():
    str1 = raw_input("Please input team_id and permission(eg. 123,pull 222,push 333,admin):")
    if len(str1) == 0:
        print 'Input error'
        return False
    arr1 = str1.split()
    for id_team in arr1:
        arr2 = id_team.split(",")
        req_github_team_add_repo(arr2[0], arr2[1])
    return True


def req_github_get_head_ref():
    print 'Getting head ref'
    headers = {}
    headers.update(GITHUB_AUTH_TOKEN)
    headers.update(GITHUB_ACCEPT)
    req = urllib2.Request(
        url=GITHUB_API_URL + "/repos/" + GITHUB_ORG + "/" + GITHUB_REPO_NAME + "/git/refs/heads/master",
        headers=headers)
    req.get_method = lambda: 'GET'
    ref_body = None
    try:
        res = urllib2.urlopen(req)
        json_str = res.read()
        print 'Get head master ref success.' + json_str
        res.close()
        ref_body = json.loads(json_str)
    except urllib2.HTTPError, e:
        print 'Get head master ref error resultCode:', e.code
        print 'Get head master ref error msg:', (e.read().decode('utf-8'))
    except urllib2.URLError, e:
        print 'Get head master ref error msg(internet error):', e.reason
    except Exception, e:
        print 'Get head master ref unknown error', e
    return ref_body


def github_get_head_ref():
    ref_body = req_github_get_head_ref()
    return ref_body['object']['sha']


def req_github_add_branch_dev(sha):
    body = {
        "ref": "refs/heads/dev",
        "sha": sha
    }
    headers = {}
    headers.update(GITHUB_AUTH_TOKEN)
    headers.update(GITHUB_ACCEPT)
    req = urllib2.Request(url=GITHUB_API_URL + "/repos/" + GITHUB_ORG + "/" + GITHUB_REPO_NAME + "/git/refs",
                          data=json.dumps(body), headers=headers)
    req.get_method = lambda: 'POST'
    try:
        res = urllib2.urlopen(req)
        print 'Added', GITHUB_REPO_NAME, 'branch dev on commit', sha, 'success!'
        res.close()
    except urllib2.HTTPError, e:
        print 'Added branch error resultCode:', e.code
        print 'Added branch error msg:', (e.read().decode('utf-8'))
    except urllib2.URLError, e:
        print 'Added branch error msg(internet error):', e.reason
    except Exception, e:
        print 'Added branch unknown error', e


def github_add_branch_dev():
    sha = github_get_head_ref()
    req_github_add_branch_dev(sha)


def req_github_update_default_branch_dev():
    body = {
        "name": GITHUB_REPO_NAME,
        "default_branch": "dev"
    }
    headers = {}
    headers.update(GITHUB_AUTH_TOKEN)
    headers.update(GITHUB_ACCEPT)
    req = urllib2.Request(url=GITHUB_API_URL + "/repos/" + GITHUB_ORG + "/" + GITHUB_REPO_NAME,
                          data=json.dumps(body), headers=headers)
    req.get_method = lambda: 'PATCH'
    try:
        res = urllib2.urlopen(req)
        print 'Update', GITHUB_REPO_NAME, 'default branch dev success!'
        res.close()
    except urllib2.HTTPError, e:
        print 'Update default branch error resultCode:', e.code
        print 'Update default branch error msg:', (e.read().decode('utf-8'))
    except urllib2.URLError, e:
        print 'Update default branch error msg(internet error):', e.reason
    except Exception, e:
        print 'Added default branch unknown error', e


def req_github_create_file(filename, content, message="init", branch="dev"):
    body = {
        "message": message,
        "committer": {
            "name": GITHUB_REPO_USERNAME,
            "email": GITHUB_REPO_MAIL
        },
        "branch": branch,
        "content": base64.b64encode(content)
    }
    headers = {}
    headers.update(GITHUB_AUTH_TOKEN)
    headers.update(GITHUB_ACCEPT)
    req = urllib2.Request(url=GITHUB_API_URL + "/repos/" + GITHUB_ORG + "/" + GITHUB_REPO_NAME + "/contents/" + filename,
                          data=json.dumps(body), headers=headers)
    req.get_method = lambda: 'PUT'
    try:
        res = urllib2.urlopen(req)
        print 'Create', filename, 'in', GITHUB_REPO_NAME, 'on branch', branch, 'with content', content, 'success!'
        res.close()
    except urllib2.HTTPError, e:
        print 'Create file error resultCode:', e.code
        print 'Create file error msg:', (e.read().decode('utf-8'))
    except urllib2.URLError, e:
        print 'Create file error msg(internet error):', e.reason
    except Exception, e:
        print 'Create file error unknown error', e


def req_codecov_get_upload_token():
    headers = {}
    headers.update(CODECOV_AUTH_TOKEN)
    req = urllib2.Request(url=CODECOV_API_URL + "/gh/" + GITHUB_ORG + "/" + GITHUB_REPO_NAME, headers=headers)
    req.get_method = lambda: 'GET'
    token_body = None
    try:
        res = urllib2.urlopen(req)
        json_str = res.read()
        print 'Get', GITHUB_REPO_NAME, 'codecov upload token success.' + json_str
        res.close()
        token_body = json.loads(json_str)
    except urllib2.HTTPError, e:
        print 'Get token error resultCode:', e.code
        print 'Get token error msg:', (e.read().decode('utf-8'))
    except urllib2.URLError, e:
        print 'Get token error msg(internet error):', e.reason
    except Exception, e:
        print 'Get token unknown error', e
    return token_body


def codecov_init_upload_token():
    token_body = req_codecov_get_upload_token()
    upload_token = token_body['repo']['upload_token']
    req_github_create_file('codecov-token', upload_token, 'Init codevoc upload token.', 'dev')


def req_travis_get_token():
    body = {
        "github_token": GITHUB_TOKEN
    }
    headers = {}
    headers.update(TRAVIS_ACCEPT)
    headers.update(TRAVIS_USER_AGENT)
    headers.update(CONTENT_TYPE)
    req = urllib2.Request(url=TRAVIS_API_URL + "/auth/github", data=json.dumps(body), headers=headers)
    req.get_method = lambda: 'POST'
    token_body = None
    try:
        res = urllib2.urlopen(req)
        json_str = res.read()
        print 'Get travis token success.' + json_str
        res.close()
        token_body = json.loads(json_str)
        TRAVIS_AUTH_TOKEN['Authorization'] = 'token ' + token_body['access_token']
    except urllib2.HTTPError, e:
        print 'Get travis token error resultCode:', e.code
        print 'Get travis token error msg:', (e.read().decode('utf-8'))
    except urllib2.URLError, e:
        print 'Get travis token error msg(internet error):', e.reason
    except Exception, e:
        print 'Get travis token unknown error', e
    return token_body


def req_travis_sync_user():
    headers = {}
    headers.update(TRAVIS_ACCEPT)
    headers.update(TRAVIS_USER_AGENT)
    headers.update(TRAVIS_AUTH_TOKEN)
    req = urllib2.Request(url=TRAVIS_API_URL + "/users/sync", headers=headers)
    req.get_method = lambda: 'GET'
    try:
        res = urllib2.urlopen(req)
        json_str = res.read()
        print 'Sync travis user success.' + json_str
        res.close()
    except urllib2.HTTPError, e:
        print 'Sync travis error resultCode:', e.code
        print 'Sync travis error msg:', (e.read().decode('utf-8'))
    except urllib2.URLError, e:
        print 'Sync travis error msg(internet error):', e.reason
    except Exception, e:
        print 'Sync travis unknown error', e


def req_travis_get_hooks():
    headers = {}
    headers.update(TRAVIS_ACCEPT)
    headers.update(TRAVIS_USER_AGENT)
    headers.update(TRAVIS_AUTH_TOKEN)
    req = urllib2.Request(url=TRAVIS_API_URL + "/hooks?all=true&owner_name=" + GITHUB_ORG, headers=headers)
    req.get_method = lambda: 'GET'
    res_body = None
    try:
        res = urllib2.urlopen(req)
        json_str = res.read()
        print 'Get travis hooks success.' + json_str
        res.close()
        res_body = json.loads(json_str)
    except urllib2.HTTPError, e:
        print 'Get travis hooks error resultCode:', e.code
        print 'Get travis hooks error msg:', (e.read().decode('utf-8'))
    except urllib2.URLError, e:
        print 'Get travis hooks error msg(internet error):', e.reason
    except Exception, e:
        print 'Get travis hooks unknown error', e
    return res_body


def travis_get_new_hook_id():
    hooks_res = req_travis_get_hooks()
    hooks = hooks_res['hooks']
    for hook in hooks:
        if hook['name'] == GITHUB_REPO_NAME:
            print 'Get the hook.', hook
            return hook['id']
    return None


def req_travis_active_hook(hook_id):
    body = {
        "hook": {
            "active": True,
            "id": hook_id
        }
    }
    headers = {}
    headers.update(TRAVIS_ACCEPT)
    headers.update(TRAVIS_USER_AGENT)
    headers.update(TRAVIS_AUTH_TOKEN)
    headers.update(CONTENT_TYPE)
    req = urllib2.Request(url=TRAVIS_API_URL + "/hooks", data=json.dumps(body), headers=headers)
    req.get_method = lambda: 'PUT'
    try:
        res = urllib2.urlopen(req)
        json_str = res.read()
        print 'Active hook success.' + json_str
        res.close()
    except urllib2.HTTPError, e:
        print 'Active hook error resultCode:', e.code
        print 'Active hook error msg:', (e.read().decode('utf-8'))
    except urllib2.URLError, e:
        print 'Active hook error msg(internet error):', e.reason
    except Exception, e:
        print 'Active hook unknown error', e


def req_travis_add_parameter(repo_id, param):
    body = {
        "env_var": param
    }
    headers = {}
    headers.update(TRAVIS_ACCEPT)
    headers.update(TRAVIS_USER_AGENT)
    headers.update(TRAVIS_AUTH_TOKEN)
    headers.update(CONTENT_TYPE)
    req = urllib2.Request(url=TRAVIS_API_URL + "/settings/env_vars?repository_id=" + str(repo_id), data=json.dumps(body),
                          headers=headers)
    req.get_method = lambda: 'POST'
    try:
        res = urllib2.urlopen(req)
        json_str = res.read()
        print 'Add travis parameter success.' + json_str
        res.close()
    except urllib2.HTTPError, e:
        print 'Add travis parameter error resultCode:', e.code
        print 'Add travis parameter error msg:', (e.read().decode('utf-8'))
    except urllib2.URLError, e:
        print 'Add travis parameter error msg(internet error):', e.reason
    except Exception, e:
        print 'Add travis parameter unknown error', e


def travis_add_parameters(repo_id):
    for param in TRAVIS_USER_PARAMS:
        req_travis_add_parameter(repo_id, param)


if __name__ == "__main__":
    print 'Starting...'
    req_github_create_repo()
    req_github_list_team()
    github_team_add_repo()
    github_add_branch_dev()
    req_github_update_default_branch_dev()
    codecov_init_upload_token()
    req_travis_get_token()
    # req_travis_sync_user()
    hook_id = travis_get_new_hook_id()
    req_travis_active_hook(hook_id)
    travis_add_parameters(hook_id)
    print 'Please check the result.'
