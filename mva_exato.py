
from itertools import product


def exact_mva_fig63(D, N, Z=None, center_types=None, class_names=None, device_names=None):

    R = len(N)          # número de classes
    K = len(D[0])       # número de dispositivos

    if Z is None:
        Z = [0.0] * R

    if center_types is None:
        center_types = ["queueing"] * K

    if class_names is None:
        class_names = [f"Classe {r + 1}" for r in range(R)]

    if device_names is None:
        device_names = [f"D{i + 1}" for i in range(K)]

    # Validações simples
    if len(D) != R:
        raise ValueError("A matriz D deve ter uma linha para cada classe em N.")

    for row in D:
        if len(row) != K:
            raise ValueError("Todas as linhas de D devem ter o mesmo número de dispositivos.")

    if len(Z) != R:
        raise ValueError("Z deve ter um valor para cada classe.")

    if len(center_types) != K:
        raise ValueError("center_types deve ter um valor para cada dispositivo.")

    states = {}

    # Equivale aos loops:
    # for j1 := 0 to N1
    #   for j2 := 0 to N2
    #       ...
    #           for jR := 0 to NR
    ranges = [range(n + 1) for n in N]

    for state in product(*ranges):
        # state = (j1, j2, ..., jR)

        R_ir = [[0.0 for _ in range(K)] for _ in range(R)]
        X_r = [0.0 for _ in range(R)]
        n_ir = [[0.0 for _ in range(K)] for _ in range(R)]
        n_i_total = [0.0 for _ in range(K)]

        # Caso base: n_i(0) = 0
        if sum(state) == 0:
            states[state] = {
                "state": state,
                "R_ir": R_ir,
                "R_total": [0.0 for _ in range(R)],
                "X_r": X_r,
                "n_ir": n_ir,
                "n_i_total": n_i_total,
            }
            continue

        # Para r := 1 to R
        for r in range(R):
            j_r = state[r]

            # If j_r > 0
            if j_r > 0:
                # Calcula N - 1_r
                previous_state = list(state)
                previous_state[r] -= 1
                previous_state = tuple(previous_state)

                # n_i(N - 1_r)
                previous_n_i_total = states[previous_state]["n_i_total"]

                # For i := 1 to K
                for i in range(K):
                    if center_types[i] == "delay":
                        R_ir[r][i] = D[r][i]
                    else:
                        R_ir[r][i] = D[r][i] * (1.0 + previous_n_i_total[i])
            else:
                # Else R_i,r(N) = 0
                for i in range(K):
                    R_ir[r][i] = 0.0

            # X_0,r(N) = j_r / (Z_r + sum_i R_i,r(N))
            R_total_r = sum(R_ir[r])

            if j_r > 0:
                denominator = Z[r] + R_total_r
                X_r[r] = j_r / denominator if denominator > 0 else 0.0
            else:
                X_r[r] = 0.0

            # n_i,r(N) = X_0,r(N) * R_i,r(N)
            for i in range(K):
                n_ir[r][i] = X_r[r] * R_ir[r][i]

        # For i := 1 to K:
        # n_i(N) = sum_r X_0,r(N) * R_i,r(N)
        for i in range(K):
            n_i_total[i] = sum(n_ir[r][i] for r in range(R))

        states[state] = {
            "state": state,
            "R_ir": R_ir,
            "R_total": [sum(R_ir[r]) for r in range(R)],
            "X_r": X_r,
            "n_ir": n_ir,
            "n_i_total": n_i_total,
        }

    return {
        "D": D,
        "N": tuple(N),
        "Z": Z,
        "center_types": center_types,
        "class_names": class_names,
        "device_names": device_names,
        "states": states,
        "final": states[tuple(N)],
    }


def print_final_result(result):
    """Imprime apenas o estado final."""
    final = result["final"]
    class_names = result["class_names"]
    device_names = result["device_names"]

    print(f"Estado final N = {result['N']}")
    print()

    header = ["Classe"] + [f"R_{d}" for d in device_names] + ["R_total", "X"] + [f"n_{d}" for d in device_names]
    print(" | ".join(header))
    print("-" * (len(" | ".join(header))))

    for r, cname in enumerate(class_names):
        row = [cname]
        row += [f"{final['R_ir'][r][i]:.3f}" for i in range(len(device_names))]
        row += [f"{final['R_total'][r]:.3f}", f"{final['X_r'][r]:.3f}"]
        row += [f"{final['n_ir'][r][i]:.3f}" for i in range(len(device_names))]
        print(" | ".join(row))

    print()
    print("n_i total por dispositivo:")
    for i, dname in enumerate(device_names):
        print(f"{dname}: {final['n_i_total'][i]:.3f}")


