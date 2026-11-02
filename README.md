# Strata Forge

A procedural terrain generation pipeline that covers the entire run.

It composites fractal noise into heightmaps, converts them into 3D meshes, and drops you into a walkable first-person [Ursina](https://www.ursinaengine.org/) environment.

<img src="noises/fbm.png" width="128"> <img src="noises/perlin.png" width="128"> <img src="noises/billow.png" width="128"> <img src="noises/ridged.png" width="128">

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

The `noise` package may need to build a wheel on some platforms.
The steps below are for Windows:

1. Install [Visual Studio Build Tools for C++](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
2. During setup, select **Desktop development with C++**.
3. Try the installation again:

```bash
pip install noise
```

## How the Terrain Gets Forged

Terrain here is just a grid of heights. The pipeline fills the grid with noise, rescales it into a fixed range, and stitches the grid into a mesh, a bit like draping a sheet over a field of pegs.

1. **Sample:** Every cell of the grid is sampled at `(x / scale, y / scale)` using the `noise` package. Therefore, a larger `scale` stretches features out into broader, smoother hills, and a smaller one packs them tighter. The `seed` picks the pattern.
   
2. **Presets:**
   - **Perlin** and **Simplex** are used as they come.
   - **FBm** stacks `octaves` layers of Perlin noise. Each layer is `lacunarity` times finer and `persistance` times as strong as the one before, so small detail sits on top of broad shapes.
   - **Billow** and **Ridged** are built from FBm output. Billow takes the absolute value, which gives rounded, puffy hills. Ridged takes 1 minus the absolute value, which flips that into sharp ridge lines.

3. **Normalize:** Heights are rescaled to the 0 to 1 range, so every preset ends up in the same range.
   
4. **Mesh:** Each grid cell becomes a vertex at `(x, height * height_scale, y)`, so `height_scale` is the tallest the terrain can get, in world units. Neighboring vertices are 1 unit apart, and every grid square is split into two triangles.

## Configuration

Settings live in `config.yaml`. The defaults are a 512x512 FBm terrain with a fixed seed (42):

```yaml
terrain:
  width: 512
  height: 512

noise:
  type: "fbm" # fbm | perlin | simplex | billow | ridged
  seed: 42    # iykyk ;)
  scale: 50.0
  height_scale: 40.0

  # not used for perlin and simplex
  octaves: 4
  persistence: 0.5
  lacunarity: 2.0

output:
  mesh_dir: "meshes/"
  mesh_name: "terrain.obj"

cmap: # colors based on height
  - { start: 0.00, color: [0.04, 0.14, 0.36], name: ocean }
  - { start: 0.11, color: [0.16, 0.48, 0.68], name: shallows }
  - { start: 0.15, color: [0.90, 0.83, 0.62], name: beach }
  - { start: 0.19, color: [0.80, 0.78, 0.52], name: plains }
  - { start: 0.34, color: [0.45, 0.65, 0.30], name: meadow }
  - { start: 0.52, color: [0.20, 0.45, 0.22], name: forest }
  - { start: 0.64, color: [0.30, 0.30, 0.32], name: rock }
  - { start: 0.71, color: [0.98, 0.99, 1.00], name: snow }
```

- Set the `seed` to `0` to pick a random seed between 1 and 100 000 on each run.
- `octaves`, `persistance` and `lacunarity` only affect FBm, Billow and Ridged.

## Usage

### 1. Preview in the notebook

Open `analysis.ipynb` to plot the configured heightmap as a 3D surface.

You don't need to generate a mesh in order to do this.

<img src="noises/simplex.png" width="256">

### 2. Generate and export a mesh

```bash
python generate.py
```

This writes an OBJ file to `meshes/`, ready to import into Blender or MeshLab.

### 3. Visualize in first-person

```bash
python render.py
```

This loads the generated mesh in a minimal Ursina environment so you can walk around it.

## License

[MIT license](LICENSE)
