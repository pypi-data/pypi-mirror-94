"""dock_r module, helps with dockerization."""

import fire as _fire

from dock_r.main import (
    login,
    build,
    smart_build,
    tag,
    pull,
    push,
    exists_locally,
    exists_remotely,
    remote_retag,
    ecs_login,
    ecs_retag,
    ecs_submit,
    ecs_wait_for_start,
    ecs_wait_for_stop,
    get_ecs_log_url,
    get_ecs_task_detail_url,
)

def _main():
    _fire.Fire()
