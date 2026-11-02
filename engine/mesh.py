import numpy as np


def normalize(hm: np.ndarray) -> np.ndarray:
    hm_min, hm_max = hm.min(), hm.max()

    if hm_max - hm_min == 0: return np.full_like(hm, 0)
    norm = (hm - hm_min) / (hm_max - hm_min)
    return norm

def heightmap_mesh(hm: np.ndarray, height_scale: float) -> tuple[np.ndarray, np.ndarray]:
    h, w = hm.shape

    xs, zs = np.meshgrid(np.arange(w), np.arange(h))
    vertices = np.stack([xs, hm * height_scale, zs], axis=-1)
    vertices = vertices.reshape(-1, 3).astype(np.float32)

    # Vertex index grid and picking the corners
    idx = np.arange(h * w, dtype=np.int32).reshape(h, w)
    tl = idx[:-1, :-1].ravel()
    tr = idx[:-1, 1:].ravel()
    bl = idx[1:, :-1].ravel()
    br = idx[1:, 1:].ravel()

    # Two triangles per quad
    faces = np.empty((tl.size * 2, 3), dtype=np.int32)
    faces[0::2] = np.stack([tl, tr, bl], axis=1)
    faces[1::2] = np.stack([tr, br, bl], axis=1)
    return vertices, faces

def export_obj(vertices: np.ndarray, faces: np.ndarray, cmap, path: str) -> None:
    starts, colors = np.asarray(cmap[0]), np.asarray(cmap[1])

    t = normalize(vertices[:, 1])

    # Band lookup for every vertex at once
    idx = (np.searchsorted(starts, t, side="right") - 1).clip(0)
    rgb = colors[idx]

    vertex_rows = np.hstack([vertices, rgb])

    with open(path, "w") as obj:
        np.savetxt(obj, vertex_rows, fmt="v %.2f %.2f %.2f %.2f %.2f %.2f")
        np.savetxt(obj, faces + 1, fmt="f %d %d %d")
