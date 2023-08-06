# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gully']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gully',
    'version': '0.1.0',
    'description': 'Simple real time data stream manipulation.',
    'long_description': '# Gully\n\nGully is a simple framework for manipulating streams of data. It provides methods for asynchronous & synchronous access to the streams.\n\n## Installation\n```shell\npip install gully\n```\n\n## Usage\n```python\nimport gully\n\nasync def monitor_stream_using_iterator(stream: gully.DataStream):\n    async for item in stream:\n        print(item)\n\nasync def monitor_stream_using_future(stream: gully.DataStream):\n    while not stream.next.done():\n        item = await stream.next\n        print(item)\n        \n\ndata_stream = gully.DataStream()\nfiltered = data_stream.filter(lambda stream, item: item == "foobar")\nmapped = filtered.map(lambda stream, item: item.upper())\n```\n## Documentation\n\n### gully.DataStream(max_size: int = -1, loop: asyncio.Loop = None)\n\nProvides the interface into the data stream. It offers both iterable and async iterable functionality, it also has item getters for accessing history. \n\nThe data stream will cache past values up to `max_size` items, or unlimited if `max_size` is less than 1. These values can be accessed using get item (e.g. `stream[1]`), `len(stream)` will return the total number and items cached, and `value in stream` will tell you if a value is in the data stream.\n\nIterating through the data stream will go through the value cache from oldest to newest. Using an async iterator will go through the cache from oldest to newest and then will await new values.\n\n- `property DataStream.max_size: int` The maximum size set for the data stream cache.\n\n- `property DataStream.next: asyncio.Future` The future that will receive the next value that is pushed into the data stream. This future will change with every pushed value, it will be cancelled if the stream is closed. \n\n**`method DataStream.push(value: Any)`**\n\nPushes a value into the data stream.\n\n**`method DataStream.close()`**\n\nCloses the stream and cancels the next future stopping all watchers whether created synchronously, asynchronously, or through an iterator.\n\n**`method DataStream.on_next(callback: Callable[[DataStreamBase, Any], None])`**\n\nRegisters a function to be called when the next future is set. The callback will be passed the data stream it was registered on and the value that was pushed.\n\n**`method DataStream.iterate_first(limit: int) -> DataStreamIterator`**\n\nGets an iterator that will only yield at most `limit` items. This iterator can be used either synchronously or asynchronously, only an async iterator will wait for new values to be pushed. This will always start at the oldest item in the cache.\n\n**`method DataStream.filter(predicate: Callable[[DataStreamBase, Any], bool], max_size: int = -1) -> DataStreamFilteredView`**\n\nCreates a data stream view that only receives values that the predicate function allows. The predicate function should return `True` for any value that should be allowed into the stream.\n\n**`method DataStream.map(mapper: Callable[[DataStreamBase, Any], Any], max_size: int = -1) -> DataStreamMappedView`**\n\nCreates a data stream view that passes every value pushed to the stream into the mapping function, the returned value will be pushed into the data stream view.\n\n### gully.DataStreamFilteredView\n\nFunctions like a normal DataStream but it monitors other streams and only pushes values to itself that pass the predicate function\'s conditions. The cache history begins when it is created and will not have access to older values from the stream it is monitoring.\n\n### gully.DataStreamMappedView\n\nFunctions like a normal DataStream but it monitors other streams and passes the new values through a mapping function before pushing them to itself. The cache history begins when it is created and will not have access to older values from the stream it is monitoring.\n',
    'author': 'Zech Zimmerman',
    'author_email': 'hi@zech.codes',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ZechCodes/gully',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
