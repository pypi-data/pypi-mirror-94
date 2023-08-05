## Project description

ic_slide is a sdk wrapper for coriander project of intemedic.it providers slide apis for python projects of internal company. It can not used for public domains.

## Installing

Install and update using `pip`:

```bash
pip install -U ic_slide
```

## A Simple Example

sample of open-slide.

```python
from ic_slide import open_slide
# open a slide with slide id.
slide_id = '4395d816-2832-e7b7-6472-39f9b9f93480'
open_slide(slide_id)

# get metadata of slide.
metadata = slide.metadata

# get tile image (PIL.Image) of slide with x=0, y=0, width=512, height=512
tile = slide.read_region(0,0,512,512)
```

sample of enumerate tiles to a slide.

```python
from ic_slide import enumerate_tiles
import numpy as np
# enumerate tiles from begin to stop with specified stride and size.
slide_id = '4395d816-2832-e7b7-6472-39f9b9f93480'
iterated_tiles = enumerate_tiles(slide_id, [0,0], [8192,8192], 400, [512,512])

for tile in iterated_tiles:
    do_something(tile)
```

sample of enumerate slide entries of private cloud.

```python
from ic_slide import get_slide_entries

#get all slide entries
slide_entries = get_slide_entries()
for entry in slide_entries:
    print(entry.Name)

```

sample of get distinct slide id of private cloud.

```python
from ic_slide import get_distinct_slide_ids
slide_ids = get_distinct_slide_ids()

for slide_id in slide_ids():
    do_something(slide_id)
```

sample of get annotations of slide entry.

```python
from ic_slide import get_slide_entries, get_slide_entry_annotations


#get all slide entries
slide_entries = get_slide_entries()
for entry in slide_entries:
    entry_id = entry.Id
    annotations = get_slide_entry_annotations(entry_id)
```