def print_all_states(result):
    """Imprime todos os estados calculados."""
    states = result["states"]
    class_names = result["class_names"]
    device_names = result["device_names"]

    for state, data in states.items():
        print("=" * 80)
        print(f"Estado {state}")
        print("-" * 80)

        for r, cname in enumerate(class_names):
            if state[r] == 0:
                continue

            print(f"Classe {cname}")
            for i, dname in enumerate(device_names):
                print(f"  R_{dname} = {data['R_ir'][r][i]:.6f} | n_{dname},{cname} = {data['n_ir'][r][i]:.6f}")

            print(f"  R_total = {data['R_total'][r]:.6f}")
            print(f"  X = {data['X_r'][r]:.6f}")
            print()

        print("n_i total:")
        for i, dname in enumerate(device_names):
            print(f"  {dname}: {data['n_i_total'][i]:.6f}")
        print()


def run_case(title, D, N, Z=None, center_types=None, class_names=None, device_names=None, show_all_states=False):
    """
    Função geral para testar qualquer exercício.

    Basta trocar:
    - title
    - D
    - N
    - Z, se tiver tempo de pensamento
    - center_types, se tiver centro delay
    """

    print("\n" + "#" * 80)
    print(title)
    print("#" * 80)

    result = exact_mva_fig63(
        D=D,
        N=N,
        Z=Z,
        center_types=center_types,
        class_names=class_names,
        device_names=device_names,
    )

    print_final_result(result)

    if show_all_states:
        print()
        print("TABELA COM TODOS OS ESTADOS")
        print_all_states(result)

    return result


if __name__ == "__main__":
    # ============================================================
    # Teste 1: exemplo original da Seção 6.2 / Tabela 6.3
    # Ordem das classes: Update, Query
    # Ordem dos dispositivos: CPU, D1, D2
    # ============================================================

    class_names = ["Update", "Query"]
    device_names = ["CPU", "D1", "D2"]

    D_original = [
        [0.375, 0.480, 0.240],  # Update
        [0.105, 0.180, 0.000],  # Query
    ]

    N_original = [1, 3]

    run_case(
        title="Teste 1 - Modelo original da Secao 6.2, N=(1,3)",
        D=D_original,
        N=N_original,
        class_names=class_names,
        device_names=device_names,
        show_all_states=True,
    )

    # ============================================================
    # Teste 2: exemplo do capítulo - mover I/O da Query de D1 para D2
    # Resultado esperado aproximado do livro:
    # X_Query = 4.335, X_Update = 0.517
    # R_Query = 0.692, R_Update = 1.934
    # ============================================================

    D_query_para_D2 = [
        [0.375, 0.480, 0.240],  # Update
        [0.105, 0.000, 0.180],  # Query
    ]

    run_case(
        title="Teste 2 - Query move I/O de D1 para D2",
        D=D_query_para_D2,
        N=N_original,
        class_names=class_names,
        device_names=device_names,
        show_all_states=False,
    )

    # ============================================================
    # Teste 3: exercício - balancear I/O da Query entre D1 e D2
    # D_Query = (0.105, 0.090, 0.090)
    # ============================================================

    D_query_balanceada = [
        [0.375, 0.480, 0.240],  # Update
        [0.105, 0.090, 0.090],  # Query
    ]

    run_case(
        title="Teste 3 - Query balanceada entre D1 e D2",
        D=D_query_balanceada,
        N=N_original,
        class_names=class_names,
        device_names=device_names,
        show_all_states=False,
    )

    # ============================================================
    # Teste 4: exercício - triplicar multiprogramação da classe Update
    # N = (3,3)
    # ============================================================

    N_update_triplicado = [3, 3]

    run_case(
        title="Teste 4 - Update triplicado, N=(3,3)",
        D=D_original,
        N=N_update_triplicado,
        class_names=class_names,
        device_names=device_names,
        show_all_states=False,
    )