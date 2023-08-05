import logging
AuthUri = 'http://private.intemedic.com:6001'
SlideCloudUrl = 'http://private.intemedic.com:6002'
StorageIndexUrl = 'http://private.intemedic.com:6003'
AssetServiceUrl = 'http://private.intemedic.com:6004'
Micron_Per_Pixel_X = 0.35093510
Micron_Per_Pixel_Y = 0.35150376

logger = logging.Logger(__name__)


def _configure(auth_url=None,
               slide_cloud_url=None,
               storage_index_url=None,
               asset_service_url=None,
               micron_per_pixel_x=None,
               micron_per_pixel_y=None):
    if not auth_url:
        global AuthUri
        AuthUri = auth_url
        logger.info(f"Change auth uri to {auth_url}")
    if not slide_cloud_url:
        global SlideCloudUrl
        SlideCloudUrl = slide_cloud_url
        logger.info(f"Change slide cloud url to {slide_cloud_url}.")
    if not storage_index_url:
        global StorageIndexUrl
        StorageIndexUrl = storage_index_url
        logger.info(f"Change storage index url to {storage_index_url}.")
    if not asset_service_url:
        global AssetServiceUrl
        AssetServiceUrl = asset_service_url
        logger.info(f"Change asset service url to {asset_service_url}.")
    if not micron_per_pixel_x:
        global Micron_Per_Pixel_X
        Micron_Per_Pixel_X = float(micron_per_pixel_x)
        logger.info(f"Change micron per pixel to {micron_per_pixel_x}.")
    if not micron_per_pixel_y:
        global Micron_Per_Pixel_Y
        Micron_Per_Pixel_Y = float(micron_per_pixel_y)
        logger.info(f"Change micron per pixel to {micron_per_pixel_y}.")


def configure(**kwargs) -> None:
    '''
    Change the ic_slide configuration here.

    Args:
        **kwargs: The keyword arguments

        'auth_url': The url of auth micro service.

        slide_cloud_url: The url of slide cloud micro service.

        storage_index_url: The url of storage index micro service.

        asset_service_url: The url of asset service micro service.

        micron_per_pixel_x: The mpp-x to unify slides in same standard.

        micron_per_pixel_y: The mpp-y to unify slides in same standard.
    '''
    _configure(**kwargs)
