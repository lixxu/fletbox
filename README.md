# fletbox

fletbox is a collection of helpers for [flet](https://flet.dev/) applications development.

## Installation

```bash
pip install -U fletbox
```

## Example

```python
import fletbox.helpers as fbh

# get assets folder
assets_dir = fbh.get_assets_dir()

# save window position and size before quit
fbh.save_window_ui(page, key="win_pos")

# settings is dict-like
settings = fbh.load_window_ui(page, "win_pos")
fbh.restore_window(page, settings)
```
