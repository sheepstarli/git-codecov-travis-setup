import read_yaml


class Config:
    def __init__(self):
        yaml_config = read_yaml.read_yaml_config()
        self.config = yaml_config

    @property
    def github_api_url(self):
        return self.config['GITHUB_API_URL']

    @property
    def codecov_api_url(self):
        return self.config['CODECOV_API_URL']

    @property
    def travis_api_url(self):
        return self.config['TRAVIS_API_URL']

    @property
    def github_token(self):
        return self.config['GITHUB_TOKEN']

    @property
    def codecov_token(self):
        return self.config['CODECOV_TOKEN']

    @property
    def github_org(self):
        return self.config['GITHUB_ORG']

    @property
    def github_repo_description(self):
        return self.config['GITHUB_REPO_DESCRIPTION']

    @property
    def github_repo_homepage(self):
        return self.config['GITHUB_REPO_HOMEPAGE']

    @property
    def github_repo_private(self):
        return self.config['GITHUB_REPO_PRIVATE']

    @property
    def github_repo_auto_init(self):
        return self.config['GITHUB_REPO_AUTO_INIT']

    @property
    def github_repo_ig_tp(self):
        return self.config['GITHUB_REPO_IG_TP']

    @property
    def github_repo_username(self):
        return self.config['GITHUB_REPO_USERNAME']

    @property
    def github_repo_mail(self):
        return self.config['GITHUB_REPO_MAIL']

    @property
    def travis_user_params(self):
        return self.config['TRAVIS_USER_PARAMS']
