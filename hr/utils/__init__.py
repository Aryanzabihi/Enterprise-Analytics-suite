# Utils package for HR Analytics Dashboard

# Import main classes to make them available at package level
from .insight_manager import AdvancedInsightManager
from .dashboard_renderer import render_world_class_insights_dashboard
from .advanced_insights import (
    generate_executive_summary,
    generate_predictive_insights,
    generate_segmentation_insights,
    generate_correlation_insights,
    generate_kpi_insights
)

__all__ = [
    'AdvancedInsightManager',
    'render_world_class_insights_dashboard',
    'generate_executive_summary',
    'generate_predictive_insights',
    'generate_segmentation_insights',
    'generate_correlation_insights',
    'generate_kpi_insights'
]
