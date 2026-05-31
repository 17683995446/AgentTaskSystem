"""
Example usage of AgentTaskSystem
"""

from AgentTaskSystem import initialize_services
from AgentTaskSystem.agent_runtime import IAgentRuntime
from AgentTaskSystem.task_core import ITaskDefine, ITaskState, TaskStateEnum
from AgentTaskSystem.common import Provider


def main():
    """
    Main example function
    """
    print("=" * 60)
    print("AgentTaskSystem Example Usage")
    print("=" * 60)
    
    # Step 1: Initialize all services
    print("\n1. Initializing services...")
    provider = initialize_services()
    print("   ✓ Services initialized successfully!")
    
    # Step 2: Get runtime
    print("\n2. Getting AgentRuntime...")
    runtime = provider.get("agent_runtime")
    print("   ✓ AgentRuntime obtained!")
    
    # Step 3: Initialize runtime
    print("\n3. Starting runtime...")
    runtime.initialize()
    print(f"   ✓ Runtime running: {runtime.is_running()}")
    
    # Step 4: Submit tasks
    print("\n4. Submitting tasks...")
    task_ids = []
    for i in range(3):
        task_data = {
            "name": f"Example Task {i+1}",
            "params": (i+1, i+2, i+3)
        }
        task_id = runtime.submit_task(task_data)
        task_ids.append(task_id)
        print(f"   ✓ Submitted task: {task_id}")
    
    # Step 5: Check task statuses
    print("\n5. Checking task statuses...")
    for task_id in task_ids:
        status = runtime.get_task_status(task_id)
        print(f"   - Task {task_id} status: {status}")
    
    # Step 6: Shutdown
    print("\n6. Shutting down runtime...")
    runtime.shutdown()
    print(f"   ✓ Runtime running: {runtime.is_running()}")
    
    # Optional: Demonstrate ServiceProvider
    print("\n" + "=" * 60)
    print("ServiceProvider Demo")
    print("=" * 60)
    
    provider2 = Provider()
    provider2.register("demo_key", "demo_value")
    
    print(f"\n- Service exists: {provider2.has('demo_key')}")
    print(f"- Service value: {provider2.get('demo_key')}")
    
    provider2.clear()
    print(f"- Services cleared: {provider2.has('demo_key')} is now {provider2.has('demo_key')}")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
