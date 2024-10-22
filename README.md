# fletbox

fletbox is a collection of helpers for [flet](https://flet.dev/) applications development.

## Installation

```bash
pip install -U fletbox
```

## Example (check examples folder for details)

```python
import fletbox.helpers as fbh

assets_dir = fbh.get_assets_dir()

# save window before quit
settings = fbh.save_window(page)
# save settings to somewhere
# save_settings(settings)

# settings is dict-like
fbh.restore_window(page, settings)
```
