from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

from engine.config import load_config, get_mesh


config = load_config()
terrain = config["terrain"]
noise = config["noise"]
mesh = get_mesh(config)

width, height = int(terrain["width"]), int(terrain["height"])
scale, height_scale = int(noise["scale"]), int(noise["height_scale"])

if not mesh.exists():
    raise FileNotFoundError('obj file not found, run "generate.py" first.')

app = Ursina()

Sky()

Entity(
    model=str(mesh),
    double_sided=True,
    collider="box", # use "mesh" to consider height
)

Text(
    text='You can jump mid-air.\nPress "esc" to exit.',
    position=window.top_left + Vec2(0.025, -0.025),
    scale=2.5
)

player = FirstPersonController(
    position=(Vec3((width / -2), scale*height_scale, (height / 2)))
)

player.jump_height = 2*scale
player.speed = 2*scale
player.gravity = 2

# Cheesy way to allow the player to jump mid-air
original = player.jump
def air_jump():
    player.grounded = True
    player.air_time = 0
    original()
player.jump = air_jump

def input(key):
    if key == "escape":
        app.quit()
    

if __name__ == "__main__":
    window.fullscreen = True
    app.run()
