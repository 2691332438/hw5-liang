## Token Cost Estimator Skill

### What this skill does

The token-cost-estimator is a small, deterministic utility that calculates the USD cost for model usage based on input and output token counts. It reads pricing constants (per 1,000,000 tokens) embedded in the script and returns a JSON object with the input cost, output cost, and total cost rounded to four decimal places.

### Why this skill was chosen

This skill is designed to offload exact arithmetic to a local script to avoid model-generated arithmetic errors and to provide a reproducible, auditable calculation for budgeting and cost estimation. Keeping the pricing in-code makes the behavior explicit and easy to update.

### How to use

From the repository root, run the CLI wrapper:

```bash
python3 .agents/skills/token-cost-estimator/scripts/estimate_cost.py <model_name> <input_tokens> <output_tokens>
```

Example:

```bash
python3 .agents/skills/token-cost-estimator/scripts/estimate_cost.py gpt-4o 1000000 500000
```

The script prints a JSON object with these fields:
- `model` — model identifier
- `input_cost` — cost for input tokens (USD, rounded to 4 decimals)
- `output_cost` — cost for output tokens (USD, rounded to 4 decimals)
- `total_cost_usd` — total cost (USD, rounded to 4 decimals)
- `currency` — currency string (currently `USD`)

### What the script does

The script (`scripts/estimate_cost.py`) contains a `MODEL_PRICING` map keyed by model name. Each entry specifies the per-1,000,000-token price for input and output tokens. The CLI parses token counts, computes costs as (tokens / 1_000_000) * price, and returns the results as JSON. The script handles simple input sanitization (commas, floats) and returns an error JSON for unsupported models or bad input.

### What worked well

- Deterministic arithmetic: the script produces exact, auditable numbers given pricing constants.
- Simple CLI: easy to call from other tools or CI pipelines.
- Rounding behavior: returns results rounded to four decimals as required by the skill documentation.

### Limitations and remaining work

- Pricing is hard-coded in `scripts/estimate_cost.py` and must be updated manually to stay current with provider pricing.
- The script only supports models listed in `MODEL_PRICING`; unsupported models return an error.
- Rounding to 4 decimals causes very small per-token costs (e.g., single token) to round to 0.0000 — consider returning higher precision when reporting micro-costs.
- No currency conversion, VAT, or account-specific discounts are modeled.

### Video / Demo

Add your video link here: VIDEO_LINK_HERE

Replace `VIDEO_LINK_HERE` with the URL of your demo video.

---

帮我补充（简短中文说明）

这个工具用于根据输入和输出的 token 数量，快速估算使用特定模型的费用。使用方法非常简单：在仓库根目录运行上面的命令，脚本会返回 JSON 格式的费用结果。注意，目前价格写死在脚本里，且结果保留 4 位小数，单 token 的费用可能会四舍五入为 0。若需要我可以：

- 帮你把价格换成从网络读取（需注意离线/凭证问题）
- 把输出精度提高到 6 位或更多
- 批量计算多模型/多场景并导出 CSV

如需我代为更新或扩展，告诉我你想要的改动。
