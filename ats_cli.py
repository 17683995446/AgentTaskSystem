#!/usr/bin/env python3
"""
AgentTaskSystem CLI - 命令行接口

用法:
    python ats_cli.py init              # 初始化系统
    python ats_cli.py submit <name>     # 提交任务
    python ats_cli.py status <task_id>  # 查看任务状态
    python ats_cli.py list              # 列出所有任务
    python ats_cli.py shutdown          # 关闭系统
    python ats_cli.py demo              # 运行演示
"""

import sys
import json
from AgentTaskSystem import initialize_services


class ATSCli:
    def __init__(self):
        self.provider = None
        self.runtime = None
        self.tasks = {}

    def init(self):
        """初始化系统"""
        print("🚀 正在初始化 AgentTaskSystem...")
        self.provider = initialize_services()
        self.runtime = self.provider.get("agent_runtime")
        self.runtime.initialize()
        print(f"✅ 系统已启动，运行状态: {self.runtime.is_running()}")

    def submit(self, name, *params):
        """提交任务"""
        if not self.runtime or not self.runtime.is_running():
            print("❌ 错误: 系统未初始化，请先运行 'init'")
            return

        task_data = {
            "name": name,
            "params": params if params else ()
        }
        task_id = self.runtime.submit_task(task_data)
        if task_id:
            self.tasks[task_id] = {"name": name, "status": "pending"}
            print(f"✅ 任务提交成功!")
            print(f"   📋 任务ID: {task_id}")
            print(f"   📛 任务名: {name}")
            print(f"   📦 参数: {params}")
        else:
            print("❌ 任务提交失败")

    def status(self, task_id):
        """查看任务状态"""
        if not self.runtime or not self.runtime.is_running():
            print("❌ 错误: 系统未初始化")
            return

        status = self.runtime.get_task_status(task_id)
        if status:
            print(f"📊 任务 {task_id} 的状态: {status}")
        else:
            print(f"❌ 未找到任务: {task_id}")

    def list_tasks(self):
        """列出所有任务"""
        if not self.tasks:
            print("📭 暂无任务")
            return

        print(f"📋 任务列表 (共 {len(self.tasks)} 个):")
        print("-" * 60)
        for task_id, info in self.tasks.items():
            status = self.runtime.get_task_status(task_id) if self.runtime else "unknown"
            print(f"  📛 {info['name']}")
            print(f"     ID: {task_id}")
            print(f"     状态: {status}")
            print()

    def shutdown(self):
        """关闭系统"""
        if self.runtime:
            self.runtime.shutdown()
            print("🛑 系统已关闭")
        else:
            print("⚠️  系统未运行")

    def demo(self):
        """运行演示"""
        print("=" * 60)
        print("🎬 AgentTaskSystem 演示")
        print("=" * 60)

        self.init()
        print()

        # 提交几个示例任务
        print("📤 提交示例任务...")
        self.submit("数据分析任务", "data.csv", "report.xlsx")
        self.submit("邮件发送任务", "user@example.com", "Hello!")
        self.submit("文件处理任务", "/path/to/file.txt")
        print()

        # 查看任务列表
        self.list_tasks()

        # 关闭
        print("🔚 演示结束，关闭系统...")
        self.shutdown()
        print("=" * 60)


def print_help():
    """打印帮助信息"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║           AgentTaskSystem CLI - 命令行工具                   ║
╠══════════════════════════════════════════════════════════════╣
║  用法: python ats_cli.py <命令> [参数...]                    ║
╠══════════════════════════════════════════════════════════════╣
║  命令:                                                       ║
║    init              初始化并启动系统                        ║
║    submit <名称>     提交任务 (可跟参数)                     ║
║    status <任务ID>   查看任务状态                            ║
║    list              列出所有任务                            ║
║    shutdown          关闭系统                                ║
║    demo              运行完整演示                            ║
║    help              显示此帮助信息                          ║
╠══════════════════════════════════════════════════════════════╣
║  示例:                                                       ║
║    python ats_cli.py init                                  ║
║    python ats_cli.py submit "我的任务" arg1 arg2           ║
║    python ats_cli.py status <task_id>                      ║
║    python ats_cli.py list                                  ║
║    python ats_cli.py shutdown                              ║
║    python ats_cli.py demo                                  ║
╚══════════════════════════════════════════════════════════════╝
""")


def main():
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1].lower()
    cli = ATSCli()

    if command == "init":
        cli.init()

    elif command == "submit":
        if len(sys.argv) < 3:
            print("❌ 错误: 请提供任务名称")
            print("   用法: python ats_cli.py submit <任务名称> [参数...]")
            return
        name = sys.argv[2]
        params = sys.argv[3:] if len(sys.argv) > 3 else ()
        cli.init()
        cli.submit(name, *params)

    elif command == "status":
        if len(sys.argv) < 3:
            print("❌ 错误: 请提供任务ID")
            print("   用法: python ats_cli.py status <任务ID>")
            return
        cli.init()
        cli.status(sys.argv[2])

    elif command == "list":
        cli.init()
        cli.list_tasks()

    elif command == "shutdown":
        cli.shutdown()

    elif command == "demo":
        cli.demo()

    elif command in ("help", "-h", "--help"):
        print_help()

    else:
        print(f"❌ 未知命令: {command}")
        print("   运行 'python ats_cli.py help' 查看帮助")


if __name__ == "__main__":
    main()
