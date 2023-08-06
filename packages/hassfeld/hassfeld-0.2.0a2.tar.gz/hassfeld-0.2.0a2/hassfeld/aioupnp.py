"""Methods implementing UPnP requests."""
from async_upnp_client import UpnpFactory
from async_upnp_client.aiohttp import UpnpEventHandler
from async_upnp_client.aiohttp import AiohttpRequester

from .constants import SERVICE_ID_SETUP_SERVICE
import traceback

async def async_get_device(location, service_type):
    requester = AiohttpRequester()
    factory = UpnpFactory(requester)
    device = await factory.async_create_device(location)
    service = device.service(SERVICE_ID_SETUP_SERVICE)
    action = service.action('GetDevice')
    response = await action.async_call(Service=service_type)
    return response["UniqueDeviceName"]
