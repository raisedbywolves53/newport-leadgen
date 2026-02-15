"""Google Sheets CRM for lead tracking."""


class SheetsCRM:
    """Lightweight CRM using Google Sheets via gspread."""

    def __init__(self, creds_path: str, sheet_id: str):
        self.creds_path = creds_path
        self.sheet_id = sheet_id

    def add_lead(self, lead: dict) -> dict:
        """Add a new lead to the CRM sheet."""
        raise NotImplementedError

    def update_lead_status(self, lead_id: str, status: str) -> dict:
        """Update a lead's status."""
        raise NotImplementedError

    def get_leads_by_status(self, status: str) -> list:
        """Get all leads with a given status."""
        raise NotImplementedError

    def log_outreach(self, lead_id: str, channel: str, details: dict) -> dict:
        """Log an outreach attempt for a lead."""
        raise NotImplementedError
