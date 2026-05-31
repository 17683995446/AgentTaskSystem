"""
极简使用示例 - 只需要 4 步！
"""

from AgentTaskSystem import initialize_services


def simple_example():
    """
    最简单的使用方式
    """
    print("=== AgentTaskSystem 极简示例 ===\n")

    # 第 1 步：初始化（一行搞定）
    print("1. 初始化系统...")
    provider = initialize_services()
    runtime = provider.get("agent_runtime")
    print("   ✓ 初始化完成！\n")

    # 第 2 步：启动运行时
    print("2. 启动系统...")
    runtime.initialize()
    print(f"   ✓ 系统运行中: {runtime.is_running()}\n")

    # 第 3 步：提交任务（就这么简单！）
    print("3. 提交任务...")
    task_id = runtime.submit_task({
        "name": "我的第一个任务",
        "params": (1, 2, 3, "hello")
    })
    print(f"   ✓ 任务ID: {task_id}\n")

    # 第 4 步：查看状态
    print("4. 查看任务状态...")
    status = runtime.get_task_status(task_id)
    print(f"   ✓ 任务状态: {status}\n")

    # 第 5 步：关闭（可选，好习惯）
    print("5. 关闭系统...")
    runtime.shutdown()
    print(f"   ✓ 已关闭: {not runtime.is_running()}\n")

    print("=== 完成！就这么简单！===")


if __name__ == "__main__":
    simple_example()
