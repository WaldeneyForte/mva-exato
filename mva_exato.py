from itertools import product

def exact_mva(D, N, Z=None, center_types=None, class_names=None, device_names=None):

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


