"""
复杂业务场景闭环测试
覆盖正向、逆向、中断、重复操作
"""

import pytest
from AgentTaskSystem.agent_runtime.impl.AgentRuntimeImpl import AgentRuntimeImpl
from AgentTaskSystem.common.Provider import Provider
from AgentTaskSystem.common.Logger import LogLevel, get_logger
from AgentTaskSystem.agent_runtime.task_schedule.impl.TaskScheduleImpl import TaskScheduleImpl
from AgentTaskSystem.agent_runtime.task_schedule.interfaces.SchedulePriority import SchedulePriority
from AgentTaskSystem.agent_runtime.task_schedule.interfaces.ScheduleRequestDto import ScheduleRequestDto
from AgentTaskSystem.task_core.task_state.interfaces.TaskStateEnum import TaskStateEnum


# ============ 正向场景 ============

def test_normal_workflow():
    """标准完整工作流"""
    runtime = AgentRuntimeImpl()
    runtime.initialize()

    task_id = runtime.submit_task({"name": "normal_task", "params": (1, 2, 3)})
    assert task_id is not None
    assert runtime.get_task_status(task_id) == "pending"

    runtime.shutdown()


def test_batch_submit():
    """批量提交任务"""
    runtime = AgentRuntimeImpl()
    runtime.initialize()

    task_ids = []
    for i in range(100):
        tid = runtime.submit_task({"name": f"batch_task_{i}", "params": (i,)})
        task_ids.append(tid)

    assert len(set(task_ids)) == 100
    assert all(tid is not None for tid in task_ids)

    runtime.shutdown()


def test_priority_scheduling():
    """优先级调度验证"""
    schedule = TaskScheduleImpl()

    # 按低优先级顺序添加
    for i in range(10):
        request = ScheduleRequestDto(
            task_id=f"task_{i}",
            priority=SchedulePriority.LOW,
            scheduled_at=i
        )
        schedule.add_task(request)

    # 添加高优先级
    high = ScheduleRequestDto(
        task_id="high_priority",
        priority=SchedulePriority.HIGH,
        scheduled_at=100
    )
    schedule.add_task(high)

    # 高优先级应该先出队
    next_task = schedule.get_next_task()
    assert next_task.task_id == "high_priority"


# ============ 逆向场景 ============

def test_invalid_inputs():
    """各种无效输入"""
    runtime = AgentRuntimeImpl()
    runtime.initialize()

    invalid_inputs = [
        None,
        "string",
        123,
        [],
        {"params": "not_tuple"},
        {"name": "x" * 300},  # 超长名称
        {"name": "test", "params": tuple(range(200))},  # 超多参数
    ]

    for inp in invalid_inputs:
        result = runtime.submit_task(inp)
        assert result is None

    runtime.shutdown()


def test_queue_overflow():
    """队列溢出处理"""
    schedule = TaskScheduleImpl()

    # 填满队列
    for i in range(1001):
        request = ScheduleRequestDto(
            task_id=f"overflow_{i}",
            priority=SchedulePriority.NORMAL,
            scheduled_at=i
        )
        result = schedule.add_task(request)
        if i >= 1000:
            assert result.success is False
            assert "full" in result.message.lower() or "Queue is full" in result.message


# ============ 中断场景 ============

def test_interrupt_mid_operation():
    """操作中断"""
    runtime = AgentRuntimeImpl()
    runtime.initialize()

    # 提交一些任务
    ids = []
    for i in range(10):
        tid = runtime.submit_task({"name": f"interrupt_{i}"})
        ids.append(tid)

    # 突然关闭
    runtime.shutdown()

    # 关闭后无法继续
    assert runtime.submit_task({"name": "after_interrupt"}) is None


def test_reinitialize_after_shutdown():
    """关闭后重新初始化"""
    runtime = AgentRuntimeImpl()
    runtime.initialize()
    runtime.shutdown()

    # 重新初始化
    runtime.initialize()
    task_id = runtime.submit_task({"name": "reinit_task"})
    assert task_id is not None
    runtime.shutdown()


