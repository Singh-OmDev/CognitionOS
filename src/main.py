import asyncio
import os
from src.core.orchestration import Orchestrator
from dotenv import load_dotenv

async def main():
    load_dotenv()
    
    print("Initializing CognitionOS...")
    orchestrator = Orchestrator()
    
    print("\nCognitionOS Ready. Type 'exit' to quit.")
    
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        print("\nProcessing...")
        try:
            async for step_result in orchestrator.run_workflow(user_input):
                pass # The orchestrator logic prints steps, or we can print here
                
                if "code_output" in step_result:
                    print(f"\n[FINAL OUTPUT]\n{step_result['code_output']}")
                    
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
