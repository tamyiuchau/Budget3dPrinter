import meshlabxml as mlx
def p2stl(file_in = "input.asc", file_out = 'out.stl')
	proj = mlx.FilterScript(file_in = file_in, file_out = file_out, ml_version='2016.12')
	mlx.normals.point_sets(proj,neighbors=32,smooth_iteration=10)
	mlx.remesh.surface_poisson_screened(proj)
	mlx.layers.delete(proj)
	proj.run_script()
