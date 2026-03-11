"""Registry di tutti i tool MCP Wolico."""

from tools.outages import TOOLS as outages_tools
from tools.staffing import TOOLS as staffing_tools
from tools.economics import TOOLS as economics_tools
from tools.employees import TOOLS as employees_tools
from tools.presence import TOOLS as presence_tools
from tools.reporting import TOOLS as reporting_tools
from tools.crm import TOOLS as crm_tools
from tools.ticketing import TOOLS as ticketing_tools
from tools.monitoring import TOOLS as monitoring_tools

ALL_TOOLS: dict = {
    **outages_tools,
    **staffing_tools,
    **economics_tools,
    **employees_tools,
    **presence_tools,
    **reporting_tools,
    **crm_tools,
    **ticketing_tools,
    **monitoring_tools,
}
