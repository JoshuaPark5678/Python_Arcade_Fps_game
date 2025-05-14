# Organize imports
import arcade
import arcade.resources
from pyglet.math import Mat4, Vec3
from array import array
from arcade.gl import BufferDescription
from pygltflib import GLTF2
import time
from struct import unpack

def load_gltf(self, gltf_path, bin_path, scale=Vec3(1.0, 1.0, 1.0)):
    """
    Load a GLTF file and extract vertex, index, and material data.
    Apply scaling to the vertex positions.
    """
    print(f"Loading GLTF: {gltf_path}")
    gltf = GLTF2().load(gltf_path)

    with open(bin_path, "rb") as f:
        bin_data = f.read()

    geometries = []  # List to store all geometries

    # Iterate through all meshes in the GLTF file
    for mesh in gltf.meshes:
        for primitive in mesh.primitives:
            # === POSITION ===
            pos_accessor = gltf.accessors[primitive.attributes.POSITION]
            pos_view = gltf.bufferViews[pos_accessor.bufferView]
            pos_offset = (pos_view.byteOffset or 0) + \
                (pos_accessor.byteOffset or 0)
            pos_length = pos_accessor.count * 12  # 3 floats * 4 bytes
            pos_data = array('f', bin_data[pos_offset:pos_offset + pos_length])

            # Apply scaling to the vertex positions
            for i in range(pos_accessor.count):
                pos_data[i * 3] *= scale.x  # Scale X
                pos_data[i * 3 + 1] *= scale.y  # Scale Y
                pos_data[i * 3 + 2] *= scale.z  # Scale Z

            # === UV (optional) ===
            uv_data = []
            if hasattr(primitive.attributes, "TEXCOORD_0"):
                uv_accessor = gltf.accessors[primitive.attributes.TEXCOORD_0]
                uv_view = gltf.bufferViews[uv_accessor.bufferView]
                uv_offset = (uv_view.byteOffset or 0) + \
                    (uv_accessor.byteOffset or 0)
                uv_length = uv_accessor.count * 8  # 2 floats * 4 bytes
                uv_data = array('f', bin_data[uv_offset:uv_offset + uv_length])

            # Combine position and UV data into a single buffer
            if uv_data:
                combined_data = []
                for i in range(pos_accessor.count):
                    # Add position (3 floats)
                    combined_data.extend(pos_data[i * 3:i * 3 + 3])
                    # Add UV (2 floats)
                    combined_data.extend(uv_data[i * 2:i * 2 + 2])
                # Ensure the buffer size aligns with the attribute layout
                vertex_buffer = self.ctx.buffer(
                    data=array('f', combined_data).tobytes())
            else:
                # If no UV data, pad with zeros to align with the buffer description
                combined_data = []
                for i in range(pos_accessor.count):
                    # Add position (3 floats)
                    combined_data.extend(pos_data[i * 3:i * 3 + 3])
                    # Add default UV (2 floats)
                    combined_data.extend([0.0, 0.0])
                vertex_buffer = self.ctx.buffer(
                    data=array('f', combined_data).tobytes())

            # === INDEX (optional) ===
            index_buffer = None
            if primitive.indices is not None:
                idx_accessor = gltf.accessors[primitive.indices]
                idx_view = gltf.bufferViews[idx_accessor.bufferView]
                idx_offset = (idx_view.byteOffset or 0) + \
                    (idx_accessor.byteOffset or 0)

                component_size = {
                    5121: 1,  # UNSIGNED_BYTE
                    5123: 2,  # UNSIGNED_SHORT
                    5125: 4   # UNSIGNED_INT
                }[idx_accessor.componentType]

                idx_length = idx_accessor.count * component_size
                index_data = bin_data[idx_offset:idx_offset + idx_length]

                index_buffer = self.ctx.buffer(data=index_data)

                geometry = self.ctx.geometry(
                    content=[BufferDescription(
                        vertex_buffer, "3f 2f", ["in_pos", "in_uv"])],
                    index_buffer=index_buffer,
                    index_element_size=component_size,
                    mode=self.ctx.TRIANGLES
                )
            else:
                geometry = self.ctx.geometry(
                    content=[BufferDescription(
                        vertex_buffer, "3f 2f", ["in_pos", "in_uv"])],
                    mode=self.ctx.TRIANGLES
                )

            # === MATERIAL ===
            material = gltf.materials[primitive.material]
            base_color_factor = material.pbrMetallicRoughness.baseColorFactor or [
                1.0, 1.0, 1.0, 1.0]
            base_color_texture_index = material.pbrMetallicRoughness.baseColorTexture.index if material.pbrMetallicRoughness.baseColorTexture else None

            # Load the base color texture if it exists
            base_color_texture = None
            if base_color_texture_index is not None:
                texture_info = gltf.textures[base_color_texture_index]
                image_info = gltf.images[texture_info.source]
                texture_path = gltf_path.rsplit(
                    "/", 1)[0] + "/" + image_info.uri
                texture = arcade.load_texture(texture_path)
                base_color_texture = self.ctx.texture(
                    size=(texture.width, texture.height),
                    components=4,
                    data=texture.image.tobytes()
                )

            # Store geometry and material data
            geometries.append({
                "geometry": geometry,
                "base_color_factor": base_color_factor,
                "base_color_texture": base_color_texture
            })
            
    
    return geometries

