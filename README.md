# Strata Forge

A minimal procedural terrain generation pipeline. It composites fractal noise into heightmaps, converts them into 3D meshes, and drops you into a walkable first-person [Ursina](https://www.ursinaengine.org/) environment.

<img src="noises/fbm.png" alt="FBm noise sample" width="128"> <img src="noises/perlin.png" alt="Perlin noise sample" width="128"> <img src="noises/billow.png" alt="Billow noise sample" width="128"> <img src="noises/ridged.png" alt="Ridged noise sample" width="128">

## Features

- Noise presets: Perlin, Simplex, FBm, Billow, Ridged
- Heightmap to mesh conversion with OBJ export
- First-person preview using Ursina Engine
- Jupyter notebook for terrain analysis and visualization

## Requirements

- Python 3.10+
- NumPy
- Matplotlib
- noise
- PyYAML
- Ursina
- Jupyter (for the notebook)

## Installation

```bash
pip install -r requirements.txt
```

### If `noise` fails to install

The `noise` package may need to build a wheel on some platforms. The steps below are for Windows:

1. Install [Visual Studio Build Tools for C++](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
2. During setup, select **Desktop development with C++**.
3. Try the installation again:

   ```bash
   pip install noise
   ```

The wheel build should succeed this time.

## Usage

### 1. Generate and export a mesh

```bash
python generate.py
```

This writes an OBJ file to `meshes/`, ready to import into Blender or MeshLab.

### 2. Preview in first-person

```bash
python render.py
```

This loads the generated mesh in a minimal Ursina environment so you can walk around it. It's bare-bones, but it's a quick way to see whether the terrain feels right. Run `generate.py` first, since the preview needs the OBJ file to exist.

The preview opens fullscreen.

### 3. Inspect in the notebook

Open `analysis.ipynb` for heightmap inspection and 3D terrain visualization.

## Configuration

Settings live in `config.yaml`. The defaults are a 128x128 FBm terrain with a fixed seed:

```yaml
terrain:
  width: 128
  height: 128

noise:
  type: "fbm"       # fbm | perlin | simplex | billow | ridged
  seed: 42          # set to 0 for random
  scale: 25.0
  height_scale: 15.0

  octaves: 4        # not used for perlin and simplex
  persistance: 0.5
  lacunarity: 2.0

output:
  mesh_dir: "meshes/"
  mesh_name: "terrain.obj"
```

Change `noise.type` to switch presets, or set `noise.seed` to `0` for a different terrain each run. Re-run `generate.py` after any change.

## License

MIT License