# ============ 重复操作场景 ============

def test_duplicate_submissions():
    """重复提交同一任务数据"""
    runtime = AgentRuntimeImpl()
    runtime.initialize()

    task_data = {"name": "duplicate", "params": (1,)}
    id1 = runtime.submit_task(task_data)
    id2 = runtime.submit_task(task_data)

    assert id1 != id2  # 每次应该生成不同ID
    runtime.shutdown()


def test_idempotent_operations():
    """幂等操作验证"""
    runtime = AgentRuntimeImpl()

    # 多次初始化
    for _ in range(5):
        assert runtime.initialize() is True

    # 多次关闭
    for _ in range(5):
        runtime.shutdown()

    assert runtime.is_running() is False


# ============ 混乱场景 ============

def test_mixed_valid_invalid():
    """混合有效和无效输入"""
    runtime = AgentRuntimeImpl()
    runtime.initialize()

    valid_count = 0
    inputs = [
        {"name": "valid1"},
        None,
        {"name": "valid2"},
        "invalid",
        {"name": "valid3"},
        123,
    ]

    for inp in inputs:
        result = runtime.submit_task(inp)
        if result is not None:
            valid_count += 1

    assert valid_count == 3
    runtime.shutdown()


def test_rapid_state_changes():
    """快速状态变更"""
    from AgentTaskSystem.task_core.task_state.impl.TaskStateImpl import TaskStateImpl
    state = TaskStateImpl()

    task_id = "rapid_task"
    states = [
        TaskStateEnum.PENDING,
        TaskStateEnum.RUNNING,
        TaskStateEnum.COMPLETED,
        TaskStateEnum.FAILED,
        TaskStateEnum.RUNNING,
        TaskStateEnum.COMPLETED,
    ]

    for s in states:
        transition = state.set_state(task_id, s)
        assert transition.to_state == s

    transitions = state.get_transitions(task_id)
    assert len(transitions) == 6


def test_concurrent_provider_access():
    """Provider并发访问"""
    provider = Provider()
    provider.clear()

    # 模拟并发注册
    for i in range(50):
        provider.register(f"service_{i}", f"value_{i}")

    # 验证所有注册成功
    for i in range(50):
        assert provider.has(f"service_{i}")
        assert provider.get(f"service_{i}") == f"value_{i}"

    provider.clear()


# ============ 日志验证场景 ============

def test_log_output():
    """验证日志输出"""
    logger = get_logger()
    logger.set_level(LogLevel.DEBUG)

    # 这些调用应该产生日志输出
    logger.debug("Test", "debug message")
    logger.info("Test", "info message")
    logger.warn("Test", "warn message")
    logger.error("Test", "error message")

    # 设置高级别后debug不应输出
    logger.set_level(LogLevel.ERROR)
    logger.debug("Test", "should not appear")


# ============ 压力场景 ============

def test_large_scale_submit():
    """大规模提交"""
    runtime = AgentRuntimeImpl()
    runtime.initialize()

    ids = []
    for i in range(500):
        tid = runtime.submit_task({"name": f"scale_{i}", "params": (i, i+1)})
        if tid:
            ids.append(tid)

    assert len(ids) == 500
    runtime.shutdown()


def test_schedule_clear_and_refill():
    """调度器清空再填充"""
    schedule = TaskScheduleImpl()

    # 填充
    for i in range(50):
        request = ScheduleRequestDto(
            task_id=f"refill_{i}",
            priority=SchedulePriority.NORMAL,
            scheduled_at=i
        )
        schedule.add_task(request)

    assert schedule.get_queue_size() == 50

    # 清空
    schedule.clear()
    assert schedule.get_queue_size() == 0

    # 再填充
    for i in range(30):
        request = ScheduleRequestDto(
            task_id=f"refill2_{i}",
            priority=SchedulePriority.HIGH,
            scheduled_at=i
        )
        schedule.add_task(request)

    assert schedule.get_queue_size() == 30
