from engine.noise import select
from engine.mesh import normalize, heightmap_mesh, export_obj
from engine.config import load_config, get_mesh, get_cmap


config  = load_config()
mesh    = get_mesh(config)
cmap    = get_cmap(config)

noise   = config["noise"]
terrain = config["terrain"]


if __name__ == "__main__":
    hm, seed = select(noise, terrain)
    print(f"Noise: {noise['type'].upper()} | Seed: {seed}")

    # Generation
    hm = normalize(hm)
    vertices, faces = heightmap_mesh(hm, noise["height_scale"])

    # Exporting
    mesh.parent.mkdir(parents=True, exist_ok=True)
    export_obj(vertices, faces, cmap, mesh)
    print(f"Exported: {mesh}")