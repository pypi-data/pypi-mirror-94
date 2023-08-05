import requests
from numpy import arange
import logging
from PIL import Image
import io
from .auth import get_access_token, urljoin
from .config import SlideCloudUrl, Micron_Per_Pixel_X, Micron_Per_Pixel_Y
import numpy as np

logger = logging.getLogger(__name__)


class SlideCloudStorage:
    metadata_url = urljoin(SlideCloudUrl,
                           "api/app/slideClientOnly/slideMetadata")
    tile_url = urljoin(SlideCloudUrl,
                       "api/app/slideClientOnly/tileUrl")

    def get_metadata(self, slide_id):
        if not slide_id:
            raise ValueError('Invalid empty slide id')
        url = f'{self.metadata_url}/{slide_id}'
        access_token = get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        metadata = requests.get(url,
                                headers=headers).json()
        if 'error' in metadata:
            raise ValueError(metadata['error']['message'])

        result = Metadata(metadata)
        result.SlideId = slide_id
        return result

    def get_tile(self, slide_id, row, column, layer, lod):
        url = f'{self.tile_url}?id={slide_id}&Row={row}&Column={column}&Layer={layer}&LODLevel={lod}'
        access_token = get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url,
                                headers=headers)

        if response.status_code >= 200 and response.status_code <= 299:
            tile_url = response.content
        else:
            raise Exception(
                f"Can not get tile, {response.reason} {response.content}")
        response = requests.get(tile_url)
        if response.status_code >= 200 and response.status_code <= 299:
            return response.content
        return None


class Metadata(object):
    SlideId = ''
    Name = ''
    LayerCount = 0
    MinimumLODLevel = 0
    MaximumLODLevel = 0
    LODGaps = []
    QuickHash = ''
    Vendor = ''
    Version = None
    Comments = ''
    BackgroundColor = None
    HorizontalTileCount = 0
    VertialTileCount = 0
    LayerCount = 0
    TileSize = {}
    ContentRegion = {}
    HorizontalResolution = 0
    VeriticalResolution = 0
    AdditionalData = {}

    def __init__(self, metadata_dict):
        self.__dict__ = metadata_dict

    def get_default_layer(self):
        return 1 if self.LayerCount == 1 else 0

    def get_lod_to_world_scale(self, lod):
        if(lod < 0 or lod > self.MaximumLODLevel):
            raise ValueError(
                f'load {lod} out of range [0-{self.MaximumLODLevel}]')

        scale = 1.0

        if lod != 0:
            for gap in self.LODGaps:
                scale /= gap

        return scale


class Slide:
    def __init__(self, metadata, slide_storage):
        self.metadata = metadata
        self._slide_storage = slide_storage

    def read_region(self, x, y, width, height, layer=None, lod=None):
        final_layer = layer if layer else self.metadata.get_default_layer()
        final_lod = lod if lod else self.metadata.MinimumLODLevel
        tile_width = self.metadata.TileSize['Width']
        tile_height = self.metadata.TileSize['Height']
        tile_index_left = int(x / tile_width)
        tile_index_top = int(y / tile_height)
        tile_index_right = int((x + width - 1) / tile_width)
        tile_index_bottom = int((y + height - 1)/tile_height)

        new_image = Image.new('RGB', (width, height), (255, 255, 255))

        offset_y = y
        # must +1 to include stop
        for row in range(tile_index_top, tile_index_bottom+1):
            tile_top = row * tile_height
            tile_bottom = (row+1) * tile_height
            offset_x = x
            area_y = offset_y - tile_top
            area_height = min(tile_bottom - offset_y, height - offset_y + y)
            # must +1 to include stop
            for column in range(tile_index_left, tile_index_right+1):
                tile_left = column * tile_width
                tile_right = (column+1) * tile_width
                area_x = offset_x - tile_left
                tile_data = self._slide_storage.get_tile(
                    self.metadata.SlideId, int(row), int(column), final_layer, final_lod)
                logger.info(
                    f'get tile {row}-{column}-{final_layer}-{final_lod} data')
                area_width = min(tile_right - offset_x, width - offset_x + x)
                if tile_data:
                    image = Image.open(io.BytesIO(tile_data))
                    image_valid_area = (area_x,
                                        area_y,
                                        area_width + area_x,
                                        area_height + area_y)
                    cropped_image = image.crop(image_valid_area)
                    # cropped_image.save(f"{image_valid_area}.jpg")
                    new_image.paste(cropped_image, (offset_x - x, offset_y-y))
                offset_x += area_width
            offset_y += area_height
        return new_image


