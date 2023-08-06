# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beetsplug', 'beetsplug.bandcamp']

package_data = \
{'': ['*']}

install_requires = \
['beets>=1.4.6',
 'cached-property>=1.5.2,<2.0.0',
 'pycountry>=20.7.3,<21.0.0',
 'requests']

setup_kwargs = {
    'name': 'beetcamp',
    'version': '0.5.7',
    'description': 'Bandcamp autotagger source for beets (http://beets.io).',
    'long_description': "[![image](http://img.shields.io/pypi/v/beetcamp.svg)](https://pypi.python.org/pypi/beetcamp)\n\nPlug-in for [beets](https://github.com/beetbox/beets) to use Bandcamp as\nan autotagger source.\n\nThis is an up-to-date fork of [unrblt/beets-bandcamp](https://github.com/unrblt/beets-bandcamp)\n\n# Installation\n\nNavigate to your `beets` virtual environment, install the plug-in with\n\n```bash\n   pip install --user beetcamp\n```\n\nand add `bandcamp` to the `plugins` list to your beets configuration file.\n\n\n# Configuration\n\n#### `preferred_media`\n\n- Default: `Digital`\n- available: `Vinyl`, `CD`, `Cassette`, `Digital`.\n\nA comma-separated list of media to prioritise when\nfetching albums. For example: `preferred_media: Vinyl,Cassette`\nwill ignore `CD`, check for a `Vinyl`, and then for a `Cassette`, in the end\ndefaulting to `Digital` (always available) if none of the two are found.\n\n#### `include_digital_only_tracks`\n\n- Default: `True`\n\nFor media that isn't `Digital Media`, include all tracks, even if their titles\ncontain **digital only** (or alike).\n\nIf you have `False` here, then, for example, a `Vinyl` media of an album will\nonly include the tracks that are supposed to be found in that media.\n\n#### `search_max`\n\n- Default: `10`.\n\nMaximum number of items to fetch through search queries. Depending on the\nspecificity of queries and whether a suitable match is found, it could\nfetch 50+ results which may take a minute, so it'd make sense to bound\nthis to some sort of sensible number. Usually, a match is found among the first 5 items.\n\n#### `lyrics`\n\n- Default: `false`.\n\nAdd lyrics to the tracks if they are available.\n\n#### `art`\n\n- Default: `false`.\n\nAdd a source to the [FetchArt](http://beets.readthedocs.org/en/latest/plugins/fetchart.html)\nplug-in to download album art for Bandcamp albums (requires `FetchArt` plug-in enabled).\n\n# Usage\n\nThis plug-in uses the Bandcamp URL as id (for both albums and songs). If no matching\nrelease is found when importing you can select `enter Id` and paste the Bandcamp URL.\n\n## Currently supported / returned data\n\n| field            | singleton track | album track | album |\n|-----------------:|:---------------:|:-----------:|:-----:|\n| `album`          |                 |             | ✔     |\n| `album_id`       |                 |             | ✔     |\n| `albumartist`    | ✔               | ✔           | ✔     |\n| `albumstatus`    |                 |             | ✔     |\n| `albumtype`      |                 |             | ✔     |\n| `artist`         | ✔               | ✔           | ✔     |\n| `artist_id`      | ✔               | ✔           |       |\n| `catalognum`     |                 |             | ✔     |\n| `country`        |                 |             | ✔     |\n| `day`            |                 |             | ✔     |\n| `disctitle`      |                 | ✔           |       |\n| `image`          |                 | ✔           | ✔     |\n| `index`          |                 | ✔           |       |\n| `label`          |                 | ✔           | ✔     |\n| `length`         | ✔               | ✔           |       |\n| `lyrics`         |                 | ✔           |       |\n| `media`          |                 | ✔           | ✔     |\n| `medium`         |                 | ✔           |       |\n| `mediums`        |                 |             | ✔     |\n| * `medium_index` |                 | ✔           |       |\n| * `medium_total` |                 | ✔           |       |\n| `month`          |                 |             | ✔     |\n| `title`          | ✔               | ✔           |       |\n| `track_alt`      | ✔               | ✔           |       |\n| `va`             |                 |             | ✔     |\n| `year`           |                 |             | ✔     |\n\n* \\* are likely to be inaccurate, since Bandcamp does not provide this data,\n  therefore they depend on artists providing some clues in the descriptions of\n  their releases. This is only relevant if you have `per_disc_numbering` set to\n  `True` in the global beets configuration.\n",
    'author': 'Šarūnas Nejus',
    'author_email': 'snejus@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/snejus/beets-bandcamp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
