import json

from django.shortcuts import render
import requests

from julython_adder.adder.forms import RepoEnableForm


github_url = 'https://api.github.com/%(command)s?access_token=%(access_token)s'
julython_url = 'http://www.julython.org/api/v1/github'
julython_hook = {
    'name': 'web',
    'active': True,
    'config': {
        'url': julython_url
    }
}

def logged_in(request):
    user_gh = request.user.social_auth.get(provider='github')
    if request.method == 'POST' and 'repos' in request.POST:
        for repo in request.POST.getlist('repos'):
            print repo
            hook_url = github_url % {
                'command': 'repos/%s/hooks' % repo,
                'access_token':user_gh.tokens['access_token'],
            }
            res = requests.get(hook_url)
            hooks = json.loads(res.content)
            existing_hook = [hook for hook in hooks
                             if hook['name'] == 'web'
                             and hook['config']['url'] == julython_url]
            if not existing_hook:
                requests.post(hook_url, data=json.dumps(julython_hook))
            else:
                print 'repo already has hook'
    more = True
    repo_choices = []
    endpoint = github_url % {
            'command': 'user/repos',
            'access_token': user_gh.tokens['access_token']
        }
    while more:
        more = False
        res = requests.get(endpoint)
        if not 'link' in res.headers:
            break
        links = res.headers['link'].split(',')
        for link in links:
            url, rel = link.split(';')
            url = url.strip('<> ')
            key, value = rel.split('=')
            value = value.strip('" ')
            if value == 'next':
                endpoint = url
                more = True
                break
        repos = json.loads(res.content)
        repo_choices += [(repo['full_name'], repo['full_name'])
                         for repo in repos]
    repo_form = RepoEnableForm(repos=repo_choices)
    return render(request,
                  template_name='logged-in.html',
                  dictionary={'repos': repos,
                              'repo_form': repo_form,})
