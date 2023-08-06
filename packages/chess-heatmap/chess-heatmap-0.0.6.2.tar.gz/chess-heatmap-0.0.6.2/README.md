Implement a project based on Chess using dask and coiled<br />

Develop a control heatmap which will show which side controls which squares how many times per ply/move. <br />
Input will be PGNs (Portable Game Notation) and produce heat maps per game per ply. Publish the (num_white_control, num_black_control) tuple for each square for each ply.
Apply parallelism to multiple games in a single PGN and to multiple PGNs
