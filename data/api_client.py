import json
import logging
from typing import Optional, Any, Dict, Union
from .api_response import ApiResponse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    logger.warning("The 'requests' library is not installed. ApiClient will not function correctly. Please run 'pip install requests'.")

class ApiClient:
    """
    A generic API client for Sukoyo.
    Handles common HTTP methods and returns consistent ApiResponse objects.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ApiClient, cls).__new__(cls)
            cls._instance._base_url = ""
            cls._instance._headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            cls._instance._timeout = 10
        return cls._instance

    def configure(self, base_url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 10):
        """Configure the API client with base URL and default headers."""
        self._base_url = base_url.rstrip('/')
        if headers:
            self._headers.update(headers)
        self._timeout = timeout

    def set_header(self, key: str, value: str):
        """Set a specific header."""
        self._headers[key] = value

    def _get_full_url(self, endpoint: str) -> str:
        """Helper to construct full URL."""
        if endpoint.startswith(('http://', 'https://')):
            return endpoint
        return f"{self._base_url}/{endpoint.lstrip('/')}"

    def _handle_request(self, method: str, endpoint: str, **kwargs) -> ApiResponse:
        """Generic request handler."""
        if not REQUESTS_AVAILABLE:
            return ApiResponse.error_response("The 'requests' library is not available.")

        url = self._get_full_url(endpoint)
        
        # Merge default headers with any passed in kwargs
        headers = self._headers.copy()
        if 'headers' in kwargs:
            headers.update(kwargs.pop('headers'))
        
        # Set default timeout if not provided
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self._timeout

        try:
            logger.info(f"API Request: {method} {url}")
            response = requests.request(method, url, headers=headers, **kwargs)
            
            try:
                data = response.json()
            except json.JSONDecodeError:
                data = response.text

            if response.ok:
                return ApiResponse.success_response(data, message=f"{method} request successful")
            else:
                error_msg = f"HTTP Error {response.status_code}: {response.reason}"
                logger.error(f"API Error: {error_msg}")
                return ApiResponse(False, error=error_msg, data=data)

        except requests.exceptions.Timeout:
            return ApiResponse.error_response("Request timed out")
        except requests.exceptions.ConnectionError:
            return ApiResponse.error_response("Could not connect to server")
        except Exception as e:
            logger.exception("Unexpected API error")
            return ApiResponse.error_response(str(e))

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> ApiResponse:
        """GET request."""
        return self._handle_request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint: str, data: Optional[Union[Dict, str]] = None, json: Optional[Dict] = None, **kwargs) -> ApiResponse:
        """POST request."""
        return self._handle_request("POST", endpoint, data=data, json=json, **kwargs)

    def put(self, endpoint: str, data: Optional[Union[Dict, str]] = None, json: Optional[Dict] = None, **kwargs) -> ApiResponse:
        """PUT request."""
        return self._handle_request("PUT", endpoint, data=data, json=json, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> ApiResponse:
        """DELETE request."""
        return self._handle_request("DELETE", endpoint, **kwargs)

    def patch(self, endpoint: str, data: Optional[Union[Dict, str]] = None, json: Optional[Dict] = None, **kwargs) -> ApiResponse:
        """PATCH request."""
        return self._handle_request("PATCH", endpoint, data=data, json=json, **kwargs)
