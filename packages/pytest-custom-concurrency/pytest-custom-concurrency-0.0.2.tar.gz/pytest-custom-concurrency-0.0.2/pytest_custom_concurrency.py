from threading import Thread, Lock


def pytest_addoption(parser):
    group = parser.getgroup("custom", "Custom grouping concurrence for pytest")
    group.addoption(
        "--concurrent",
        action="store",
        default="off",
        choices=['on', 'off'],
        help="Default 'off' for switch, option: on or off"
    )
    group.addoption(
        "--sub_group",
        action="store",
        default="group",
        type=str,
        help="Default group name 'group', Can be specified manually"
    )


def pytest_runtestloop(session) -> bool:
    if getattr(session.config.option, "concurrent", None) == "on":
        if session.testsfailed and not session.config.option.continue_on_collection_errors:
            raise session.Interrupted(
                "%d error%s during collection"
                % (session.testsfailed, "s" if session.testsfailed != 1 else "")
            )

        if session.config.option.collectonly:
            return True
        case_obj = {}
        GROUP_NAME = getattr(session.config.option, "sub_group", "group")
        for item in session.items:
            if getattr(item, "callspec", None):
                param = item.callspec.params
                for k, y in param.items():
                    if k == GROUP_NAME:
                        case_obj.setdefault(y, list()).append(item)
            else:
                case_obj.setdefault("default", list()).append(item)

        lock = Lock()
        def run(items):
            for i, item in enumerate(items):
                nextitem = items[i + 1] if i + 1 < len(items) else None
                item.config.hook.pytest_runtest_protocol(item=item, nextitem=nextitem)
                lock.acquire(timeout=2)
                if session.shouldfail:
                    raise session.Failed(session.shouldfail)
                if session.shouldstop:
                    raise session.Interrupted(session.shouldstop)
                lock.release()

        thread_obj = {}
        for k, y in case_obj.items():
            thread = Thread(target=run, kwargs={"items": y})
            thread_obj[k] = thread
            thread.start()
        for obj in thread_obj.values():
            obj.join()
        return True
