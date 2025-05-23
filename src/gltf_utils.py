import arcade
import arcade.resources
from pyglet.math import Vec3
from array import array
from arcade.gl import BufferDescription
from pygltflib import GLTF2
import numpy as np
import os
import struct


def load_gltf(self, gltf, bin_data, scale=Vec3(0.2, 0.2, 0.2)):
    """
    Load a GLTF file and extract vertex, index, and material data.
    Apply scaling to the vertex positions.
    """

    geometries = []  # List to store all geometries

    # Iterate through all meshes in the GLTF file
    for i, mesh in enumerate(gltf.meshes):
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

            # vertex buffer
            combined_data = []
            for i in range(pos_accessor.count):
                # Add position (3 floats)
                combined_data.extend(pos_data[i * 3:i * 3 + 3])
            vertex_buffer = self.ctx.buffer(
                data=array('f', combined_data).tobytes())

            # === INDEX (optional) ===
            index_buffer = None
            if primitive.indices is not None:
                idx_accessor = gltf.accessors[primitive.indices]
                idx_view = gltf.bufferViews[idx_accessor.bufferView]
                idx_offset = (idx_view.byteOffset or 0) + (idx_accessor.byteOffset or 0)

                component_size = {
                    5121: 1,  # UNSIGNED_BYTE
                    5123: 2,  # UNSIGNED_SHORT
                    5125: 4   # UNSIGNED_INT
                }[idx_accessor.componentType]

                idx_length = idx_accessor.count * component_size
                index_data = bin_data[idx_offset:idx_offset + idx_length]

                # Decode index_data to a Python list
                if idx_accessor.componentType == 5121:  # UNSIGNED_BYTE
                    fmt = f'{idx_accessor.count}B'
                elif idx_accessor.componentType == 5123:  # UNSIGNED_SHORT
                    fmt = f'{idx_accessor.count}H'
                elif idx_accessor.componentType == 5125:  # UNSIGNED_INT
                    fmt = f'{idx_accessor.count}I'
                else:
                    raise ValueError("Unsupported index component type")

                indices = list(struct.unpack(fmt, index_data))
            else:
                # No indices: generate default
                vertex_count = pos_accessor.count
                indices = list(range(vertex_count))

            index_buffer = self.ctx.buffer(data=index_data)
            
            geometry = self.ctx.geometry(
                content=[BufferDescription(
                    vertex_buffer, "3f", ["in_pos"])],
                index_buffer=index_buffer,
                index_element_size=component_size,
                mode=self.ctx.TRIANGLES
            )
            
            # === MATERIAL ===
            material = gltf.materials[primitive.material]
            base_color_factor = material.pbrMetallicRoughness.baseColorFactor or [
                1.0, 1.0, 1.0, 1.0]
            base_color_texture_index = material.pbrMetallicRoughness.baseColorTexture.index if material.pbrMetallicRoughness.baseColorTexture else None

            # Store geometry and material data
            geometries.append({
                "geometry": geometry,
                "base_color_factor": base_color_factor,
                "indices": indices,  # <--- Add this line
            })

    return geometries


# def load_gltf(self, gltf, bin_data, scale=Vec3(0.2, 0.2, 0.2)):
#     """
#     Load a GLTF file and extract vertex, index, and material data.
#     Apply scaling to the vertex positions.
#     """

#     geometries = []

#     # Handle skin data
#     skin = gltf.skins[0] if gltf.skins else None
#     joint_count = len(skin.joints) if skin else 0

#     # Parse inverse bind matrices
#     if skin:
#         ibm_accessor = gltf.accessors[skin.inverseBindMatrices]
#         ibm_view = gltf.bufferViews[ibm_accessor.bufferView]
#         ibm_offset = (ibm_view.byteOffset or 0) + \
#             (ibm_accessor.byteOffset or 0)
#         ibm_length = ibm_accessor.count * 64
#         ibm_data = bin_data[ibm_offset:ibm_offset + ibm_length]
#         inverse_bind_matrices = np.frombuffer(
#             ibm_data, dtype=np.float32).reshape((ibm_accessor.count, 4, 4))
#     else:
#         inverse_bind_matrices = []

#     for mesh in gltf.meshes:
#         for primitive in mesh.primitives:
#             # === POSITION ===
#             pos_accessor = gltf.accessors[primitive.attributes.POSITION]
#             pos_view = gltf.bufferViews[pos_accessor.bufferView]
#             pos_offset = (pos_view.byteOffset or 0) + \
#                 (pos_accessor.byteOffset or 0)
#             pos_length = pos_accessor.count * 12
#             pos_data = np.frombuffer(
#                 bin_data[pos_offset:pos_offset + pos_length], dtype=np.float32)
#             pos_data = pos_data.reshape((-1, 3)) * [scale.x, scale.y, scale.z]

