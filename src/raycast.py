# raycast.py
import math
import arcade
from pyglet.math import Vec3
import numpy as np

# Optional: Use moderngl for GPU acceleration
try:
    import moderngl
    MODERNGL_AVAILABLE = True
except ImportError:
    MODERNGL_AVAILABLE = False

def ray_intersects_triangle(ray_origin, ray_dir, v0, v1, v2):
    EPSILON = 1e-6
    edge1 = v1 - v0
    edge2 = v2 - v0
    h = ray_dir.cross(edge2)
    a = edge1.dot(h)
    if -EPSILON < a < EPSILON:
        return False, None  # Ray is parallel to triangle
    f = 1.0 / a
    s = ray_origin - v0
    u = f * s.dot(h)
    if u < 0.0 or u > 1.0:
        return False, None
    q = s.cross(edge1)
    v = f * ray_dir.dot(q)
    if v < 0.0 or u + v > 1.0:
        return False, None
    t = f * edge2.dot(q)
    if t > EPSILON:
        return True, t  # Intersection at distance t
    else:
        return False, None


def ray_intersects_aabb(ray_start, ray_direction, min_x, max_x, min_y, max_y, min_z, max_z):
    t_min = (min_x - ray_start.x) / \
        ray_direction.x if ray_direction.x != 0 else float('-inf')
    t_max = (max_x - ray_start.x) / \
        ray_direction.x if ray_direction.x != 0 else float('inf')

    if t_min > t_max:
        t_min, t_max = t_max, t_min

    ty_min = (min_y - ray_start.y) / \
        ray_direction.y if ray_direction.y != 0 else float('-inf')
    ty_max = (max_y - ray_start.y) / \
        ray_direction.y if ray_direction.y != 0 else float('inf')

    if ty_min > ty_max:
        ty_min, ty_max = ty_max, ty_min

    if (t_min > ty_max) or (ty_min > t_max):
        return False, None

    if ty_min > t_min:
        t_min = ty_min
    if ty_max < t_max:
        t_max = ty_max

    tz_min = (min_z - ray_start.z) / \
        ray_direction.z if ray_direction.z != 0 else float('-inf')
    tz_max = (max_z - ray_start.z) / \
        ray_direction.z if ray_direction.z != 0 else float('inf')

    if tz_min > tz_max:
        tz_min, tz_max = tz_max, tz_min

    if (t_min > tz_max) or (tz_min > t_max):
        return False, None

    if tz_min > t_min:
        t_min = tz_min
    if tz_max < t_max:
        t_max = tz_max

    if t_min < 0 and t_max < 0:
        return False, None  # Both intersections are behind the ray

    return True, t_min if t_min > 0 else t_max


def gpu_ray_intersects_mesh(ray_origin, ray_dir, positions, indices):
    if not MODERNGL_AVAILABLE:
        raise ImportError("moderngl is required for GPU ray-mesh intersection.")
    ctx = moderngl.create_standalone_context()
    n_tris = len(indices) // 3
    pos_buf = ctx.buffer(np.array(positions, dtype='f4').tobytes())
    idx_buf = ctx.buffer(np.array(indices, dtype='i4').tobytes())
    result_buf = ctx.buffer(reserve=4 * n_tris)
    shader = ctx.compute_shader('''
    #version 430
    layout(std430, binding = 0) buffer Positions { float positions[]; };
    layout(std430, binding = 1) buffer Indices { int indices[]; };
    layout(std430, binding = 2) buffer Results { float results[]; };
    uniform vec3 ray_origin;
    uniform vec3 ray_dir;
    void main() {
        uint i = gl_GlobalInvocationID.x;
        int idx0 = indices[i*3+0];
        int idx1 = indices[i*3+1];
        int idx2 = indices[i*3+2];
        vec3 v0 = vec3(positions[idx0*3+0], positions[idx0*3+1], positions[idx0*3+2]);
        vec3 v1 = vec3(positions[idx1*3+0], positions[idx1*3+1], positions[idx1*3+2]);
        vec3 v2 = vec3(positions[idx2*3+0], positions[idx2*3+1], positions[idx2*3+2]);
        float EPSILON = 1e-6;
        vec3 edge1 = v1 - v0;
        vec3 edge2 = v2 - v0;
        vec3 h = cross(ray_dir, edge2);
        float a = dot(edge1, h);
        if (abs(a) < EPSILON) { results[i] = -1.0; return; }
        float f = 1.0 / a;
        vec3 s = ray_origin - v0;
        float u = f * dot(s, h);
        if (u < 0.0 || u > 1.0) { results[i] = -1.0; return; }
        vec3 q = cross(s, edge1);
        float v = f * dot(ray_dir, q);
        if (v < 0.0 || u + v > 1.0) { results[i] = -1.0; return; }
        float t = f * dot(edge2, q);
        results[i] = (t > EPSILON) ? t : -1.0;
    }
    ''')
    shader['ray_origin'].value = tuple(ray_origin)
    shader['ray_dir'].value = tuple(ray_dir)
    pos_buf.bind_to_storage_buffer(0)
    idx_buf.bind_to_storage_buffer(1)
    result_buf.bind_to_storage_buffer(2)
    shader.run(group_x=n_tris)
    results = np.frombuffer(result_buf.read(), dtype='f4')
    min_t = np.min(results[results > 0]) if np.any(results > 0) else None
    return min_t

