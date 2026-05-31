import sys
import os
sys.path.insert(0, "/workspace")

from AgentTaskSystem.agent_runtime.impl.agent_runtime_impl import AgentRuntimeImpl
from AgentTaskSystem.common.service_provider import ServiceProvider


def main():
    print("=" * 60)
    print("AgentTaskSystem 使用示例")
    print("=" * 60)
    
    # 方式1: 直接使用 AgentRuntimeImpl
    print("\n1. 直接使用 AgentRuntimeImpl")
    runtime = AgentRuntimeImpl()
    print("   创建 Runtime 实例: 成功")
    
    # 初始化运行时
    print("\n2. 初始化运行时")
    initialized = runtime.initialize()
    print(f"   初始化结果: {initialized}")
    print(f"   运行状态: {runtime.is_running()}")
    
    # 提交任务
    print("\n3. 提交任务")
    task_data = {
        "name": "示例任务",
        "params": ["参数1", "参数2"]
    }
    task_id = runtime.submit_task(task_data)
    print(f"   任务提交成功, 任务ID: {task_id}")
    
    # 查询任务状态
    print("\n4. 查询任务状态")
    if task_id:
        status = runtime.get_task_status(task_id)
        print(f"   任务 {task_id} 状态: {status}")
    
    # 关闭运行时
    print("\n5. 关闭运行时")
    runtime.shutdown()
    print(f"   运行状态: {runtime.is_running()}")
    
    # 方式2: 使用 ServiceProvider 进行依赖注入
    print("\n" + "=" * 60)
    print("6. 使用 ServiceProvider")
    print("=" * 60)
    
    service_provider = ServiceProvider.get_instance()
    service_provider.initialize()
    
    agent_runtime = service_provider.get("IAgentRuntime")
    print("   从 ServiceProvider 获取 IAgentRuntime: 成功")
    
    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
