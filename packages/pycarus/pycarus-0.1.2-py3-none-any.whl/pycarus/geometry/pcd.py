import math
from pathlib import Path
from random import randint
from typing import Callable, Dict, List, Tuple, Union

import numpy as np  # type: ignore
import open3d as o3d  # type: ignore
import pytorch3d.transforms.transform3d as pt3d  # type: ignore
import torch
from einops import rearrange  # type: ignore


def read_pcd(pcd_path: Union[str, Path]) -> torch.Tensor:
    """Read a point cloud from a given file.

    The point cloud is returned as a torch tensor with shape (NUM_POINTS, D).
    D can be 3 (only XYZ coordinates), 6 (XYZ coordinates and
    normals) or 9 (XYZ coordinates, normals and colors).

    Args:
        pcd_path: The path of the point cloud file.

    Raises:
        ValueError: If the given file doesn't exist.

    Returns:
        A torch tensor with the loaded point cloud with shape (NUM_POINTS, D).
    """
    pcd_path = Path(pcd_path)
    if not pcd_path.exists():
        raise ValueError(f"The pcd file {str(pcd_path)} does not exists.")

    pcd_o3d = o3d.io.read_point_cloud(str(pcd_path))
    pcd_torch = torch.tensor(pcd_o3d.points)

    if len(pcd_o3d.normals) > 0:
        normals_torch = torch.tensor(pcd_o3d.normals)
        pcd_torch = torch.cat((pcd_torch, normals_torch), dim=-1)

    if len(pcd_o3d.colors) > 0:
        colors_torch = torch.tensor(pcd_o3d.colors)
        pcd_torch = torch.cat((pcd_torch, colors_torch), dim=-1)

    return pcd_torch


def normalize_pcd(pcd: torch.Tensor) -> torch.Tensor:
    """Normalize the given point cloud in the unit sphere.

    Coordinates are first express wrt to the point cloud centroid.
    Then, they are normalized wrt the maximum distance from the centroid.
    If present, normals and colors are preserved.

    Args:
        pcd: The point cloud to normalize with shape (NUM_POINTS, D).

    Returns:
        A torch tensor with the normalized point cloud with shape (NUM_POINTS, D).
    """
    pcd_copy = torch.clone(pcd)

    xyz = pcd_copy[:, :3]
    centroid = torch.mean(xyz, dim=0)
    xyz = xyz - centroid
    distances_from_centroid = torch.norm(xyz, p=2, dim=-1)  # type: ignore
    max_dist_from_centroid = torch.max(distances_from_centroid)
    xyz = xyz / max_dist_from_centroid

    normalized_pcd = torch.cat((xyz, pcd_copy[:, 3:]), dim=-1)

    return normalized_pcd


def farthest_point_sampling(pcd: torch.Tensor, num_points: int) -> torch.Tensor:
    """Sample the requested number of points from the given point cloud
    using farthest point sampling.

    Args:
        pcd: The input point cloud with shape (NUM_POINTS, D).
        num_points: Number of points to sample.

    Returns:
        A torch tensor with sampled points with shape (NUM_SAMPLED_POINTS, D).
    """
    pcd_copy = torch.clone(pcd)

    original_num_points, _ = pcd_copy.shape
    xyz = pcd_copy[:, :3]

    indexes_to_sample: List[int] = []
    distances = torch.ones((original_num_points,)) * 1e10
    farthest = torch.tensor(randint(0, original_num_points - 1))

    for i in range(num_points):
        indexes_to_sample.append(int(farthest))
        current = xyz[farthest, :]
        distances_from_current = torch.sum((xyz - current) ** 2, -1)
        mask = distances_from_current < distances
        distances[mask] = distances_from_current[mask]  # avoid picking previous point
        farthest = torch.argmax(distances)

    sampled_points = pcd_copy[indexes_to_sample]

    return sampled_points


def get_o3d_from_tensor(pcd: Union[torch.Tensor, np.ndarray]) -> o3d.geometry.PointCloud:
    """Get open3d point cloud from either numpy array or torch tensor.

    The input point cloud must have shape (NUM_POINTS, D), where D can be 3
    (only XYZ coordinates), 6 (XYZ coordinates and normals) or 9
    (XYZ coordinates, normals and colors).

    Args:
        pcd: The numpy or torch point cloud with shape (NUM_POINTS, D).

    Returns:
        The open3d point cloud.
    """
    pcd_o3d = o3d.geometry.PointCloud()

    pcd_o3d.points = o3d.utility.Vector3dVector(pcd[:, :3])

    if pcd.shape[1] >= 6:
        pcd_o3d.normals = o3d.utility.Vector3dVector(pcd[:, 3:6])

    if pcd.shape[1] == 9:
        pcd_o3d.colors = o3d.utility.Vector3dVector(pcd[:, 6:])

    return pcd_o3d


