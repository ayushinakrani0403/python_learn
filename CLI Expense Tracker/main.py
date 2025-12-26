import argparse
import json
from typing import List, Dict
from datetime import datetime
from pathlib import Path
import logging
from functools import wraps



DATA_FILE = "data.json"
LOG_FILE = "tracker.log"

# ==============================
# LOGGING SETUP
# ==============================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)

# ==============================
# DECORATORS
# ==============================

def log_action(func):
    """Decorator to log function execution."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info("Running %s", func.__name__)
        return func(*args, **kwargs)
    return wrapper

# ==============================
# FILE HANDLING (JSON)
# ==============================

def load_expenses(file_path: Path) -> List[Dict]:
    """Load expenses and auto-fix missing IDs."""
    if not file_path.exists():
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            expenses = json.load(f)

        # 🔥 AUTO-MIGRATION FOR OLD DATA
        next_id = 1
        for exp in expenses:
            if "id" not in exp:
                exp["id"] = next_id
                next_id += 1

        return expenses

    except (IOError, json.JSONDecodeError) as exc:
        logger.error("Failed to load JSON file: %s", exc)
        raise


def save_expenses(file_path: Path, expenses: List[Dict]) -> None:
    """Save expenses to JSON file."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(expenses, f, indent=2)
    except IOError as exc:
        logger.error("Failed to save JSON file: %s", exc)
        raise

# ==============================
# CORE LOGIC
# ==============================

@log_action
def add_expense(
    expenses: List[Dict],
    amount: float,
    category: str,
    note: str
) -> None:
    """Add a new expense."""
    if amount <= 0:
        raise ValueError("Amount must be positive")

    next_id = max((e.get("id", 0) for e in expenses), default=0) + 1

    expense = {
        "id": next_id,
        "amount": amount,
        "category": category,
        "note": note,
        "date": datetime.now().isoformat(timespec="seconds"),
    }

    expenses.append(expense)
    logger.info("Expense added: %s", expense)


@log_action
def list_expenses(expenses: List[Dict]) -> None:
    """List all expenses."""
    if not expenses:
        print("No expenses found")
        return

    print("\nID | DATE                | CATEGORY | AMOUNT | NOTE")
    print("-" * 65)

    for exp in expenses:
        print(
            f"{exp.get('id', 'NA'):2} | {exp['date']:19} | "
            f"{exp['category']:8} | {exp['amount']:7.2f} | {exp['note']}"
        )


@log_action
def delete_expense(expenses: List[Dict], expense_id: int) -> None:
    """Delete expense by ID."""
    for i, exp in enumerate(expenses):
        if exp.get("id") == expense_id:
            removed = expenses.pop(i)
            logger.info("Deleted expense: %s", removed)
            return

    raise ValueError(f"Expense with ID {expense_id} not found")

# ==============================
# CLI ARGUMENTS
# ==============================

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CLI Expense Tracker")

    # JSON file is configurable from here
    parser.add_argument(
        "--file",
        default=DATA_FILE,
        help=f"JSON data file (default: {DATA_FILE})",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add command
    add_cmd = subparsers.add_parser("add", help="Add new expense")
    add_cmd.add_argument("--amount", type=float, required=True)
    add_cmd.add_argument("--category", required=True)
    add_cmd.add_argument("--note", default="")

    # List command
    subparsers.add_parser("list", help="List expenses")

    # Delete command
    del_cmd = subparsers.add_parser("delete", help="Delete expense by ID")
    del_cmd.add_argument("--id", type=int, required=True)

    return parser

# ==============================
# MAIN ENTRY POINT
# ==============================

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    file_path = Path(args.file)
    expenses = load_expenses(file_path)

    try:
        if args.command == "add":
            add_expense(expenses, args.amount, args.category, args.note)
            save_expenses(file_path, expenses)

        elif args.command == "list":
            list_expenses(expenses)

        elif args.command == "delete":
            delete_expense(expenses, args.id)
            save_expenses(file_path, expenses)

    except Exception as exc:
        logger.exception("Operation failed: %s", exc)
        print(f"Error: {exc}")

if __name__ == "__main__":
    main()