#             # === UV ===
#             uv_data = np.zeros((pos_accessor.count, 2), dtype=np.float32)
#             if hasattr(primitive.attributes, "TEXCOORD_0"):
#                 uv_accessor = gltf.accessors[primitive.attributes.TEXCOORD_0]
#                 uv_view = gltf.bufferViews[uv_accessor.bufferView]
#                 uv_offset = (uv_view.byteOffset or 0) + \
#                     (uv_accessor.byteOffset or 0)
#                 uv_length = uv_accessor.count * 8
#                 uv_data = np.frombuffer(
#                     bin_data[uv_offset:uv_offset + uv_length], dtype=np.float32).reshape((-1, 2))

#             # === JOINTS_0 & WEIGHTS_0 ===
#             # Use uint8 for joints
#             joints_data = np.zeros((pos_accessor.count, 4), dtype=np.uint8)
#             weights_data = np.zeros((pos_accessor.count, 4), dtype=np.float32)
#             if skin and hasattr(primitive.attributes, "JOINTS_0") and hasattr(primitive.attributes, "WEIGHTS_0"):
#                 joint_accessor = gltf.accessors[primitive.attributes.JOINTS_0]
#                 joint_view = gltf.bufferViews[joint_accessor.bufferView]
#                 joint_offset = (joint_view.byteOffset or 0) + \
#                     (joint_accessor.byteOffset or 0)

#                 # Determine dtype for joints
#                 if joint_accessor.componentType == 5121:  # UNSIGNED_BYTE
#                     joint_dtype = np.uint8
#                 elif joint_accessor.componentType == 5123:  # UNSIGNED_SHORT
#                     joint_dtype = np.uint16
#                 else:
#                     raise ValueError(
#                         f"Unsupported JOINTS_0 componentType {joint_accessor.componentType}")

#                 raw_joints = np.frombuffer(
#                     bin_data[joint_offset:joint_offset +
#                              joint_accessor.count * 4 * np.dtype(joint_dtype).itemsize],
#                     dtype=joint_dtype
#                 ).reshape((-1, 4))

#                 # If ushort, cast down to uint8
#                 if joint_dtype == np.uint16:
#                     joints_data = raw_joints.astype(np.uint8)
#                 else:
#                     joints_data = raw_joints

#                 weight_accessor = gltf.accessors[primitive.attributes.WEIGHTS_0]
#                 weight_view = gltf.bufferViews[weight_accessor.bufferView]
#                 weight_offset = (weight_view.byteOffset or 0) + \
#                     (weight_accessor.byteOffset or 0)
#                 weights_data = np.frombuffer(
#                     bin_data[weight_offset:weight_offset +
#                              weight_accessor.count * 16], dtype=np.float32
#                 ).reshape((-1, 4))

#             # Combine all vertex attributes
#             vertex_buffer = self.ctx.buffer(data=np.hstack(
#                 [pos_data, uv_data]).astype(np.float32).tobytes())
#             joint_buffer = self.ctx.buffer(data=joints_data.tobytes())
#             weight_buffer = self.ctx.buffer(data=weights_data.tobytes())

#             # === INDEX BUFFER ===
#             index_buffer = None
#             component_size = 4
#             if primitive.indices is not None:
#                 idx_accessor = gltf.accessors[primitive.indices]
#                 idx_view = gltf.bufferViews[idx_accessor.bufferView]
#                 idx_offset = (idx_view.byteOffset or 0) + \
#                     (idx_accessor.byteOffset or 0)
#                 component_size = {5121: 1, 5123: 2, 5125: 4}[
#                     idx_accessor.componentType]
#                 idx_length = idx_accessor.count * component_size
#                 index_data = bin_data[idx_offset:idx_offset + idx_length]
#                 index_buffer = self.ctx.buffer(data=index_data)

#             # Create geometry
#             geometry = self.ctx.geometry(
#                 content=[
#                     BufferDescription(vertex_buffer, "3f 2f",
#                                       ["in_pos", "in_uv"]),
#                     # <-- Use 4u1 for uint8
#                     BufferDescription(joint_buffer, "4u1", ["in_joints"]),
#                     BufferDescription(weight_buffer, "4f", ["in_weights"])
#                 ],
#                 index_buffer=index_buffer,
#                 index_element_size=component_size,
#                 mode=self.ctx.TRIANGLES
#             )

#             # === MATERIAL ===
#             material = gltf.materials[primitive.material]
#             base_color_factor = material.pbrMetallicRoughness.baseColorFactor or [
#                 1.0, 1.0, 1.0, 1.0]
#             base_color_texture_index = material.pbrMetallicRoughness.baseColorTexture.index if material.pbrMetallicRoughness.baseColorTexture else None

#             # Attach shader program
#             shader_program = self.GLTF_program

#             geometries.append({
#                 "geometry": geometry,
#                 "base_color_factor": base_color_factor,
#                 "joint_count": joint_count,
#                 "inverse_bind_matrices": inverse_bind_matrices,
#                 "program": shader_program
#             })

#             # # Simple geometry and material data
#             # geometries.append({
#             #     "geometry": geometry,
#             #     "base_color_factor": base_color_factor,

#             # })

#     print(f"Loaded {len(geometries)} geometries")
#     return geometries
