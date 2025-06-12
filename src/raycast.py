# raycast.py
import math
import arcade
from pyglet.math import Mat4, Vec3
from array import array
from arcade.gl import BufferDescription


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


def raycast(ray_start, ray_direction, objects, ray_length=100):
    from pyglet.math import Vec3

    # Ensure ray_direction is normalized
    if hasattr(ray_direction, "normalize"):
        ray_direction = ray_direction.normalize()
    else:
        ray_direction = Vec3(*ray_direction).normalize()

    closest_hit = None
    closest_distance = float('inf')
    
    # reverse the obj
    objects = objects[::-1]
    
    # Iterate through all objects in the scene
    for obj in objects:
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
            # gltf model
            body = obj["geometry"][0]
            positions = body["positions"]  # Use the mesh's vertex positions
            indices = body["indices"] if "indices" in body else None
            if indices:
                num_triangles = len(indices) // 3
                model_origin = obj["object"].get_world_position()
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