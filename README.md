# Solecki-et-al-2025a

This repository contains code and data relating to Solecki et al. 2026a*. These functions require a temperature array (ERA5 daily mean temperature data in our case) and will define, process, and cluster this temperature data.

Cold air outbreak date information is stored in the `data` directory.

The matrix used for the K-means algorithm is also stored in the `data` directory, and the analysis and construction of related matricies can be found in `K_means_prep.ipynb`.

The rest of the analysis in Solecki et al. 2026a can be replicated using this information and ERA5 reanalysis data.

Please email zachsolecki@gmail.com with any questions