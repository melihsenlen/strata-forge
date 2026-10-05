from engine.noise import select
from engine.mesh import normalize, heightmap_mesh, export_obj
from engine.config import load_config, get_mesh


config = load_config()
noise = config["noise"]
mesh = get_mesh(config)

hm, seed = select(noise["type"], config)
hm = normalize(hm)

vertices, faces = heightmap_mesh(hm, noise["height_scale"])


if __name__ == "__main__":
    print(f"Generating terrain... | noise: {noise['type'].upper()} | seed: {seed}")
    mesh.parent.mkdir(parents=True, exist_ok=True)
    export_obj(vertices, faces, mesh)
    print(f"Exported to: {mesh}")