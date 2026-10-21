from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DATABASE_PATH = DATA_DIR / "warehouse.db"
EXPIRY_ALERT_DAYS = 30
