import os
import re
from openai import OpenAI
from tools import search_web

# Define the System Prompt with a Few-Shot Example (One-shot)
SYSTEM_PROMPT = """You are an intelligent ReAct (Reasoning and Acting) agent.
Your task is to answer user questions by thinking step-by-step and gathering information.
You must use the following format strictly:

Thought: Consider what you need to do next. Do you need to search? Or do you have the answer?
Action: The action to take. The only available action is `Search[query]`.
Observation: The result of the action. (You do not generate this, the system will provide it).
... (this Thought/Action/Observation can repeat up to 5 times)
Thought: I know the final answer.
Final Answer: The final detailed answer to the original input question.

---
FEW-SHOT EXAMPLE:

Question: What is the capital of France and what is its population?
Thought: I need to find the capital of France first.
Action: Search[capital of France]
Observation: Paris is the capital and most populous city of France, with an estimated population of 2,102,650 residents as of 2023.
Thought: The search result gives me the capital (Paris) and its population. I now have enough information to answer the question.
Final Answer: The capital of France is Paris, and its population is estimated to be around 2.1 million.
---

Instructions:
- If a search fails or doesn't return the information you need, Reflect on why it failed and try a different search query.
- Never fake or hallucinate Observations. Always Output Action: Search[query] and stop.
"""

class ReActAgent:
    def __init__(self, model_name="google/gemini-2.5-flash"):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ.get("OPENROUTER_API_KEY"),
        )
        self.model_name = model_name
        self.system_prompt = SYSTEM_PROMPT
        self.max_steps = 5

    def execute(self, question: str) -> str:
        print(f"\n========== BEGIN TASK ==========")
        print(f"Question: {question}")
        
        # Initialize the prompt history with the system prompt and the question
        prompt_history = self.system_prompt + f"\n\nQuestion: {question}\n"
        
        step = 0
        while step < self.max_steps:
            step += 1
            print(f"\n--- Step {step} ---")
            
            # 1. Call LLM
            # We use stop to prevent the LLM from generating the Observation itself
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt_history}
                ],
                stop=["Observation:"],
                temperature=0.2, # Low temperature for more deterministic reasoning
                max_tokens=2000, # Limit generation to prevent 402 Insufficient Credit errors
            )
            
            generation = response.choices[0].message.content.strip()
            print(generation)
            
            # Update history with the LLM's generation
            prompt_history += generation + "\n"
            
            # Check if the agent found the final answer
            if "Final Answer:" in generation:
                print("\n========== TASK COMPLETED ==========")
                return generation.split("Final Answer:")[-1].strip()
            
            # 2. Parse Action
            # Look for "Action: Search[...]"
            action_match = re.search(r"Action:\s*Search\[(.*?)\]", generation)
            
            if action_match:
                query = action_match.group(1)
                
                # 3. Call Tool
                print(f">> Executing Search for: '{query}'...")
                observation_result = search_web(query)
                print(f"Observation: {observation_result[:200]}... (truncated for display)")
                
                # 4. Update History with the true Observation
                observation_text = f"Observation: {observation_result}\n"
                prompt_history += observation_text
            else:
                # If no valid action and no final answer, force the agent to re-evaluate
                warning = "Observation: Invalid format. Please provide an 'Action: Search[query]' or a 'Final Answer:'"
                print(warning)
                prompt_history += warning + "\n"

        print("\n========== TASK FAILED (MAX STEPS REACHED) ==========")
        return "I could not find the answer within the maximum allowed steps."
