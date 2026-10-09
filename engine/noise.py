import numpy as np
from noise import pnoise2, snoise2


def _base(seed: int) -> int:
    if seed == 0:
        seed = np.random.randint(1, 1e5) # higher gives C-level array overflow
    return seed

def _grid(width: int, height: int, sample) -> np.ndarray:
    hm = np.zeros((height, width), dtype=np.float32)
    for y in range(height):
        for x in range(width):
            hm[y, x] = sample(x, y)
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
    return _grid(width, height, lambda x, y: pnoise2(
        x / scale,
        y / scale,
        octaves=octaves,
        persistence=persistence,
        lacunarity=lacunarity,
        base=base
    )), base

# Types that only need (width, height, scale, seed)
PS = {"perlin": _perlin, "simplex": _simplex}

# Types built by post-processing raw fbm output
FBM = {
    "fbm": lambda hm: hm,
    "billow": np.abs,
    "ridged": lambda hm: 1 - np.abs(hm)
}

def select(config: dict) -> np.ndarray:
    noise = config["noise"]["type"]
    width = config["terrain"]["width"]
    height = config["terrain"]["height"]
    scale = config["noise"]["scale"]
    seed = config["noise"]["seed"]

    if noise in PS:
        return PS[noise](width, height, scale, seed)

    if noise in FBM:
        hm = _fbm(
            width,
            height,
            scale,
            config["noise"]["octaves"],
            config["noise"]["persistence"],
            config["noise"]["lacunarity"],
            seed
        )
        return FBM[noise](hm)
    raise ValueError(f"Unknown noise: {noise}")