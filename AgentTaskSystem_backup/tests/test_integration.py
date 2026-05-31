import sys
import os

sys.path.insert(0, "/workspace")


def test_import_agent_runtime():
    from AgentTaskSystem.agent_runtime.impl.agent_runtime_impl import AgentRuntimeImpl
    runtime = AgentRuntimeImpl()
    assert runtime is not None
    print("PASS: AgentRuntimeImpl import")


def test_import_task_core():
    from AgentTaskSystem.task_core.impl.task_core_impl import TaskCoreImpl
    assert TaskCoreImpl is not None
    print("PASS: TaskCoreImpl import")


def test_import_task_define():
    from AgentTaskSystem.task_core.task_define.interfaces.i_task_define import ITaskDefine
    from AgentTaskSystem.task_core.task_define.interfaces.task_dto import TaskParamDto, TaskResultDto
    assert ITaskDefine is not None
    assert TaskParamDto is not None
    assert TaskResultDto is not None
    print("PASS: TaskDefine interfaces import")


def test_import_task_state():
    from AgentTaskSystem.task_core.task_state.interfaces.i_task_state import ITaskState
    from AgentTaskSystem.task_core.task_state.interfaces.task_state_enum import TaskStateEnum
    assert ITaskState is not None
    assert TaskStateEnum is not None
    print("PASS: TaskState interfaces import")


def test_import_task_schedule():
    from AgentTaskSystem.agent_runtime.task_schedule.interfaces.i_task_schedule import ITaskSchedule
    from AgentTaskSystem.agent_runtime.task_schedule.interfaces.schedule_priority import SchedulePriority
    assert ITaskSchedule is not None
    assert SchedulePriority is not None
    print("PASS: TaskSchedule interfaces import")


def test_import_task_runner():
    from AgentTaskSystem.agent_runtime.task_runner.interfaces.i_task_runner import ITaskRunner
    assert ITaskRunner is not None
    print("PASS: TaskRunner interfaces import")


def test_import_common():
    from AgentTaskSystem.common.service_provider import ServiceProvider
    from AgentTaskSystem.common.error_code import ErrorCode
    assert ServiceProvider is not None
    assert ErrorCode is not None
    print("PASS: Common module import")


def test_import_utils():
    from AgentTaskSystem.common.utils.TimeUtil import TimeUtil
    from AgentTaskSystem.common.utils.IdUtil import IdUtil
    assert TimeUtil is not None
    assert IdUtil is not None
    print("PASS: Utils import")


def run_all_tests():
    print("=" * 50)
    print("Running Integration Tests")
    print("=" * 50)
    
    tests = [
        test_import_agent_runtime,
        test_import_task_core,
        test_import_task_define,
        test_import_task_state,
        test_import_task_schedule,
        test_import_task_runner,
        test_import_common,
        test_import_utils,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"FAIL: {test.__name__} - {e}")
            failed += 1
    
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
