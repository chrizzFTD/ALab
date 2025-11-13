from pathlib import Path
from functools import partial

ROOT_DIR = Path(__file__).parent / "ALab"

from pxr import UsdUtils, Sdf

URL_ROOT = "https://raw.githubusercontent.com/chrizzFTD/ALab/refs/heads/url_references/ALab/"

def modifyFn(anchor, path):
    # this could be smarter but for now, lazy hardcode
    if path.startswith("../"):
        full_path = Path(anchor).parent / path
        resolved = full_path.resolve()
        url_path = URL_ROOT + str(resolved.relative_to(ROOT_DIR).as_posix())
        return url_path
    elif not Path(path).is_absolute():
        full_path = Path(anchor).parent / path
        if full_path.suffix and not full_path.is_file():
            print(f"Not a file: {full_path}")
        url_path = URL_ROOT + str(full_path.relative_to(ROOT_DIR).as_posix())
        return url_path
    else:
        return path


for (root, __, filenames) in ROOT_DIR.walk():
    for filename in filenames:
        filepath = root / filename
        if filepath.suffix not in (".usda", "usd"):
            continue

        dependencies = UsdUtils.ExtractExternalReferences(str(filepath))
        layer = Sdf.Layer.FindOrOpen(str(filepath))
        UsdUtils.ModifyAssetPaths(layer, partial(modifyFn, layer.identifier))
        layer.Save()
