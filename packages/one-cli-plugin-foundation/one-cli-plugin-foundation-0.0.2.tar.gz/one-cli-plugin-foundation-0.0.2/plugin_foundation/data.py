GITLAB_BASE_URL = 'git@gitlab.com:DNXLabs/'
BUBBLETEA_REPOSITORY_URL = 'bubbletea/aws-platform-v2/'
GIT = '.git'

exclude_dirs = ['.git', '.terraform', '.one', 'terraform.tfstate.d', 'terraform-aws-*']
exclude_files = ['.terraform', 'terraform.tfstate*', '.env', '.env.auth', '.terraform-plan-*']

bubbletea_repos = [
    "infra-bubbletea-app-platform-ecs",
    "infra-bubbletea-app-platform-eks",
    "infra-bubbletea-domain",
    "infra-bubbletea-identity",
    "infra-bubbletea-network",
    "infra-bubbletea-network-peering",
    "infra-bubbletea-openvpn",
    "infra-bubbletea-root",
    "infra-bubbletea-shared-services",
    "infra-bubbletea-utilities"
]
