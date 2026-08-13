"""System settings service — key-value store with env fallback."""

from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.system_setting import SystemSetting

settings = get_settings()

# Keys editable in admin (secrets stay in .env)
EDITABLE_KEYS = (
    "site_name",
    "ga_measurement_id",
    "contact_email",
    "footer_text",
    "bing_site_verification",
)


def get_setting(db: Session, key: str, default: str = "") -> str:
    row = db.query(SystemSetting).filter(SystemSetting.key == key).first()
    if row and row.value:
        return row.value
    return default


def set_setting(db: Session, key: str, value: str) -> None:
    row = db.query(SystemSetting).filter(SystemSetting.key == key).first()
    if row:
        row.value = value
    else:
        db.add(SystemSetting(key=key, value=value))
    db.commit()


def get_all_settings(db: Session) -> dict[str, str]:
    rows = db.query(SystemSetting).all()
    return {r.key: r.value or "" for r in rows}


def get_ga_measurement_id(db: Session | None = None) -> str:
    """Env takes priority; DB setting as fallback."""
    if settings.ga_measurement_id:
        return settings.ga_measurement_id
    if db:
        return get_setting(db, "ga_measurement_id", "")
    return ""


def save_settings_batch(db: Session, data: dict[str, str]) -> None:
    for key in EDITABLE_KEYS:
        if key in data:
            set_setting(db, key, data[key].strip())
