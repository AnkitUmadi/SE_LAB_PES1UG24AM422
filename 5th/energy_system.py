"""Energy tariff and meter reading management system."""

import ast
import json
from datetime import datetime

# Global state
meters = {}
RATE_TIERS = [3.5, 5.0, 7.5]
SPIKE_LIMIT = 500


def record_reading(meter_id, units, history=None):
    """Record a meter reading and update total meter units."""
    if history is None:
        history = []
    history.append((meter_id, units, str(datetime.now())))
    meters[meter_id] = meters.get(meter_id, 0) + units
    return history


def compute_bill(meter_id, tier_rates):
    """Compute the energy bill for a meter based on tiered rates."""
    units = meters[meter_id]
    if units <= 100:
        return units * tier_rates[0]
    if units <= 300:
        return 100 * tier_rates[0] + (units - 100) * tier_rates[1]
    base_cost = 100 * tier_rates[0] + 200 * tier_rates[1]
    return base_cost + (units - 300) * tier_rates[2]


def raise_rates(percent):
    """Increase all tariff tier rates by a given percentage."""
    multiplier = 1 + percent / 100
    for idx, rate in enumerate(RATE_TIERS):
        RATE_TIERS[idx] = rate * multiplier


def flag_spikes():
    """Return a list of meter IDs whose readings exceed SPIKE_LIMIT."""
    return [
        meter_id for meter_id, units in meters.items()
        if units > SPIKE_LIMIT
    ]


def load_meter_data(file="meters.json"):
    """Load meter data from a JSON file."""
    try:
        with open(file, "r", encoding="utf-8") as file_handle:
            loaded_data = json.loads(file_handle.read())
            meters.clear()
            meters.update(loaded_data)
    except (OSError, json.JSONDecodeError):
        meters.clear()


def save_meter_data(file="meters.json"):
    """Save current meter data to a JSON file."""
    with open(file, "w", encoding="utf-8") as file_handle:
        file_handle.write(json.dumps(meters))


def main():
    """Run main workflow for energy tariff calculation."""
    history = record_reading("M-01", 120)
    record_reading("M-02", 640, history)
    record_reading("M-03", -50, history)
    print("Readings stored so far:", len(history))
    raise_rates(10)
    print(f"Bill M-01: {compute_bill('M-01', RATE_TIERS):.2f}")
    print(f"Bill M-03: {compute_bill('M-03', RATE_TIERS):.2f}")
    print("Spikes:", flag_spikes())
    prompt = "Extra units for M-01 as an expression (Enter for 0): "
    adjustment = input(prompt) or "0"
    record_reading("M-01", ast.literal_eval(adjustment), history)
    save_meter_data()
    load_meter_data()
    bill_after = compute_bill("M-01", RATE_TIERS)
    print(f"Bill M-01 after reload: {bill_after:.2f}")


if __name__ == "__main__":
    main()
