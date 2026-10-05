import numpy as np


def normalize(hm: np.ndarray) -> np.ndarray:
    hm_min, hm_max = hm.min(), hm.max()

    if hm_max - hm_min == 0: return np.full_like(hm, 0)
    norm = (hm - hm_min) / (hm_max - hm_min)
    return norm

def heightmap_mesh(hm: np.ndarray, height_scale: float) -> tuple[np.ndarray, np.ndarray]:
    h, w = hm.shape
    vertices = np.zeros((h * w, 3), dtype=np.float32)

    for y in range(h):
        for x in range(w):
            idx = y * w + x
            vertices[idx] = [x, hm[y, x] * height_scale, y]

    faces = []
    for y in range(h - 1):
        for x in range(w - 1):
            i = y * w + x
            faces.append([i, i + 1, i + w])
            faces.append([i + 1, i + w + 1, i + w])
    faces = np.array(faces, dtype=np.int32)
    return vertices, faces

def heightmap_color(h, h_min, h_max) -> tuple[float, float, float]:
    t = (h - h_min) / (h_max - h_min + 1e-8)

    if   t < 0.11: return (0.04, 0.14, 0.36) # deep ocean
    elif t < 0.19: return (0.16, 0.48, 0.68) # shallows
    elif t < 0.21: return (0.90, 0.83, 0.62) # beach
    elif t < 0.34: return (0.80, 0.78, 0.52) # grass
    elif t < 0.52: return (0.45, 0.65, 0.30) # meadow
    elif t < 0.64: return (0.20, 0.45, 0.22) # forest
    elif t < 0.71: return (0.30, 0.30, 0.32) # rock
    else:          return (0.98, 0.99, 1.00) # snow

def export_obj(vertices: np.ndarray, faces: np.ndarray, path: str) -> None:
    heights = vertices[:, 1]
    h_min, h_max = heights.min(), heights.max()

    with open(path, "w") as obj:
        for v in vertices:
            r, g, b = heightmap_color(v[1], h_min, h_max)
            obj.write(f"v {v[0]} {v[1]} {v[2]} {r} {g} {b}\n")

        for face in faces:
            obj.write(f"f {face[0] + 1} {face[1] + 1} {face[2] + 1}\n")
