import numpy as np
from noise import pnoise2, snoise2


def _base(seed: int) -> int:
    if seed == 0:
        seed = np.random.randint(1, int(1e5)) # Higher gives C-level array overflow
    return seed

def _grid(width: int, height: int, sample) -> np.ndarray:
    hm = np.zeros((height, width), dtype=np.float32)
    for h in range(height):
        for w in range(width):
            hm[h, w] = sample(w, h)
    return hm

def _perlin(width: int, height: int, scale: float, seed: int) -> tuple[np.ndarray, int]:
    base = _base(seed)
    return _grid(width, height, lambda x, y: pnoise2(x / scale, y / scale, base=base)), base

def _simplex(width: int, height: int, scale: float, seed: int) -> tuple[np.ndarray, int]:
    base = _base(seed)
    return _grid(width, height, lambda x, y: snoise2(x / scale, y / scale, base=base)), base

def _fbm(
    width: int,
    height: int,
    scale: float,
    octaves: int,
    persistence: float,
    lacunarity: float,
    seed: int
) -> tuple[np.ndarray, int]:
    base = _base(seed)
    return _grid(width, height, lambda h, w: pnoise2(
        h / scale,
        w / scale,
        octaves=octaves,
        persistence=persistence,
        lacunarity=lacunarity,
        base=base
    )), base

PS = {"perlin": _perlin, "simplex": _simplex}

# Types built by post-processing raw fbm output
FBM = {
    "fbm": lambda hm: hm,
    "billow": np.abs,
    "ridged": lambda hm: 1 - np.abs(hm)
}

def select(noise: dict, terrain: dict) -> np.ndarray:
    method = noise["type"]
    scale  = noise["scale"]
    seed   = noise["seed"]
    width  = terrain["width"]
    height = terrain["height"]

    if method in PS:
        return PS[method](width, height, scale, seed)

    if method in FBM:
        hm, base = _fbm(
            width,
            height,
            scale,
            noise["octaves"],
            noise["persistence"],
            noise["lacunarity"],
            seed
        )
        return FBM[method](hm), base
    raise ValueError(f"Unknown noise: {method}")