def get_node_map(self, gltf_path):
    """
    Create a mapping of node indices to their corresponding GLTF nodes.
    """
    gltf = GLTF2().load(gltf_path)
    node_map = {}
    for i, node in enumerate(gltf.nodes):
        node_map[i] = {
            "name": node.name or f"Node_{i}",
            "translation": node.translation or [0.0, 0.0, 0.0],
            "rotation": node.rotation or [0.0, 0.0, 0.0, 1.0],
            "scale": node.scale or [1.0, 1.0, 1.0]
        }
    return node_map

def load_animations(self, gltf_path, bin_path):
    
    gltf = GLTF2().load(gltf_path)
    
    with open(bin_path, "rb") as f:
        bin_data = f.read()
    
    animations = []
    # Iterate through all animations in the GLTF file
    for anim in gltf.animations:
        anim_data = {
            "name": anim.name or "Unnamed",
            "channels": []
        }

        for channel in anim.channels:
            sampler = anim.samplers[channel.sampler]

            # Get input (times)
            input_accessor = gltf.accessors[sampler.input]
            input_view = gltf.bufferViews[input_accessor.bufferView]
            input_offset = (input_view.byteOffset or 0) + (input_accessor.byteOffset or 0)
            input_count = input_accessor.count
            input_data = unpack(
                f"<{input_count}f",
                bin_data[input_offset:input_offset + input_count * 4]
            )

            # Get output (values)
            output_accessor = gltf.accessors[sampler.output]
            output_view = gltf.bufferViews[output_accessor.bufferView]
            output_offset = (output_view.byteOffset or 0) + (output_accessor.byteOffset or 0)
            output_count = output_accessor.count

            # Determine value format
            path = channel.target.path  # translation, rotation, scale, weights
            if path == "translation" or path == "scale":
                component_count = 3
            elif path == "rotation":
                component_count = 4
            else:
                component_count = 1  # fallback or weights

            output_data = unpack(
                f"<{output_count * component_count}f",
                bin_data[output_offset:output_offset + output_count * component_count * 4]
            )

            # Group output data into tuples
            grouped_output = [
                tuple(output_data[i:i + component_count])
                for i in range(0, len(output_data), component_count)
            ]

            anim_data["channels"].append({
                "node": channel.target.node,
                "path": path,
                "interpolation": sampler.interpolation,
                "times": input_data,
                "values": grouped_output
            })

        animations.append(anim_data)
       
    return animations

# # Animation interpolation functions
# import numpy as np
# from scipy.spatial.transform import Rotation as R

# def interpolate_linear(times, values, t):
#     if t <= times[0]:
#         return values[0]
#     if t >= times[-1]:
#         return values[-1]

#     for i in range(1, len(times)):
#         if t < times[i]:
#             t0, t1 = times[i - 1], times[i]
#             v0, v1 = values[i - 1], values[i]
#             factor = (t - t0) / (t1 - t0)
#             return tuple(v0[j] + factor * (v1[j] - v0[j]) for j in range(len(v0)))

#     return values[-1]

# def slerp_quaternion(q0, q1, t):
#     r0 = R.from_quat(q0)
#     r1 = R.from_quat(q1)
#     return tuple(R.slerp(0, 1, [r0, r1])(t).as_quat())

# def animate(self, animations, current_time, node_map):
#     for anim in animations:
#         for channel in anim["channels"]:
#             times = channel["times"]
#             values = channel["values"]
#             path = channel["path"]
#             node_index = channel["node"]
#             interpolation = channel["interpolation"]

#             # Skip if the node isn’t mapped
#             if node_index not in node_map:
#                 continue

#             # Only LINEAR interpolation supported for now
#             if interpolation != "LINEAR":
#                 continue

#             # Interpolate based on the path type
#             if path == "rotation":
#                 # SLERP for quaternions
#                 if current_time <= times[0]:
#                     value = values[0]
#                 elif current_time >= times[-1]:
#                     value = values[-1]
#                 else:
#                     for i in range(1, len(times)):
#                         if current_time < times[i]:
#                             t0, t1 = times[i - 1], times[i]
#                             q0, q1 = values[i - 1], values[i]
#                             factor = (current_time - t0) / (t1 - t0)
#                             value = slerp_quaternion(q0, q1, factor)
#                             break
#                 node_map[node_index].set_rotation(value)

#             elif path == "translation":
#                 value = interpolate_linear(times, values, current_time)
#                 node_map[node_index].set_position(value)

#             elif path == "scale":
#                 value = interpolate_linear(times, values, current_time)
#                 node_map[node_index].set_scale(value)
    
    
