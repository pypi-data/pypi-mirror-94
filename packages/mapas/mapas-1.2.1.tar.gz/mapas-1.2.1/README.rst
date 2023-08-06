Mapas
=====

Create static maps from some layers, pretty much like you do with `openlayers`
but static and in python.

Installation
------------

.. code:: bash

    $ pip install mapas

Usage
-----

.. code:: python

    from mapas import Map, Tile, Image, source

    mapa = Map(
        width=600,
        height=400,
        layers=[
            Tile(source=source.Mapbox(
                username='your-username',
                style_id='some-style',
                token='your-token',
            )),
            Image(source=source.ImageWms(
                server_url="https://some.geoserver.com/wms",
                layers=['your:layer'],
                cql_filter="prop='value'",
            )),
        ],
    )

    mapa.set_center(-96.10257, 19.13352)
    mapa.set_zoom(18)

    renderer = mapa.render_to_image()

    renderer.save('mapa.png')

Run it and you'll have a beautiful map at ``mapa.png``.
