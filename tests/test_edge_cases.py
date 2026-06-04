"""
边界条件与异常场景测试
验证修复的8个问题
"""

import pytest
from AgentTaskSystem.agent_runtime.impl.AgentRuntimeImpl import AgentRuntimeImpl
from AgentTaskSystem.task_core.task_define.impl.TaskDefineImpl import TaskDefineImpl
from AgentTaskSystem.task_core.task_state.impl.TaskStateImpl import TaskStateImpl
from AgentTaskSystem.task_core.task_state.interfaces.TaskStateEnum import TaskStateEnum
from AgentTaskSystem.agent_runtime.task_schedule.impl.TaskScheduleImpl import TaskScheduleImpl
from AgentTaskSystem.agent_runtime.task_schedule.interfaces.SchedulePriority import SchedulePriority
from AgentTaskSystem.agent_runtime.task_schedule.interfaces.ScheduleRequestDto import ScheduleRequestDto
from AgentTaskSystem.agent_runtime.task_runner.impl.TaskRunnerImpl import TaskRunnerImpl
from AgentTaskSystem.agent_runtime.task_runner.interfaces.ExecuteRequestDto import ExecuteRequestDto
from AgentTaskSystem.common.Provider import Provider


# ============ 问题1: AgentRuntimeImpl 参数校验 ============

def test_submit_none_task_data():
    """提交 None 任务数据"""
    runtime = AgentRuntimeImpl()
    runtime.initialize()
    result = runtime.submit_task(None)
    assert result is None


def test_submit_non_dict_task_data():
    """提交非 dict 任务数据"""
    runtime = AgentRuntimeImpl()
    runtime.initialize()
    result = runtime.submit_task("invalid")
    assert result is None


def test_submit_empty_dict():
    """提交空 dict"""
    runtime = AgentRuntimeImpl()
    runtime.initialize()
    result = runtime.submit_task({})
    assert result is not None


def test_get_status_invalid_task_id():
    """获取无效 task_id 状态"""
    runtime = AgentRuntimeImpl()
    runtime.initialize()
    assert runtime.get_task_status(None) is None
    assert runtime.get_task_status("") is None
    assert runtime.get_task_status(123) is None


# ============ 问题2: 重复初始化保护 ============

def test_initialize_idempotent():
    """初始化幂等性"""
    runtime = AgentRuntimeImpl()
    assert runtime.initialize() is True
    assert runtime.initialize() is True
    assert runtime.is_running() is True


def test_shutdown_idempotent():
    """关闭幂等性"""
    runtime = AgentRuntimeImpl()
    runtime.initialize()
    runtime.shutdown()
    runtime.shutdown()
    assert runtime.is_running() is False


# ============ 问题3: 未初始化提交任务 ============

def test_submit_without_initialize():
    """未初始化就提交任务"""
    runtime = AgentRuntimeImpl()
    result = runtime.submit_task({"name": "test"})
    assert result is None


def test_submit_after_shutdown():
    """关闭后提交任务"""
    runtime = AgentRuntimeImpl()
    runtime.initialize()
    runtime.shutdown()
    result = runtime.submit_task({"name": "test"})
    assert result is None


# ============ 问题4: TaskDefineImpl 健壮性 ============

def test_create_task_none():
    """创建 None 任务"""
    define = TaskDefineImpl()
    result = define.create_task(None)
    assert result.success is False


def test_create_task_non_dict():
    """创建非 dict 任务"""
    define = TaskDefineImpl()
    result = define.create_task("invalid")
    assert result.success is False


def test_validate_task_invalid_id():
    """验证无效 task_id"""
    define = TaskDefineImpl()
    assert define.validate_task(None) is False
    assert define.validate_task("") is False
    assert define.validate_task(123) is False


# ============ 问题5: TaskStateImpl 状态校验 ============

def test_set_state_invalid_task_id():
    """设置无效 task_id 状态"""
    state = TaskStateImpl()
    with pytest.raises(ValueError):
        state.set_state(None, TaskStateEnum.RUNNING)
    with pytest.raises(ValueError):
        state.set_state("", TaskStateEnum.RUNNING)


