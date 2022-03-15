import json  # noqa # pylint: disable=unused-import
import subprocess
import time

import requests

from get_project_core.settings import logger, config, current_dir

headers = {'PRIVATE-TOKEN': config('X5_SCM_TOKEN', cast=str)}


def create_repositories(group_id: int):
    """
    Create submodules from gitlab group

    :param group_id: Can be find under group name
    """
    request = requests.get(f'https://scm.x5.ru/api/v4/groups/{group_id}/projects', headers=headers, verify=False)
    # logger.info(f'{json.dumps(request.json(), indent=4, separators=(",", ":"))}')

    repos = request.json()

    for repo in repos:
        name = str(repo.get("ssh_url_to_repo", None)).strip()
        subprocess.Popen(['git', 'submodule', 'add', name])
        logger.info(f'Created: {name}')
        time.sleep(15)


def update_submodules():
    """
    Update all submodules

    """
    subprocess.Popen(['git', 'submodule', 'foreach', f'{current_dir}/get-project-core/update-repos.sh'])


if __name__ == '__main__':
    create_repositories(group_id=3574)
    # update_submodules()
