---
name: token-cost-estimator
description: Calculate token usage costs for popular AI models. Use when users ask for cost or budget estimates or provide token counts.
---

# Token Cost Estimator

## When to use
- The user provides input and/or output token counts.
- The user wants to compare costs across different models.
- The user requires price precision rounded to four decimal places.

## Inputs
- `model_name`: Model identifier (e.g., `gpt-4o`, `claude-3-5-sonnet`)
- `input_tokens`: Number of input (prompt) tokens (integer)
- `output_tokens`: Number of output (completion) tokens (integer)

## Workflow
1. Detect the model and token counts from the user's message.
2. Call `scripts/estimate_cost.py` to perform a deterministic calculation.
3. Parse the returned JSON and present the results (as text or a table).

## Return schema
The script returns a JSON object with the following fields:

- `model` (string)
- `input_cost` (number, USD, rounded to 4 decimals)
- `output_cost` (number, USD, rounded to 4 decimals)
- `total_cost_usd` (number, USD, rounded to 4 decimals)
- `currency` (string, e.g. `USD`)

Example output:

{"model":"gpt-4o","input_cost":2.5,"output_cost":1.5,"total_cost_usd":4.0,"currency":"USD"}

## Supported models and pricing (per 1,000,000 tokens, USD)
- `gpt-4o`: input 5.00, output 15.00
- `gpt-3.5-turbo`: input 0.50, output 1.50
- `claude-3-5-sonnet`: input 3.00, output 15.00
- `deepseek-v3`: input 0.27, output 1.10

## Error handling and limits
- Only the built-in pricing models above are supported. If the user requests an unsupported model, return an error message or ask for a supported model.
- If token counts are missing or malformed, prompt the user with a short template, for example:

"Please provide token counts in the format: input=12345 output=6789"

## Example CLI invocation

python3 .agents/skills/token-cost-estimator/scripts/estimate_cost.py gpt-4o 500000 100000

## Notes
- Keep `MODEL_PRICING` in `scripts/estimate_cost.py` synchronized with this document.
- The skill is intended to offload deterministic arithmetic to a script to avoid model-generated arithmetic errors.
