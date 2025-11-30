import os
import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

from pymoo.problems import get_problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.termination import get_termination
from pymoo.indicators.hv import HV
from pymoo.indicators.gd import GD
from pymoo.indicators.igd import IGD
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting

# real-coded operators
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM


# ================== CONFIG ==================
SEEDS = [12345, 67890, 11111, 22222, 33333,
         44444, 55555, 66666, 77777, 88888]

POP_SIZE = 600
N_GENERATIONS = 4000
N_VAR = 30
N_OBJ = 3

OUTPUT_DIR = "DTLZ6"
PLOT_DIR = os.path.join(OUTPUT_DIR, "plots")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PLOT_DIR, exist_ok=True)


def apply_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)


def get_true_front(problem):
    # Older pymoo-compatible pareto front
    return problem.pareto_front()


def make_nsga2():
    """NSGA-II with explicit real-coded operators."""
    crossover = SBX(prob=0.9, eta=20.0)
    mutation = PM(eta=20.0)  # prob defaults to 1 / n_var inside pymoo
    sampling = FloatRandomSampling()

    algo = NSGA2(
        pop_size=POP_SIZE,
        sampling=sampling,
        crossover=crossover,
        mutation=mutation,
        eliminate_duplicates=True
    )
    return algo


def run_single_nsga2(seed, problem, pf, ref_point):
    apply_seed(seed)

    algorithm = make_nsga2()
    termination = get_termination("n_gen", N_GENERATIONS)

    res = minimize(
        problem,
        algorithm,
        termination,
        seed=seed,
        verbose=False
    )

    F = res.F  # (N, 3)
    nd_idx = NonDominatedSorting().do(F, only_non_dominated_front=True)
    F_nd = F[nd_idx]

    hv = HV(ref_point=ref_point)(F_nd)
    gd = GD(pf)(F_nd)
    igd = IGD(pf)(F_nd)

    return F_nd, hv, gd, igd, F_nd.shape[0]


def plot_front_3d(run_id, F_nd, pf, hv, gd, igd, out_dir):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # True DTLZ6 front (red)
    ax.scatter(
        pf[:, 0], pf[:, 1], pf[:, 2],
        s=8, alpha=0.5,
        color='red', label='True DTLZ6 front'
    )

    # NSGA-II front (blue)
    ax.scatter(
        F_nd[:, 0], F_nd[:, 1], F_nd[:, 2],
        s=10, alpha=0.9,
        color='blue', label='NSGA-II front'
    )

    ax.set_xlabel("f1")
    ax.set_ylabel("f2")
    ax.set_zlabel("f3")

    ax.set_title(
        f"DTLZ6 (30 vars, 3 objs) – Run {run_id}\n"
        f"HV={hv:.4f}, GD={gd:.4f}, IGD={igd:.4f}"
    )

    ax.legend()
    ax.grid(True)

    out_path = os.path.join(out_dir, f"dtlz6_run_{run_id:02d}.png")
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def main():
    print("Running DTLZ6 with 30 variables and 3 objectives (NSGA-II)")

    problem = get_problem("dtlz6", n_var=N_VAR, n_obj=N_OBJ)
    pf = get_true_front(problem)

    # Ref point slightly above PF for HV
    ref_point = np.max(pf, axis=0) + 0.1

    csv_path = os.path.join(OUTPUT_DIR, "nsga2_dtlz6_30var_summary.csv")
    with open(csv_path, "w") as f:
        f.write("run_id,seed,HV,GD,IGD,ND_size\n")

        for run_id, seed in enumerate(SEEDS, start=1):
            print(f"=== Run {run_id} – Seed {seed} ===")
            F_nd, hv, gd, igd, nd_size = run_single_nsga2(seed, problem, pf, ref_point)

            print(f"HV      = {hv:.6f}")
            print(f"GD      = {gd:.6f}")
            print(f"IGD     = {igd:.6f}")
            print(f"ND size = {nd_size}\n")

            plot_front_3d(run_id, F_nd, pf, hv, gd, igd, PLOT_DIR)

            f.write(f"{run_id},{seed},{hv:.10f},{gd:.10f},{igd:.10f},{nd_size}\n")

    print("\nDone.")
    print("CSV saved to:", csv_path)
    print("Plots saved to:", PLOT_DIR)


if __name__ == "__main__":
    main()
