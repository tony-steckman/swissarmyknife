# pylint: disable=missing-module-docstring
import json


from OTXv2 import OTXv2  # type: ignore
from OTXv2 import IndicatorTypes


from src.lib.tool import Tool


class OTXLookupTool(Tool):
    """
    A tool for looking up information from the Open Threat Exchange (OTX).
    """

    def __init__(self):
        super().__init__(
            name="OTXLookup",
            description=(
                (
                    "A tool to look up information from the Open Threat "
                    "Exchange (OTX)."
                )
            ),
            version="1.0.0",
            author="Tony Steckman"
        )
        self.add_required_input("indicator")
        self.add_required_input("indicator_type")
        self.add_output("otx_data")
        self.credentials_required = False
        self.api_key_required = True

    def run(self):
        """Execute the tool's main functionality."""
        indicator = self.input_values.get("indicator")
        if not indicator:
            raise ValueError("Indicator input is required.")
        indicator_type = {
            "ip": IndicatorTypes.IPv4,
            "domain": IndicatorTypes.DOMAIN,
            "hostname": IndicatorTypes.HOSTNAME,
            "url": IndicatorTypes.URL,
            "file": IndicatorTypes.FILE_HASH_MD5
        }
        otx = OTXv2(self.get_api_key())
        otx_data = otx.get_indicator_details_full(
            indicator=indicator,
            indicator_type=indicator_type.get(
                self.input_values.get("indicator_type", "ip"))
        )
        self.output_values['otx_data'] = json.dumps(otx_data, indent=3)
        return self.output_values['otx_data']

    def set_api_key(self, api_key):
        """Set the API key for OTX."""
        self.add_credentials("otx_api_key", api_key)

    def get_api_key(self):
        """Get the API key for OTX."""
        return self.credentials.get("otx_api_key", None)
