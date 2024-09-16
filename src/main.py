import moderngl
import moderngl_window as mglw
import numpy as np

class TriangleWindow(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "ModernGL Animated Triangle"
    window_size = (800, 600)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.prog = self.ctx.program(
            vertex_shader='''
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
            ''',
            fragment_shader='''
                #version 330
                uniform float u_time;
                out vec4 fragColor;
                void main() {
                    float green = sin(u_time) * 0.5 + 0.5;
                    fragColor = vec4(1.0, green, 0.2, 1.0);
                }
            ''',
        )
        
        vertices = np.array([
            -0.6, -0.6,
             0.6, -0.6,
             0.0,  0.6
        ], dtype='f4')
        
        self.vbo = self.ctx.buffer(vertices.tobytes())
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'in_vert')

    def render(self, time, frame_time):
        self.ctx.clear(0.2, 0.3, 0.3)
        self.prog['u_time'].value = time
        self.vao.render(moderngl.TRIANGLES)

if __name__ == '__main__':
    mglw.run_window_config(TriangleWindow)