def get_distances_matrix(pcd: torch.Tensor) -> torch.Tensor:
    """Get euclidean distances between points as a matrix.

    Given a point cloud with shape (NUM_POINTS, D), this functions
    assumes that the first three element of each point are XYZ coordinates.
    Then, it creates a matrix with shape (NUM_POINTS, NUM_POINTS),
    where the i-th row contains the euclidean distances between
    the i-th point and all the other points.

    Args:
        pcd: The input point cloud with shape (NUM_POINTS, D)-

    Returns:
        The matrix with distances, with shape (NUM_POINTS, NUM_POINTS).
    """
    num_points = pcd.shape[0]
    xyz = pcd[:, :3]
    diff = torch.stack([xyz] * num_points)
    diff_t = rearrange(diff, "h w d -> w h d")
    distances = torch.norm((diff - diff_t), p=2, dim=-1)  # type: ignore
    return distances


def get_neighbours_distance(pcd: torch.Tensor, reduce_fn: str) -> float:
    """Compute median distance between neighbouring points.

    Args:
        pcd: The input point cloud with shape (NUM_POINTS, D).
        reduce_fn: The reduce function to apply to neighbours distances.
            Available options are "min", "max", "mean", "median", "std".

    Raises:
        ValueError: If the given reduce function is unknown.

    Returns:
        The median distance.
    """
    num_points = pcd.shape[0]
    distances = get_distances_matrix(pcd)
    distances[torch.eye(num_points).bool()] = float("inf")
    neighbours_distances = torch.min(distances, dim=-1)[0]

    rfns: Dict[str, Callable[[torch.Tensor], torch.Tensor]] = {
        "min": torch.min,
        "max": torch.max,
        "mean": torch.mean,
        "median": torch.median,
        "std": torch.std,
    }

    try:
        rfn = rfns[reduce_fn]
    except KeyError:
        raise ValueError("Unknown reduce function.")

    result = float(rfn(neighbours_distances).item())

    return result


def shuffle_pcd(pcd: torch.Tensor) -> torch.Tensor:
    """Shuffle the order of the point inside the point cloud.

    Args:
        pcd: The input point cloud.

    Returns:
        The shuffled point cloud.
    """

    pcd_copy = torch.clone(pcd)[torch.randperm(len(pcd))]

    return pcd_copy


def jitter_pcd(pcd: torch.Tensor, sigma: float = 0.01, clip: float = 0.05) -> torch.Tensor:
    """Jitter point cloud by adding random noise.

    Add a gaussian noise to each coordinates of each point in the input point cloud. The noise is
    sampled from a normal distribution with mean 0 and std 1 multiplied by sigma. Finally, the final
    amount of noise to add is clipped between -1*clip and clip.

    Args:
        pcd: The input point cloud with shape (NUM_POINTS, D).
        sigma: The sigma for the gaussian noise.
        clip: The clipping value.

    Returns:
        The jittered point cloud.
    """
    pcd_copy = torch.clone(pcd)
    noise = torch.clip(sigma * torch.randn(pcd.shape), min=-1 * clip, max=clip)
    jittered_pcd = pcd_copy + noise

    return jittered_pcd


def random_rotate_pcd(pcd: torch.Tensor) -> torch.Tensor:
    return torch.ones()


