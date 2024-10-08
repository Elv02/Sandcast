import raylib  # raylib-python-cffi
from raylib import ffi
import numpy as np
import math

# Initialization
screen_width = 800
screen_height = 600
raylib.InitWindow(screen_width, screen_height, b"Raylib Animated Triangle")
raylib.SetTargetFPS(60)

# Load shaders
vertex_shader_code = b"""
    #version 330
    in vec2 in_vert;
    uniform float u_time;
    void main() {
        float angle = u_time;
        float scale = sin(u_time) * 0.5 + 1.0;
        mat2 rotation = mat2(
            cos(angle), -sin(angle),
            sin(angle),  cos(angle)
        );
        mat2 scaling = mat2(
            scale, 0.0,
            0.0,  scale
        );
        vec2 transformed_vert = rotation * scaling * in_vert;
        gl_Position = vec4(transformed_vert, 0.0, 1.0);
    }
"""

fragment_shader_code = b"""
    #version 330
    uniform float u_time;
    out vec4 fragColor;
    void main() {
        float green = sin(u_time) * 0.5 + 0.5;
        fragColor = vec4(1.0, green, 0.2, 1.0);
    }
"""

shader = raylib.LoadShaderFromMemory(vertex_shader_code, fragment_shader_code)
time_location = raylib.GetShaderLocation(shader, b"u_time")

# Define the vertices for the triangle
vertices = np.array([
    -0.6, -0.6,
     0.6, -0.6,
     0.0,  0.6
], dtype=np.float32)

# Main game loop
while not raylib.WindowShouldClose():
    time = raylib.GetTime()

    # Update time in shader
    raylib.SetShaderValue(shader, time_location, ffi.new("float[1]", [time]), raylib.SHADER_UNIFORM_FLOAT)

    # Start Drawing
    raylib.BeginDrawing()
    raylib.ClearBackground(raylib.RAYWHITE)
    
    raylib.BeginShaderMode(shader)
    
    # Custom immediate-mode drawing (OpenGL-style)
    raylib.rlPushMatrix()
    raylib.rlBegin(raylib.RL_TRIANGLES)
    
    # Set vertex positions from the array
    raylib.rlVertex2f(vertices[0], vertices[1])
    raylib.rlVertex2f(vertices[2], vertices[3])
    raylib.rlVertex2f(vertices[4], vertices[5])
    
    raylib.rlEnd()
    raylib.rlPopMatrix()
    
    raylib.EndShaderMode()
    
    raylib.EndDrawing()

# De-initialization
raylib.UnloadShader(shader)
raylib.CloseWindow()
