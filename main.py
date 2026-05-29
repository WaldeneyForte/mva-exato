from mva_aproximado import approximate_mva_closed
from mva_exato import exact_mva
from mva_mixed_multiclass import mixed_multiclass_model

from output_utils import (
    print_final_result,
    print_iteration_table,
    print_all_states,
)


def main():
    print("\n" + "=" * 100)
    print("EXERCÍCIO 1")
    print("=" * 100)

    class_names = ["Update", "Query"]
    device_names = ["CPU", "D1", "D2"]

    D_original = [
        [0.375, 0.480, 0.240],
        [0.105, 0.180, 0.000],
    ]

    N_original = [1, 3]

    print("\n1(a) Modelo original N=(1,3), MVA aproximado, epsilon=0.001")

    ex1_original_aprox = approximate_mva_closed(
        D=D_original,
        N=N_original,
        epsilon=0.001,
        class_names=class_names,
        device_names=device_names,
        tolerance_mode="relative",
    )

    print_final_result(ex1_original_aprox)
    print_iteration_table(ex1_original_aprox)

    N_triplicado = [3, 3]

    print("\n1(b) Update triplicado N=(3,3), MVA exato")

    ex1_triplicado_exato = exact_mva(
        D=D_original,
        N=N_triplicado,
        class_names=class_names,
        device_names=device_names,
    )

    print_final_result(ex1_triplicado_exato)
    print_all_states(ex1_triplicado_exato)

    print("\n1(b) Update triplicado N=(3,3), MVA aproximado, epsilon=0.001")

    ex1_triplicado_aprox = approximate_mva_closed(
        D=D_original,
        N=N_triplicado,
        epsilon=0.001,
        class_names=class_names,
        device_names=device_names,
        tolerance_mode="relative",
    )

    print_final_result(ex1_triplicado_aprox)
    print_iteration_table(ex1_triplicado_aprox)

    print("\nComparação: MVA exato vs MVA aproximado")
    print("Classe | R_exato | R_aprox | X_exato | X_aprox")

    for r, cname in enumerate(class_names):
        print(
            f"{cname} | "
            f"{ex1_triplicado_exato['final']['R_total'][r]:.6f} | "
            f"{ex1_triplicado_aprox['final']['R_total'][r]:.6f} | "
            f"{ex1_triplicado_exato['final']['X_r'][r]:.6f} | "
            f"{ex1_triplicado_aprox['final']['X_r'][r]:.6f}"
        )

    R = len(N_triplicado)
    K = len(device_names)

    effort_exact = R * K * (1 + N_triplicado[0]) * (1 + N_triplicado[1])
    effort_approx = ex1_triplicado_aprox["final"]["iteration"] * R * K

    print("\nEsforço computacional")
    print(f"MVA exato: {effort_exact}")
    print(f"MVA aproximado: {effort_approx}")

    print("\n" + "=" * 100)
    print("EXERCÍCIO 2")
    print("=" * 100)

    N_ex2 = [1, 3]

    D_atual = [
        [0.375, 0.480, 0.240],
        [0.105, 0.180, 0.000],
    ]

    D_balanceado = [
        [0.375, 0.480, 0.240],
        [0.105, 0.090, 0.090],
    ]

    print("\n2(a) Situação atual, Query usa apenas D1")

    ex2_atual = exact_mva(
        D=D_atual,
        N=N_ex2,
        class_names=class_names,
        device_names=device_names,
    )

    print_final_result(ex2_atual)
    print_all_states(ex2_atual)

    print("\n2(b) Situação modificada, Query balanceada entre D1 e D2")

    ex2_balanceado = exact_mva(
        D=D_balanceado,
        N=N_ex2,
        class_names=class_names,
        device_names=device_names,
    )

    print_final_result(ex2_balanceado)
    print_all_states(ex2_balanceado)

    print("\nComparação do exercício 2")
    print("Classe | R_atual | R_balanceado | X_atual | X_balanceado")

    for r, cname in enumerate(class_names):
        print(
            f"{cname} | "
            f"{ex2_atual['final']['R_total'][r]:.6f} | "
            f"{ex2_balanceado['final']['R_total'][r]:.6f} | "
            f"{ex2_atual['final']['X_r'][r]:.6f} | "
            f"{ex2_balanceado['final']['X_r'][r]:.6f}"
        )

    print("\n" + "=" * 100)
    print("EXERCÍCIO 3")
    print("=" * 100)

    open_class_names = ["Q", "U"]
    closed_class_names = ["I"]
    device_names_ex3 = ["CPU", "D1", "D2"]

    lambda_q_original = 3.0
    lambda_u = 1.5
    lambda_q_95 = lambda_q_original * 1.95

    N_closed = [50]
    Z_closed = [15.0]

    ex3_a = mixed_multiclass_model(
        D_open=[
            [0.060, 0.030, 0.060],
            [0.100, 0.030, 0.090],
        ],
        lambdas_open=[lambda_q_original, lambda_u],
        D_closed=[
            [0.090, 0.045, 0.000],
        ],
        N_closed=N_closed,
        Z_closed=Z_closed,
        open_class_names=open_class_names,
        closed_class_names=closed_class_names,
        device_names=device_names_ex3,
    )

    ex3_b = mixed_multiclass_model(
        D_open=[
            [0.060, 0.030, 0.060],
            [0.100, 0.030, 0.090],
        ],
        lambdas_open=[lambda_q_95, lambda_u],
        D_closed=[
            [0.090, 0.045, 0.000],
        ],
        N_closed=N_closed,
        Z_closed=Z_closed,
        open_class_names=open_class_names,
        closed_class_names=closed_class_names,
        device_names=device_names_ex3,
    )

    ex3_c_d1 = mixed_multiclass_model(
        D_open=[
            [0.060, 0.015, 0.060],
            [0.100, 0.015, 0.090],
        ],
        lambdas_open=[lambda_q_95, lambda_u],
        D_closed=[
            [0.090, 0.0225, 0.000],
        ],
        N_closed=N_closed,
        Z_closed=Z_closed,
        open_class_names=open_class_names,
        closed_class_names=closed_class_names,
        device_names=device_names_ex3,
    )

    ex3_c_cpu = mixed_multiclass_model(
        D_open=[
            [0.030, 0.030, 0.060],
            [0.050, 0.030, 0.090],
        ],
        lambdas_open=[lambda_q_95, lambda_u],
        D_closed=[
            [0.045, 0.045, 0.000],
        ],
        N_closed=N_closed,
        Z_closed=Z_closed,
        open_class_names=open_class_names,
        closed_class_names=closed_class_names,
        device_names=device_names_ex3,
    )

    print("\nResultados dos itens 3(a), 3(b) e 3(c)")
    print("Cenário | R_Q | R_U | R_I | X_Q | X_U | X_I")

    scenarios = [
        ("3(a) Original", ex3_a),
        ("3(b) lambda_Q +95%", ex3_b),
        ("3(c) D1 2x", ex3_c_d1),
        ("3(c) CPU 2x", ex3_c_cpu),
    ]

    for name, result in scenarios:
        if not result["stable"]:
            print(f"{name} | instável")
            continue

        R_Q = result["open"]["R_total"][0]
        R_U = result["open"]["R_total"][1]
        R_I = result["closed"]["final"]["R_total"][0]

        X_Q = result["open"]["X_r"][0]
        X_U = result["open"]["X_r"][1]
        X_I = result["closed"]["final"]["X_r"][0]

        print(
            f"{name} | "
            f"{R_Q:.6f} | "
            f"{R_U:.6f} | "
            f"{R_I:.6f} | "
            f"{X_Q:.6f} | "
            f"{X_U:.6f} | "
            f"{X_I:.6f}"
        )

    print("\n3(d) Variação do número de terminais de 50 até 250")
    print("M | R_I | X_I")

    for M in range(50, 251):
        result = mixed_multiclass_model(
            D_open=[
                [0.030, 0.030, 0.060],
                [0.050, 0.030, 0.090],
            ],
            lambdas_open=[lambda_q_95, lambda_u],
            D_closed=[
                [0.045, 0.045, 0.000],
            ],
            N_closed=[M],
            Z_closed=Z_closed,
            open_class_names=open_class_names,
            closed_class_names=closed_class_names,
            device_names=device_names_ex3,
        )

        if result["stable"]:
            R_I = result["closed"]["final"]["R_total"][0]
            X_I = result["closed"]["final"]["X_r"][0]

            if M % 25 == 0:
                print(f"{M} | {R_I:.6f} | {X_I:.6f}")

    print("\nBusca do número máximo de terminais com R_I < 1.5s")

    max_supported = None
    M = 50

    while True:
        result = mixed_multiclass_model(
            D_open=[
                [0.030, 0.030, 0.060],
                [0.050, 0.030, 0.090],
            ],
            lambdas_open=[lambda_q_95, lambda_u],
            D_closed=[
                [0.045, 0.045, 0.000],
            ],
            N_closed=[M],
            Z_closed=Z_closed,
            open_class_names=open_class_names,
            closed_class_names=closed_class_names,
            device_names=device_names_ex3,
        )

        if not result["stable"]:
            print("Sistema ficou instável.")
            break

        R_I = result["closed"]["final"]["R_total"][0]

        if R_I < 1.5:
            max_supported = M
            M += 1
        else:
            print(f"Primeiro M com R_I >= 1.5s: {M}")
            print(f"R_I nesse ponto: {R_I:.6f}")
            break

    print(f"Máximo número de terminais com R_I < 1.5s: {max_supported}")


if __name__ == "__main__":
    main()