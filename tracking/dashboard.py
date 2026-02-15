"""Campaign dashboard and reporting."""


class Dashboard:
    """Generate campaign reports and metrics."""

    def __init__(self, crm):
        self.crm = crm

    def get_campaign_summary(self, campaign_id: str) -> dict:
        """Get summary stats for a campaign."""
        raise NotImplementedError

    def get_pipeline_metrics(self) -> dict:
        """Get overall pipeline metrics across all campaigns."""
        raise NotImplementedError
