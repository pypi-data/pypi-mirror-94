from typing import Tuple

import requests


class Source:
    pass


class NetworkSource(Source):
    def get_uri_for_resource(self, *args, **kwargs) -> str:
        raise NotImplementedError

    def make_request_for_resource(self, *args, **kwargs):
        retries = 5

        while retries > 0:
            url = self.get_uri_for_resource(*args, **kwargs)
            r = requests.get(url, params=self.get_request_params(*args, **kwargs))

            if r.status_code != 200:
                retries -= 1
                continue
            else:
                break

        if retries == 0:
            r.raise_for_status()

        return r


class XYZSource(NetworkSource):
    def get_tile_size(self):
        return 256

    def get_tile_png(self, z: int, x: int, y: int) -> bytes:
        r = self.make_request_for_resource(z, x, y)
        return r.content


class ImageSource(NetworkSource):
    def get_image_png(
            self, bbox: Tuple[float, float, float, float],
            dimensions: Tuple[int, int]) -> bytes:
        r = self.make_request_for_resource(bbox, dimensions)
        return r.content
