#!/usr/bin/env python

import urllib2
import json
import base64
import sys
import config


# Common Header
CONTENT_TYPE = {"Content-Type": "application/json"}

# Other Header
GITHUB_AUTH_TOKEN = {"Authorization": "token "}
GITHUB_ACCEPT = {"Accept": "application/vnd.github.v3+json"}

CODECOV_AUTH_TOKEN = {"Authorization": "token "}

TRAVIS_AUTH_TOKEN = {"Authorization": "token "}
TRAVIS_ACCEPT = {"Accept": "application/vnd.travis-ci.2+json"}
TRAVIS_USER_AGENT = {"User-Agent": "MyClient/1.0.0"}

cfg = None

def init_config():
    global cfg
    cfg = config.Config()
    GITHUB_AUTH_TOKEN["Authorization"] = "token " + cfg.github_token
    CODECOV_AUTH_TOKEN["Authorization"] = "token " + cfg.codecov_token


def github_input_repo_name():
    str1 = raw_input("Please input repo name:")
    if len(str1) == 0:
        print 'Input error'
        return None
    return str1


def req_github_create_repo(name):
    print 'Create repo...'
    github_body_create_repo = {
        "name": name,
        "description": cfg.github_repo_description,
        "homepage": cfg.github_repo_homepage,
        "private": cfg.github_repo_private,
        "auto_init": cfg.github_repo_auto_init,
        "gitignore_template": cfg.github_repo_ig_tp
    }
    headers = {}
    headers.update(GITHUB_AUTH_TOKEN)
    headers.update(GITHUB_ACCEPT)
    req = urllib2.Request(url=cfg.github_api_url + "/orgs/" + cfg.github_org + "/repos",
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


def req_github_list_team(page=1, per_page=100):
    print 'Getting team list page', page
    headers = {}
    headers.update(GITHUB_AUTH_TOKEN)
    headers.update(GITHUB_ACCEPT)
    req = urllib2.Request(url=cfg.github_api_url + "/orgs/" + cfg.github_org + "/teams?page=" + str(page) + "&per_page=" + str(per_page), headers=headers)
    req.get_method = lambda: 'GET'
    try:
        res = urllib2.urlopen(req)
        json_str = res.read()
        res.close()
        return json.loads(json_str)
    except urllib2.HTTPError, e:
        print 'error resultCode:', e.code
        print 'error msg:', (e.read().decode('utf-8'))
    except urllib2.URLError, e:
        print 'error msg(internet error):', e.reason
    except Exception, e:
        print 'Unknown error', e


def github_list_team():
    page = 1
    per_page = 1
    team_list = []
    while True:
        tmp_list = req_github_list_team(page, per_page)
        if tmp_list:
            team_list.extend(tmp_list)
            page += 1
        else:
            break

    print "Team List"
    for team in team_list:
        print "name:", team["name"], "\t\t\t\tid:", team["id"]


def req_github_team_add_repo(name, team_id, permission):
    body = {
        "permission": permission
    }
    headers = {}
    headers.update(GITHUB_AUTH_TOKEN)
    headers.update(GITHUB_ACCEPT)
    req = urllib2.Request(url=cfg.github_api_url + "/teams/" + team_id + "/repos/" + cfg.github_org + "/" + name,
                          data=json.dumps(body), headers=headers)
    req.get_method = lambda: 'PUT'
    try:
        res = urllib2.urlopen(req)
        print 'Added repo', name, 'team', team_id, 'with permission', permission, 'success!'
        res.close()
    except urllib2.HTTPError, e:
        print 'Added repo error resultCode:', e.code
        print 'Added repo error msg:', (e.read().decode('utf-8'))
    except urllib2.URLError, e:
        print 'Added repo error msg(internet error):', e.reason
    except:
        print 'Added repo unknown error'


def github_team_add_repo(name):
    str1 = raw_input("Please input team_id and permission(eg. 123,pull 222,push 333,admin):")
    if len(str1) == 0:
        print 'Input error'
        return False
    arr1 = str1.split()
    for id_team in arr1:
        arr2 = id_team.split(",")
        req_github_team_add_repo(name, arr2[0], arr2[1])
    return True


def req_github_get_head_ref(name):
    print 'Getting head ref'
    headers = {}
    headers.update(GITHUB_AUTH_TOKEN)
    headers.update(GITHUB_ACCEPT)
    req = urllib2.Request(
        url=cfg.github_api_url + "/repos/" + cfg.github_org + "/" + name + "/git/refs/heads/master",
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


def github_get_head_ref(name):
    ref_body = req_github_get_head_ref(name)
    return ref_body['object']['sha']


def req_github_add_branch_dev(name, sha):
    body = {
        "ref": "refs/heads/dev",
        "sha": sha
    }
    headers = {}
    headers.update(GITHUB_AUTH_TOKEN)
    headers.update(GITHUB_ACCEPT)
    req = urllib2.Request(url=cfg.github_api_url + "/repos/" + cfg.github_org + "/" + name + "/git/refs",
                          data=json.dumps(body), headers=headers)
    req.get_method = lambda: 'POST'
    try:
        res = urllib2.urlopen(req)
        print 'Added', name, 'branch dev on commit', sha, 'success!'
        res.close()
    except urllib2.HTTPError, e:
        print 'Added branch error resultCode:', e.code
        print 'Added branch error msg:', (e.read().decode('utf-8'))
    except urllib2.URLError, e:
        print 'Added branch error msg(internet error):', e.reason
    except Exception, e:
        print 'Added branch unknown error', e


def github_add_branch_dev(name):
    sha = github_get_head_ref(name)
    req_github_add_branch_dev(name, sha)


def req_github_update_default_branch_dev(name):
    body = {
        "name": name,
        "default_branch": "dev"
    }
    headers = {}
    headers.update(GITHUB_AUTH_TOKEN)
    headers.update(GITHUB_ACCEPT)
    req = urllib2.Request(url=cfg.github_api_url + "/repos/" + cfg.github_org + "/" + name,
                          data=json.dumps(body), headers=headers)
    req.get_method = lambda: 'PATCH'
    try:
        res = urllib2.urlopen(req)
        print 'Update', name, 'default branch dev success!'
        res.close()
    except urllib2.HTTPError, e:
        print 'Update default branch error resultCode:', e.code
        print 'Update default branch error msg:', (e.read().decode('utf-8'))
    except urllib2.URLError, e:
        print 'Update default branch error msg(internet error):', e.reason
    except Exception, e:
        print 'Added default branch unknown error', e


def req_github_create_file(name, filename, content, message="init", branch="dev"):
    body = {
        "message": message,
        "committer": {
            "name": cfg.github_repo_username,
            "email": cfg.github_repo_mail
        },
        "branch": branch,
        "content": base64.b64encode(content)
    }
    headers = {}
    headers.update(GITHUB_AUTH_TOKEN)
    headers.update(GITHUB_ACCEPT)
    req = urllib2.Request(url=cfg.github_api_url + "/repos/" + cfg.github_org + "/" + name + "/contents/" + filename,
                          data=json.dumps(body), headers=headers)
    req.get_method = lambda: 'PUT'
    try:
        res = urllib2.urlopen(req)
        print 'Create', filename, 'in', name, 'on branch', branch, 'with content', content, 'success!'
        res.close()
    except urllib2.HTTPError, e:
        print 'Create file error resultCode:', e.code
        print 'Create file error msg:', (e.read().decode('utf-8'))
    except urllib2.URLError, e:
        print 'Create file error msg(internet error):', e.reason
    except Exception, e:
        print 'Create file error unknown error', e


def req_codecov_get_upload_token(name):
    headers = {}
    headers.update(CODECOV_AUTH_TOKEN)
    req = urllib2.Request(url=cfg.codecov_api_url + "/gh/" + cfg.github_org + "/" + name, headers=headers)
    req.get_method = lambda: 'GET'
    token_body = None
    try:
        res = urllib2.urlopen(req)
        json_str = res.read()
        print 'Get', name, 'codecov upload token success.' + json_str
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


def codecov_init_upload_token(name):
    token_body = req_codecov_get_upload_token(name)
    upload_token = token_body['repo']['upload_token']
    req_github_create_file(name, '.codecov-token', upload_token, 'Init codevoc upload token.', 'dev')


def req_travis_get_token():
    body = {
        "github_token": cfg.github_token
    }
    headers = {}
    headers.update(TRAVIS_ACCEPT)
    headers.update(TRAVIS_USER_AGENT)
    headers.update(CONTENT_TYPE)
    req = urllib2.Request(url=cfg.travis_api_url + "/auth/github", data=json.dumps(body), headers=headers)
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
    req = urllib2.Request(url=cfg.travis_api_url + "/users/sync", headers=headers)
    req.get_method = lambda: 'POST'
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
    req = urllib2.Request(url=cfg.travis_api_url + "/hooks?all=true&owner_name=" + cfg.github_org, headers=headers)
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


def travis_get_new_hook_id(name):
    hooks_res = req_travis_get_hooks()
    hooks = hooks_res['hooks']
    for hook in hooks:
        if hook['name'] == name:
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
    req = urllib2.Request(url=cfg.travis_api_url + "/hooks", data=json.dumps(body), headers=headers)
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
    req = urllib2.Request(url=cfg.travis_api_url + "/settings/env_vars?repository_id=" + str(repo_id), data=json.dumps(body),
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
    for param in cfg.travis_user_params:
        req_travis_add_parameter(repo_id, param)


def travis_init_script(name):
    f = file('template_travis.yml', 'r')
    content = f.read()
    req_github_create_file(name, ".travis.yml", content)


if __name__ == "__main__":
    print 'Starting...'
    init_config()
    repo_name = github_input_repo_name()
    req_github_create_repo(repo_name)
    github_list_team()
    github_team_add_repo(repo_name)
    github_add_branch_dev(repo_name)
    req_github_update_default_branch_dev(repo_name)
    codecov_init_upload_token(repo_name)
    req_travis_get_token()
    req_travis_sync_user()
    hook_id = travis_get_new_hook_id(repo_name)
    req_travis_active_hook(hook_id)
    travis_add_parameters(hook_id)
    travis_init_script(repo_name)
    print 'Please check the result.'
