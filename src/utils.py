

# def sample_bilinear(a, coords):
#     coords0 = coords.astype(int)
#     coords0 = np.clip(coords0, 0, np.asarray(a.shape) - 2)
#     coords1 = coords0 + 1
#     weights0 = coords - coords0
#     weights1 = 1.0 - weights0
#     values00 = a[coords0[:, 0], coords0[:, 1]]
#     values01 = a[coords0[:, 0], coords1[:, 1]]
#     values10 = a[coords1[:, 0], coords0[:, 1]]
#     values11 = a[coords1[:, 0], coords1[:, 1]]
#     values = sum((
#         values00 * weights0[:, 0] * weights0[:, 1],
#         values01 * weights0[:, 0] * weights1[:, 1],
#         values10 * weights1[:, 0] * weights0[:, 1],
#         values11 * weights1[:, 0] * weights1[:, 1],
#     ))
#     return values