# AgentTaskSystem 使用说明

## 系统概述
---------
AgentTaskSystem 是一个严格符合 V2.1 终极零柔性绝对刚性版规范构建的 AI Agent 任务管理系统。

## 主要组件说明
-----------

### 核心模块

1. **AgentRuntime** - 运行时入口 ([IAgentRuntime](file:///workspace/AgentTaskSystem/agent_runtime/interfaces/i_agent_runtime.py))
   - 系统主入口，负责编排整个任务流程
   - 主要方法：
     - `initialize()` - 初始化运行时
     - `submit_task(task_data)` - 提交任务
     - `get_task_status(task_id)` - 查询任务状态
     - `shutdown()` - 关闭运行时
     - `is_running()` - 检查运行状态

2. **TaskCore** - 任务核心
   - **TaskDefine** - 任务定义与校验
     - [ITaskDefine](file:///workspace/AgentTaskSystem/task_core/task_define/interfaces/i_task_define.py) - 任务定义接口
     - [ITaskValidator](file:///workspace/AgentTaskSystem/task_core/task_define/interfaces/i_task_validator.py) - 任务校验接口
   
   - **TaskState** - 状态管理
     - [ITaskState](file:///workspace/AgentTaskSystem/task_core/task_state/interfaces/i_task_state.py) - 状态管理接口
     - [TaskStateEnum](file:///workspace/AgentTaskSystem/task_core/task_state/interfaces/task_state_enum.py) - 任务状态枚举

3. **AgentRuntime** 子模块
   - **TaskSchedule** - 任务调度
     - [ITaskSchedule](file:///workspace/AgentTaskSystem/agent_runtime/task_schedule/interfaces/i_task_schedule.py) - 调度接口
     - [SchedulePriority](file:///workspace/AgentTaskSystem/agent_runtime/task_schedule/interfaces/schedule_priority.py) - 优先级枚举
   
   - **TaskRunner** - 任务执行
     - [ITaskRunner](file:///workspace/AgentTaskSystem/agent_runtime/task_runner/interfaces/i_task_runner.py) - 执行接口

## 使用方式
---------

### 方式1: 直接使用 AgentRuntimeImpl

```python
from AgentTaskSystem.agent_runtime.impl.agent_runtime_impl import AgentRuntimeImpl

# 创建并初始化
runtime = AgentRuntimeImpl()
runtime.initialize()

# 提交任务
task_data = {
    "name": "任务名称",
    "params": ["参数1", "参数2"]
}
task_id = runtime.submit_task(task_data)

# 查询状态
status = runtime.get_task_status(task_id)

# 关闭
runtime.shutdown()
```

### 方式2: 使用 ServiceProvider 依赖注入

```python
from AgentTaskSystem.common.service_provider import ServiceProvider

service_provider = ServiceProvider.get_instance()
service_provider.initialize()

# 获取服务
agent_runtime = service_provider.get("IAgentRuntime")
```

## 数据结构
----------

### 任务数据格式

```python
task_data = {
    "name": str,      # 任务名称
    "params": list   # 任务参数列表
}
```

### 主要接口

- 所有模块的接口都定义在各自的 `interfaces/` 目录下，实现则放在 `impl/` 目录下。
- 跨模块调用只能通过 `interfaces/` 下的接口，不能直接调用 impl。

## 运行测试
-----------

### 集成测试

```bash
cd /workspace
python3 AgentTaskSystem/tests/test_integration.py
```

### 示例程序

```bash
cd /workspace
python3 example_usage.py
```