def test_set_state_invalid_state_type():
    """设置无效状态类型"""
    state = TaskStateImpl()
    with pytest.raises(ValueError):
        state.set_state("task1", "invalid")
    with pytest.raises(ValueError):
        state.set_state("task1", None)


def test_get_state_invalid_task_id():
    """获取无效 task_id 状态"""
    state = TaskStateImpl()
    assert state.get_state(None) == TaskStateEnum.PENDING
    assert state.get_state("") == TaskStateEnum.PENDING
    assert state.get_state(123) == TaskStateEnum.PENDING


# ============ 问题6: TaskScheduleImpl 重复任务ID ============

def test_duplicate_task_id():
    """重复任务ID"""
    schedule = TaskScheduleImpl()
    request = ScheduleRequestDto(
        task_id="same_id",
        priority=SchedulePriority.NORMAL,
        scheduled_at=1
    )
    result1 = schedule.add_task(request)
    assert result1.success is True

    result2 = schedule.add_task(request)
    assert result2.success is False
    assert "Duplicate" in result2.message


def test_add_task_none_request():
    """添加 None 请求"""
    schedule = TaskScheduleImpl()
    result = schedule.add_task(None)
    assert result.success is False


def test_add_task_empty_task_id():
    """添加空 task_id"""
    schedule = TaskScheduleImpl()
    request = ScheduleRequestDto(
        task_id="",
        priority=SchedulePriority.NORMAL,
        scheduled_at=1
    )
    result = schedule.add_task(request)
    assert result.success is False


# ============ 问题7: TaskRunnerImpl 健壮性 ============

def test_execute_none_request():
    """执行 None 请求"""
    runner = TaskRunnerImpl()
    result = runner.execute_task(None)
    assert result.success is False


def test_execute_empty_task_id():
    """执行空 task_id"""
    runner = TaskRunnerImpl()
    request = ExecuteRequestDto(task_id="", params=())
    result = runner.execute_task(request)
    assert result.success is False


def test_cancel_invalid_task_id():
    """取消无效 task_id"""
    runner = TaskRunnerImpl()
    assert runner.cancel_task(None) is False
    assert runner.cancel_task("") is False
    assert runner.cancel_task(123) is False


def test_get_progress_invalid_task_id():
    """获取无效 task_id 进度"""
    runner = TaskRunnerImpl()
    progress = runner.get_progress(None)
    assert progress.progress == 0


def test_reset_task():
    """重置任务"""
    runner = TaskRunnerImpl()
    request = ExecuteRequestDto(task_id="task1", params=())
    runner.cancel_task("task1")
    assert runner.get_progress("task1").message == "Cancelled"

    runner.reset_task("task1")
    assert runner.get_progress("task1").message == "In progress"


# ============ 问题8: Provider 单例线程安全 ============

def test_provider_singleton():
    """Provider 单例模式"""
    p1 = Provider()
    p2 = Provider()
    assert p1 is p2


def test_provider_clear():
    """Provider 清空"""
    provider = Provider()
    provider.clear()
    provider.register("test", "value")
    assert provider.has("test") is True
    provider.clear()
    assert provider.has("test") is False


# ============ 复杂场景测试 ============

def test_full_lifecycle():
    """完整任务生命周期"""
    runtime = AgentRuntimeImpl()
    runtime.initialize()

    # 创建任务
    task_id = runtime.submit_task({"name": "lifecycle_test", "params": (1, 2, 3)})
    assert task_id is not None
    assert runtime.get_task_status(task_id) == "pending"

    # 关闭后无法提交
    runtime.shutdown()
    task_id2 = runtime.submit_task({"name": "after_shutdown"})
    assert task_id2 is None


def test_multiple_tasks_same_name():
    """同名多任务"""
    runtime = AgentRuntimeImpl()
    runtime.initialize()

    ids = []
    for i in range(5):
        tid = runtime.submit_task({"name": "same_name", "params": (i,)})
        ids.append(tid)

    assert len(set(ids)) == 5
    runtime.shutdown()


def test_rapid_initialize_shutdown():
    """快速初始化/关闭"""
    runtime = AgentRuntimeImpl()
    for _ in range(10):
        runtime.initialize()
        runtime.shutdown()
    assert runtime.is_running() is False
