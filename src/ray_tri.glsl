// GLSL version of ray_intersects_triangle
bool ray_intersects_triangle(
    vec3 ray_origin,
    vec3 ray_dir,
    vec3 v0,
    vec3 v1,
    vec3 v2,
    out float t
) {
    float EPSILON = 1e-6;
    vec3 edge1 = v1 - v0;
    vec3 edge2 = v2 - v0;
    vec3 h = cross(ray_dir, edge2);
    float a = dot(edge1, h);
    if (abs(a) < EPSILON)
        return false; // Ray is parallel to triangle

    float f = 1.0 / a;
    vec3 s = ray_origin - v0;
    float u = f * dot(s, h);
    if (u < 0.0 || u > 1.0)
        return false;

    vec3 q = cross(s, edge1);
    float v = f * dot(ray_dir, q);
    if (v < 0.0 || u + v > 1.0)
        return false;

    t = f * dot(edge2, q);
    if (t > EPSILON)
        return true; // Intersection at distance t
    else
        return false;
}