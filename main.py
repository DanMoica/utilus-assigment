import json
import logging
import sys
from importlib import import_module
from pathlib import Path

from assignment.saas_metrics.report import build_report

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

loader = import_module("assignment.saas_metrics.loader")
load_customers = loader.load_customers
load_subscriptions = loader.load_subscriptions


logger = logging.getLogger(__name__)


def configure_logging() -> None:
    """Configure application logging.

    Returns:
        None.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )


def build_output(customers_path: Path, subscriptions_path: Path) -> dict[str, object]:
    """Build the assignment output from customer and subscription CSV files.

    Args:
        customers_path: Path to the customers CSV file.
        subscriptions_path: Path to the subscriptions CSV file.

    Returns:
        A dictionary containing the calculated SaaS metrics report.
    """
    logger.info("Reading customers from %s", customers_path)
    logger.info("Reading subscriptions from %s", subscriptions_path)

    customers = load_customers(customers_path)
    subscriptions = load_subscriptions(subscriptions_path)

    logger.info("Loaded %s customers", len(customers))
    logger.info("Loaded %s subscriptions", len(subscriptions))

    return build_report(customers, subscriptions)


def main() -> int:
    """Run the command-line program.

    Returns:
        Process exit code. Returns 0 on success, 1 on processing failure, and 2
        when command-line arguments are invalid.
    """
    configure_logging()

    if len(sys.argv) != 4:
        logger.error("Usage: python main.py customers.csv subscriptions.csv output.json")
        return 2

    customers_path = Path(sys.argv[1])
    subscriptions_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3])

    try:
        output = build_output(customers_path, subscriptions_path)
        output_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    except Exception:
        logger.exception("Failed to process input files")
        return 1

    logger.info("Wrote output to %s", output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
