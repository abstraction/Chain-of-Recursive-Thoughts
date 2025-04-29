# Chain of Recursive Thoughts: How It Works

This document explains the logic behind the Chain of Recursive Thoughts (CoRT) technique implemented in this codebase.

## Core Concept

The Chain of Recursive Thoughts is a technique that enhances an LLM's reasoning capabilities by making it:

1. Generate an initial response
2. Create multiple alternative responses
3. Evaluate all responses (including the initial one)
4. Select the best response
5. Repeat this process for multiple rounds

This recursive thinking process mimics how humans often refine their thoughts by considering alternatives and selecting the best approach.

## Key Components

### 1. Thinking Rounds

**What it is:** The number of iterations the LLM will go through to refine its response.

**How it works:**
- The LLM itself determines how many rounds are needed (1-5) based on the complexity of the user's query
- For simple queries, it might only need 1 round
- For complex queries, it might need 5 rounds
- If the LLM fails to determine a valid number, it defaults to 3 rounds

**Why it matters:** Different queries require different amounts of thinking. A simple factual question might only need one round, while a complex reasoning task benefits from multiple rounds of refinement.

### 2. Alternatives

**What it is:** The number of different responses generated in each thinking round.

**How it works:**
- In each round, the LLM generates a specified number of alternative responses (default: 3)
- Each alternative is a complete, independent response to the original query
- The alternatives are generated with slightly increasing temperature values to encourage diversity

**Why it matters:** Having multiple alternatives increases the chance of finding a better response than the current best one. It's like brainstorming multiple solutions to a problem.

### 3. Evaluation

**What it is:** The process of comparing the current best response with the alternatives.

**How it works:**
- The LLM is presented with the current best response and all alternatives
- It's asked to select the best one based on accuracy, clarity, and completeness
- It must provide a one-sentence explanation for its choice
- The selected response becomes the new "current best" for the next round

**Why it matters:** This forces the LLM to critically evaluate its own outputs and select the most effective response, rather than just generating a single answer.

## The Complete Process

1. **Initial Response Generation**
   - The LLM generates an initial response to the user's query
   - This becomes the "current best" response

2. **Determining Thinking Rounds**
   - The LLM analyzes the query complexity and decides how many rounds of thinking are needed (1-5)

3. **Iterative Improvement**
   - For each round:
     - Generate N alternative responses (where N is the number of alternatives)
     - Evaluate all responses (current best + alternatives)
     - Select the best response with an explanation
     - Update the current best if a better alternative was found

4. **Final Response**
   - After all rounds are complete, the current best response is presented as the final answer
   - The complete thinking process is also available for review

## Differences from Standard LLM Interactions

1. **Multiple Perspectives:** Instead of a single response, the LLM considers multiple approaches.

2. **Self-Evaluation:** The LLM critically evaluates its own responses.

3. **Iterative Refinement:** The response improves over multiple rounds of thinking.

4. **Transparency:** The entire thinking process is visible, not just the final answer.

## Temperature Cascading

An important aspect of the implementation is "temperature cascading" for generating alternatives:

- Each alternative is generated with a slightly higher temperature
- For example: 0.7, 0.8, 0.9 for three alternatives
- This encourages increasing creativity and diversity in the alternatives
- It helps avoid getting stuck in local optima by exploring more of the possibility space

## Practical Example

For the query "How to tie a knot?":

1. **Initial Response:** "Cross one end over the other, loop it through, pull tight. Adjust as needed for security."

2. **Round 1 Alternatives:**
   - "Create a loop, thread one end through, tighten by pulling both ends. Practice for precision and firmness."
   - "Overlap ends, create a loop, thread one through, and pull firmly. Adjust for desired tightness and stability."

3. **Evaluation:** The LLM keeps the initial response because it's concise and clear.

4. **Round 2 Alternatives:**
   - "Overlap ends, form a loop, thread one end through, tighten. Ensure it's secure by pulling both ends."
   - "Create a loop, thread the end through, pull tight. Practice different knots for various uses and better security."

5. **Final Evaluation:** The LLM selects the first alternative from Round 2 because it provides a clear, step-by-step guide while ensuring security.

This process results in a better response than would likely have been generated in a single pass.
