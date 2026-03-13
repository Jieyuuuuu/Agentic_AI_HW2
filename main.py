import os
from dotenv import load_dotenv
from agent import ReActAgent

def main():
    # Load environment variables
    load_dotenv()
    
    if not os.environ.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY") == "your_gemini_api_key_here":
        print("ERROR: Please set your GEMINI_API_KEY in the .env file.")
        return

    # Initialize the agent
    # Using gemini-2.5-flash-lite as requested
    agent = ReActAgent(model_name="gemini-2.5-flash-lite")
    
    # Task 1: Planning & Quantitative Reasoning
    task1 = "What fraction of Japan's population is Taiwan's population as of 2025?"
    print(f"\n[Running Task 1]: {task1}")
    result1 = agent.execute(task1)
    print(f"\n>> Final Result 1: {result1}\n")
    print("-" * 50)
    
    # Task 2: Technical Specificity
    task2 = "Compare the main display specs of iPhone 15 and Samsung S24."
    print(f"\n[Running Task 2]: {task2}")
    result2 = agent.execute(task2)
    print(f"\n>> Final Result 2: {result2}\n")
    print("-" * 50)

    # Task 3: Resilience & Reflection Test
    task3 = "Who is the CEO of the startup 'Morphic' AI search?"
    print(f"\n[Running Task 3]: {task3}")
    result3 = agent.execute(task3)
    print(f"\n>> Final Result 3: {result3}\n")
    print("-" * 50)

if __name__ == "__main__":
    main()
