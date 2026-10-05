"""Install the target-averaged sequence-residual aggregation for figure III-09."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np


def install(module) -> None:
    original = module.figures_iii

    def recovered(rows):
        try:
            original(rows)
            return
        except ValueError as error:
            if "could not broadcast input array from shape (3,3) into shape (3,)" not in str(error):
                raise
            plt.close("all")

        d, a = module._load("phenomenon_III_sequences.h5")
        seq = a["sequence_names"]
        obs = a["observable_names"]
        oi = {name: index for index, name in enumerate(obs)}
        data = str(module.ROOT / "10_RAW_DATA" / "phenomenon_III_sequences.h5")

        def matrix_for(name):
            residual = np.zeros((3, 3))
            for target in range(3):
                final = d["values"][target, :, -1, oi[name]]
                residual += abs(final[:, None] - final[None, :])
            return residual / 3.0

        def matrix_panel(name):
            def panel(ax):
                image = ax.imshow(matrix_for(name), cmap=module.WARM_CMAP)
                ax.set(xticks=range(3), yticks=range(3), xticklabels=seq, yticklabels=seq, title=name)
                plt.colorbar(image, ax=ax, fraction=0.05, pad=0.02)
            return panel

        rows.append(module._make(
            "III-09", "III", "Sequence-to-sequence residual matrices",
            [matrix_panel("bandwidth"), matrix_panel("moment2_scaled"), matrix_panel("green_abs"), matrix_panel("return_t0p2")],
            observable="target-averaged pairwise route differences at final level",
            cover="local exact approximants",
            resolution="level six residuals averaged over three generic targets",
            conclusion="sequence agreement is strong for bandwidth and moments but weaker for pointwise Green and return observables.",
            data_path=data,
        ))

        depth_names = ["moment2/bound2", "moment4/bound4", "|G00|", "return(0.2)"]
        labels = a["target_labels"]
        callbacks = []
        for index, name in enumerate(depth_names):
            def make(idx, label):
                def panel(ax):
                    for target, target_label in enumerate(labels):
                        module._line(ax, 2 * d["depth_sizes_per_layer"], d["depth_values"][:, target, idx], target, target_label, marker="o", ms=3)
                    ax.set(xlabel="bilayer dimension", ylabel=label)
                    ax.set_xscale("log")
                    module._legend(ax)
                return panel
            callbacks.append(make(index, name))
        rows.append(module._make(
            "III-10", "III", "Spatial-depth convergence of direct generic observables", callbacks,
            observable="moments, Green function, return probability",
            cover="generic local Dirichlet only",
            resolution="depths 1,2,3 = dimensions 18,130,914",
            conclusion="coarse/medium/fine local data quantify boundary sensitivity separately from arithmetic sequence effects.",
            data_path=data,
        ))

    module.figures_iii = recovered

