#!/usr/bin/env python3
"""Token cost estimator CLI

Usage:
    estimate_cost.py <model_name> <input_tokens> <output_tokens>

Returns JSON with costs rounded to 4 decimal places.
"""
import sys
import json

# pricing per 1,000,000 tokens (USD)
MODEL_PRICING = {
    "gpt-4o": {"input": 5.00, "output": 15.00},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    "deepseek-v3": {"input": 0.27, "output": 1.10}
}


def calculate(model_name, input_tokens, output_tokens):
    if model_name not in MODEL_PRICING:
        return {"error": f"Model {model_name} not found."}

    pricing = MODEL_PRICING[model_name]
    in_cost = (input_tokens / 1_000_000) * pricing["input"]
    out_cost = (output_tokens / 1_000_000) * pricing["output"]
    total = in_cost + out_cost

    return {
        "model": model_name,
        "input_cost": round(in_cost, 4),
        "output_cost": round(out_cost, 4),
        "total_cost_usd": round(total, 4),
        "currency": "USD"
    }


if __name__ == "__main__":
    try:
        if len(sys.argv) < 4:
            raise ValueError("Usage: estimate_cost.py <model_name> <input_tokens> <output_tokens>")

        m = sys.argv[1]

        def parse_int(x):
            if isinstance(x, int):
                return x
            s = str(x).replace(',', '')
            return int(float(s))

        i = parse_int(sys.argv[2])
        o = parse_int(sys.argv[3])
        print(json.dumps(calculate(m, i, o), ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