def raycast(ray_start, ray_direction, objects, ray_length=100, use_gpu=False):
    from pyglet.math import Vec3

    # Ensure ray_direction is normalized
    if hasattr(ray_direction, "normalize"):
        ray_direction = ray_direction.normalize()
    else:
        ray_direction = Vec3(*ray_direction).normalize()

    closest_hit = None
    closest_distance = float('inf')
    
    # Iterate through all objects in the scene
    for obj in objects[::-1]:
        if obj["id"] == 1:  # Wall
            positions = obj["buffer_data"]
            num_vertices = len(positions) // 5
            # Check for intersection with the wall's bounding box
            min_x = min(positions[i * 5] for i in range(num_vertices))
            max_x = max(positions[i * 5] for i in range(num_vertices))
            min_y = min(positions[i * 5 + 1] for i in range(num_vertices))
            max_y = max(positions[i * 5 + 1] for i in range(num_vertices))
            min_z = min(positions[i * 5 + 2] for i in range(num_vertices))
            max_z = max(positions[i * 5 + 2] for i in range(num_vertices))

            hit, distance = ray_intersects_aabb(
                ray_start, ray_direction, min_x, max_x, min_y, max_y, min_z, max_z
            )
            # Only consider hits within ray_length
            if hit and 0 <= distance <= ray_length and distance < closest_distance:
                return obj, False

        if obj["id"] == 10:
            if obj["type"] == 4:  # Mini boss
                # For minibosses, we need to check geometry being used
                geometry = obj["geometry"][0] if obj["object"].get_form() == 1 else obj["geometry"][1]
            else:
                geometry = obj["geometry"]
            # gltf model
            body = geometry[0]
            positions = body["positions"]  # Use the mesh's vertex positions
            indices = body["indices"] if "indices" in body else None
            model_origin = obj["object"].get_world_position()
            # --- AABB culling for mesh ---
            num_vertices = len(positions) // 3
            min_x = min(positions[i * 3] + model_origin.x for i in range(num_vertices))
            max_x = max(positions[i * 3] + model_origin.x for i in range(num_vertices))
            min_y = min(positions[i * 3 + 1] + model_origin.y for i in range(num_vertices))
            max_y = max(positions[i * 3 + 1] + model_origin.y for i in range(num_vertices))
            min_z = min(positions[i * 3 + 2] + model_origin.z for i in range(num_vertices))
            max_z = max(positions[i * 3 + 2] + model_origin.z for i in range(num_vertices))
            hit, distance = ray_intersects_aabb(
                ray_start, ray_direction, min_x, max_x, min_y, max_y, min_z, max_z
            )
            if not hit:
                continue  # Skip triangle tests for this mesh
            # --- End AABB culling ---
            if indices and use_gpu and MODERNGL_AVAILABLE:
                # Use GPU for intersection
                # Offset positions by model_origin
                pos_np = np.array(positions, dtype='f4').reshape(-1, 3)
                pos_np += np.array([model_origin.x, model_origin.y, model_origin.z], dtype='f4')
                min_t = gpu_ray_intersects_mesh(
                    (ray_start.x, ray_start.y, ray_start.z),
                    (ray_direction.x, ray_direction.y, ray_direction.z),
                    pos_np.flatten(),
                    np.array(indices, dtype='i4')
                )
                if min_t is not None and 0 <= min_t <= ray_length and min_t < closest_distance:
                    # For headshot logic, you can add barycentric interpolation if needed
                    return obj, False
            elif indices:
                num_triangles = len(indices) // 3
                for i in range(num_triangles):
                    idx0 = indices[i * 3]
                    idx1 = indices[i * 3 + 1]
                    idx2 = indices[i * 3 + 2]
                    v0 = Vec3(
                        positions[idx0 * 3] + model_origin.x,
                        positions[idx0 * 3 + 1] + model_origin.y,
                        positions[idx0 * 3 + 2] + model_origin.z
                    )
                    v1 = Vec3(
                        positions[idx1 * 3] + model_origin.x,
                        positions[idx1 * 3 + 1] + model_origin.y,
                        positions[idx1 * 3 + 2] + model_origin.z
                    )
                    v2 = Vec3(
                        positions[idx2 * 3] + model_origin.x,
                        positions[idx2 * 3 + 1] + model_origin.y,
                        positions[idx2 * 3 + 2] + model_origin.z
                    )
                    hit, distance = ray_intersects_triangle(
                        ray_start, ray_direction, v0, v1, v2)
                    # Only consider hits within ray_length
                    if hit and 0 <= distance <= ray_length and distance < closest_distance:
                        # if y coordinate of the hit point is greater than 0.5, return headshot
                        if v0.y > 0.5 and v1.y > 0.5 and v2.y > 0.5:
                            return obj, True
                        else:
                            return obj, False

    return None, False
