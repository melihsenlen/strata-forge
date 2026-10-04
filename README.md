# Strata Forge

A minimal procedural terrain generation pipeline that covers the entire run.

It composites fractal noise into heightmaps, converts them into 3D meshes, and drops you into a walkable first-person [Ursina](https://www.ursinaengine.org/) environment.

<img src="noises/fbm.png" alt="FBm noise sample" width="128"> <img src="noises/perlin.png" alt="Perlin noise sample" width="128"> <img src="noises/billow.png" alt="Billow noise sample" width="128"> <img src="noises/ridged.png" alt="Ridged noise sample" width="128">

## Features

- Noise presets: Perlin, Simplex, FBm, Billow, Ridged
- Heightmap to mesh conversion with OBJ export
- First-person mesh preview using Ursina Engine
- Jupyter notebook for terrain visualization

## Requirements

- Python 3.10+
- NumPy
- Matplotlib
- noise
- PyYAML
- Ursina
- Jupyter

## Installation

```bash
pip install -r requirements.txt
```

> [!NOTE]
>
> The `noise` package may need to build a wheel on some platforms.
The steps below are for Windows:
>
> 1. Install [Visual Studio Build Tools for C++](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
> 2. During setup, select **Desktop development with C++**.
> 3. Try the installation again:
>
> ```bash
> pip install noise
> ```

## How the Terrain Gets Forged

Terrain here is just a grid of heights. The pipeline fills the grid with noise, rescales it into a fixed range, and stitches the grid into a mesh, a bit like draping a sheet over a field of pegs.

1. **Sample noise.** Every cell of the `width` x `height` grid is sampled at `(x / scale, y / scale)` using the `noise` package. A larger `scale` stretches features out into broader, smoother hills, and a smaller one packs them tighter. The `seed` picks the pattern.
   
2. **Apply a preset.**
   - **Perlin** and **Simplex** are used as they come.
   - **FBm** stacks `octaves` layers of Perlin noise. Each layer is `lacunarity` times finer and `persistance` times as strong as the one before, so small detail sits on top of broad shapes.
   - **Billow** and **Ridged** are built from FBm output. Billow takes the absolute value, which gives rounded, puffy hills. Ridged takes 1 minus the absolute value, which flips that into sharp ridge lines.

3. **Normalize.** Heights are rescaled to the 0 to 1 range, so every preset ends up in the same range regardless of noise type.
   
4. **Build the mesh.** Each grid cell becomes a vertex at `(x, height * height_scale, y)`, so `height_scale` is the tallest the terrain can get, in world units. Neighboring vertices are 1 unit apart, and every grid square is split into two triangles.
   
5. **Color and export.** Each vertex is colored by its height: blue for low ground, then greens, gray rock, and white at the peaks, with a little random variation per vertex. The colors are stored as per-vertex colors in the OBJ file.

## Configuration

Settings live in `config.yaml`. The defaults are a 128x128 FBm terrain with a fixed seed:

```yaml
terrain:
  width: 128
  height: 128

noise:
  type: "fbm" # fbm | perlin | simplex | billow | ridged
  seed: 42    # set to 0 for random
  scale: 25.0
  height_scale: 15.0

  # not used for perlin and simplex
  octaves: 4  
  persistance: 0.5
  lacunarity: 2.0

output:
  mesh_dir: "meshes/"
  mesh_name: "terrain.obj"
```

> [!TIP]
> - Change `noise.type` to switch presets.
> - A `seed` of `0` picks a random seed between 0 and 99 on each run.
> - `octaves`, `persistance` and `lacunarity` only affect FBm, Billow and Ridged.

## Usage

### Generate and export a mesh

```bash
python generate.py
```

This writes an OBJ file to `meshes/`, ready to import into Blender or MeshLab.

### Preview in first-person

> [!IMPORTANT]
> Run `generate.py` first, since the preview needs the OBJ file to exist.

```bash
python render.py
```

This loads the generated mesh in a minimal Ursina environment so you can walk around it.

### Visualize in the notebook

Open `analysis.ipynb` to plot the configured heightmap as a 3D surface, using the same `config.yaml` settings.

## License

[MIT license](LICENSE)