def open_slide(slide_id):
    '''
    Open a cloud slide of coriander.

    Args:
        slide_id; the id of slide.

    Returns:
        slide (Slide): the slide.
    '''
    logger.info(f"open slide with slide id {slide_id}")
    slide_storage = SlideCloudStorage()
    metadata = slide_storage.get_metadata(slide_id)
    return Slide(metadata, slide_storage)


def enumerate_tiles(slide_id,
                    begin,
                    stop,
                    stride=(400, 400),
                    size=(512, 512),
                    auto_scaling=True):
    '''
    Get tiles of slide id with begin and end.

    Args:
        begin (list[2]): the begin location to the slide.

        end (list[2]): the end location to the slide.

        stride (tuple(int, int)): the stride to get tiles in Vertical/ Horizontal.

        size (tuple(int,int)): the size of tile image.

        auto-scaling (boolean): should unify slides in same standard by mpp.

    Returns:
        tiles (Generator[Image]): the tile images
    '''
    slide = open_slide(slide_id)
    logger.info(f"Enumerate slide {slide_id}  tiles.")
    return _enumerate_slide_tiles(slide, begin, stop, stride, size, auto_scaling)


def enumerate_content_tiles(slide_id, stride=(400, 400), size=(512, 512), auto_scaling=True):
    '''
    Get tiles in the content area of slide

    Args:
        stride (tuple(int, int)): the stride to get tiles in Vertical/ Horizontal.

        size (tuple(int,int)): the size of tile image.

        auto-scaling (boolean): should unify slides in same standard by mpp.

    Returns:
        tiles (Generator[Image]): the tile images
    '''
    slide = open_slide(slide_id)
    logger.info(f"Enumerate slide {slide_id} content tiles .")
    begin = int(slide.metadata.ContentRegion['X']), int(
        slide.metadata.ContentRegion['Y'])

    stop = begin[0] + int(slide.metadata.ContentRegion["Width"]
                          ), begin[1]+int(slide.metadata.ContentRegion["Height"])

    return _enumerate_slide_tiles(slide, begin, stop, stride, size, auto_scaling)


def _enumerate_slide_tiles(slide, begin, stop, stride, size, auto_scaling=True):
    if not slide:
        raise ValueError("Can not enumerate tiles with empty slide.")

    if not begin or len(begin) != 2:
        raise ValueError(f"Invalid begin value {begin}")

    if not stop or len(stop) != 2:
        raise ValueError(f"Invalid stop value {stop}.")

    if not stride or len(stride) != 2:
        raise ValueError(f"Invalid stride value {stride}.")

    if not size or len(size) != 2:
        raise ValueError(f"Invalide size value {size}.")
    scale = [1, 1]
    if auto_scaling:
        scale = _get_slide_scale(slide)
    begin = np.array(begin)
    stop = np.array(stop)
    stride = (np.array(stride) * scale).astype(int)
    size = (np.array(size) * scale).astype(int)

    step = ((stop - begin - size)/stride+1).astype(int)
    for row in range(step[1]):
        for col in range(step[0]):
            x0, y0 = (begin + np.array((col, row)) * stride).astype(int)
            image = slide.read_region(x0, y0, size[0], size[1], None, None)

            yield {
                'location': [x0, y0],
                'image': image,
                'size': list(size),
                'step': [col, row]
            }


def _get_slide_scale(slide):
    mpp_x = Micron_Per_Pixel_X
    mpp_y = Micron_Per_Pixel_Y
    slide_metadata = slide.metadata
    if slide_metadata.HorizontalResolution and \
            slide_metadata.HorizontalResolution > 0 and \
            slide_metadata.VerticalResolution and \
            slide_metadata.VerticalResolution > 0:
        return mpp_x/slide_metadata.HorizontalResolution, \
            mpp_y/slide_metadata.VerticalResolution
    return [1, 1]