def random_drop_points(
    pcd: torch.Tensor, drop_percentage: float
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Random drop points in the point cloud.

    Args:
        pcd: The input point cloud with shape (NUM_POINTS, D).
        drop_percentage: The percentage of points to be removed.

    Returns:
        - The dropped point cloud.
        - The indices of points that have been keeped.
        - The indices of points that have been removed.
    """
    pcd_copy = torch.clone(pcd)
    size_pcd = len(pcd)
    num_pts_to_remove = math.ceil(size_pcd * drop_percentage)

    weights = torch.ones(size_pcd).float()
    indices_to_remove = torch.multinomial(weights, num_pts_to_remove, replacement=False)
    indices_pcd = torch.arange(size_pcd)
    indices_to_keep = ~indices_pcd.unsqueeze(1).eq(indices_to_remove).any(-1)

    pcd_droppped = pcd_copy[indices_to_keep, :]
    indices_to_keep = indices_pcd[indices_to_keep]

    return pcd_droppped, indices_to_keep, indices_to_remove


def _apply_pt3d_transform(
    pcd: torch.Tensor, transform: pt3d.Transform3d, transform_normals: bool
) -> torch.Tensor:
    """Apply PyTorch 3D transform to the input point cloud.

    This method is a wrapper to the PyTorch3D Transform3D in order to avoid to call separate
    methods to transform points and normals. If transform_normals is True also the normals are
    transformed, for some rigid transformation such as scale and transation this is not
    necessary.

    Args:
        pcd: The input point cloud with shape (NUM_POINTS, D).
        transform: The transform to apply.

    Returns:
        The transformed point cloud.
    """
    size_points = pcd.shape[1]
    pcd_transformed = transform.transform_points(pcd[:, :3])

    if size_points >= 6:
        normals = transform.transform_normals(pcd[:, 3:6]) if transform_normals else pcd[:, 3:6]
        pcd_transformed = torch.cat((pcd_transformed, normals), dim=-1)

    if size_points == 9:
        colors = pcd[:, 6:9]
        pcd_transformed = torch.cat((pcd_transformed, colors), dim=-1)

    return pcd_transformed


def affine(pcd: torch.Tensor, affine_transform: torch.Tensor) -> torch.Tensor:
    """Apply an affine transformation, typically a rigid motion matrix.

    This method applies a rotation and a translation to the input point cloud. We rely on the same
    convention of PyTorch3D, hence an affine matrix is stored using a row-major order:
      M = [ [Rxx, Ryx, Rzx, 0],
            [Rxy, Ryy, Rzy, 0],
            [Rxz, Ryz, Rzz, 0],
            [Tx,  Ty,  Tz,  1],]
    the rows of the matrix represent the bases of a coordinate system and the last row stores
    the translation vector. If the point cloud contains also the normals, only the rotation
    will be applied. Despite operating in with affine matrix the coordinates of the input points
    don't need to be in the affine space.

    Args:
        pcd: The input point cloud with shape (NUM_POINTS, D).
        affine_transform: The transformation to appyly with shape (4, 4).

    Returns:
        The transformed point cloud.
    """
    transform = pt3d.Transform3d(dtype=pcd.dtype, device=str(pcd.device), matrix=affine_transform)
    return _apply_pt3d_transform(pcd, transform=transform, transform_normals=True)


def rotate(pcd: torch.Tensor, rotation: torch.Tensor) -> torch.Tensor:
    """Rotate a point cloud give the input matrix.

    Rotate the cloud using the same convention as in PyTorch3D: a right-hand coordinate system,
    meaning that rotation about an axis with a positive angle results in a counter clockwise
    rotation, more info at (https://pytorch3d.readthedocs.io).
    The points are multiplied using post-multiplication: rotated_points = points * rotation.

    Args:
        pcd: The input point cloud with shape (NUM_POINTS, D).
        rotation: The rotation matrix with shape (3, 3).

    Returns:
        The rotated point cloud.
    """
    transform = pt3d.Rotate(rotation, dtype=pcd.dtype, device=str(pcd.device))
    return _apply_pt3d_transform(pcd, transform, transform_normals=True)


def scale(pcd: torch.Tensor, scale_factor: torch.Tensor) -> torch.Tensor:
    """Scale a point cloud given the input scale factor.

    Args:
        pcd: The input point cloud with shape (NUM_POINTS, D).
        scale: The scale factor for the x, y, z, dimensions with shape (3,).

    Returns:
        The scaled point cloud.
    """
    scale_x, scale_y, scale_z = scale_factor[0], scale_factor[1], scale_factor[2]
    transform = pt3d.Scale(x=scale_x, y=scale_y, z=scale_z, dtype=pcd.dtype, device=str(pcd.device))

    return _apply_pt3d_transform(pcd, transform, transform_normals=False)


def translate(pcd: torch.Tensor, translation: torch.Tensor) -> torch.Tensor:
    """Translate a point cloud given the input translation.

    Args:
        pcd: The input point cloud with shape (NUM_POINTS, D).
        translation: The translation offset with shape (3,).

    Returns:
        The translated point cloud.
    """
    x, y, z = translation[0], translation[1], translation[2]
    transform = pt3d.Translate(x=x, y=y, z=z, dtype=pcd.dtype, device=str(pcd.device))

    return _apply_pt3d_transform(pcd, transform, transform_normals=False)
