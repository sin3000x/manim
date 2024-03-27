#version 330

layout (points) in;
layout (triangle_strip, max_vertices = 4) out;

<<<<<<< HEAD
// Needed for get_gl_Position
uniform vec2 frame_shape;
uniform float focal_distance;
uniform float is_fixed_in_frame;
uniform float anti_alias_width;

in vec3 v_point[1];
in float v_radius[1];
in vec4 v_color[1];

out vec4 color;
out float radius;
out vec2 center;
out vec2 point;

#INSERT get_gl_Position.glsl

void main() {
    color = v_color[0];
    radius = v_radius[0];
    center = v_point[0].xy;
    
    radius = v_radius[0] / max(1.0 - v_point[0].z / focal_distance / frame_shape.y, 0.0);
    float rpa = radius + anti_alias_width;

    for(int i = 0; i < 4; i++){
        // To account for perspective

        int x_index = 2 * (i % 2) - 1;
        int y_index = 2 * (i / 2) - 1;
        vec3 corner = v_point[0] + vec3(x_index * rpa, y_index * rpa, 0.0);

        gl_Position = get_gl_Position(corner);
        point = corner.xy;
        EmitVertex();
=======
uniform float pixel_size;
uniform float anti_alias_width;
uniform float frame_scale;
uniform vec3 camera_position;

in vec3 v_point[1];
in float v_radius[1];
in vec4 v_rgba[1];

out vec4 color;
out float scaled_aaw;
out vec3 point;
out vec3 to_cam;
out vec3 center;
out float radius;
out vec2 uv_coords;

#INSERT emit_gl_Position.glsl

void main(){
    color = v_rgba[0];
    radius = v_radius[0];
    center = v_point[0];
    scaled_aaw = (anti_alias_width * pixel_size) / v_radius[0];

    to_cam = normalize(camera_position - v_point[0]);
    vec3 right = v_radius[0] * normalize(cross(vec3(0, 1, 1), to_cam));
    vec3 up = v_radius[0] * normalize(cross(to_cam, right));

    for(int i = -1; i < 2; i += 2){
        for(int j = -1; j < 2; j += 2){
            point = v_point[0] + i * right + j * up;
            uv_coords = vec2(i, j);
            emit_gl_Position(point);
            EmitVertex();
        }
>>>>>>> 4729e44e057fcc4f02b4d6bdb64c010af4a540b3
    }
    EndPrimitive();
}