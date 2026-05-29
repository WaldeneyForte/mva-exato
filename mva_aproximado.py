def approximate_mva_closed(
    D,
    N,
    epsilon=0.001,
    Z=None,
    center_types=None,
    class_names=None,
    device_names=None,
    tolerance_mode="relative",
    max_iterations=10000,
):
    

    R = len(N)       # número de classes
    K = len(D[0])    # número de dispositivos

    if Z is None:
        Z = [0.0] * R

    if center_types is None:
        center_types = ["queueing"] * K

    if class_names is None:
        class_names = [f"Classe {r + 1}" for r in range(R)]

    if device_names is None:
        device_names = [f"D{i + 1}" for i in range(K)]

    if len(D) != R:
        raise ValueError("A matriz D deve ter uma linha para cada classe em N.")

    for row in D:
        if len(row) != K:
            raise ValueError("Todas as linhas de D devem ter o mesmo número de dispositivos.")

    if len(Z) != R:
        raise ValueError("Z deve ter um valor para cada classe.")

    if len(center_types) != K:
        raise ValueError("center_types deve ter um valor para cada dispositivo.")

    if tolerance_mode not in {"relative", "absolute"}:
        raise ValueError('tolerance_mode deve ser "relative" ou "absolute".')

    n_est = [[0.0 for _ in range(K)] for _ in range(R)]

    for r in range(R):
        K_r = sum(1 for i in range(K) if D[r][i] > 0)

        for i in range(K):
            if D[r][i] > 0 and K_r > 0:
                n_est[r][i] = N[r] / K_r
            else:
                n_est[r][i] = 0.0

    history = []

    converged = False

    for iteration in range(1, max_iterations + 1):
        # n antigo recebe a estimativa anterior
        n_old = [row[:] for row in n_est]

        
        seen_by_arrival = [[0.0 for _ in range(K)] for _ in range(R)]

        for r in range(R):
            for i in range(K):
                total_seen = 0.0

                for t in range(R):
                    if t == r:
                        if N[r] > 0:
                            total_seen += ((N[r] - 1) / N[r]) * n_old[t][i]
                    else:
                        total_seen += n_old[t][i]

                seen_by_arrival[r][i] = total_seen

        # Calcula R_i,r(N), X_0,r(N), e a nova estimativa n^e_i,r(N)
        R_ir = [[0.0 for _ in range(K)] for _ in range(R)]
        R_total = [0.0 for _ in range(R)]
        X_r = [0.0 for _ in range(R)]
        n_new = [[0.0 for _ in range(K)] for _ in range(R)]

        for r in range(R):
            for i in range(K):
                if center_types[i] == "delay":
                    R_ir[r][i] = D[r][i]
                else:
                    R_ir[r][i] = D[r][i] * (1.0 + seen_by_arrival[r][i])

            R_total[r] = sum(R_ir[r])

            denominator = Z[r] + R_total[r]
            if N[r] > 0 and denominator > 0:
                X_r[r] = N[r] / denominator
            else:
                X_r[r] = 0.0

            for i in range(K):
                n_new[r][i] = X_r[r] * R_ir[r][i]

        # Calcula a diferença
        max_difference = 0.0

        for r in range(R):
            for i in range(K):
                if tolerance_mode == "relative":
                    denominator = abs(n_new[r][i])
                    if denominator > 0:
                        difference = abs(n_new[r][i] - n_old[r][i]) / denominator
                    else:
                        difference = abs(n_new[r][i] - n_old[r][i])
                else:
                    difference = abs(n_new[r][i] - n_old[r][i])

                if difference > max_difference:
                    max_difference = difference

        n_i_total = [sum(n_new[r][i] for r in range(R)) for i in range(K)]

        iteration_data = {
            "iteration": iteration,
            "max_difference": max_difference,
            "R_ir": R_ir,
            "R_total": R_total,
            "X_r": X_r,
            "n_ir": n_new,
            "n_i_total": n_i_total,
            "seen_by_arrival": seen_by_arrival,
        }

        history.append(iteration_data)

        n_est = n_new

        if max_difference < epsilon:
            converged = True
            break

    return {
        "D": D,
        "N": tuple(N),
        "Z": Z,
        "epsilon": epsilon,
        "tolerance_mode": tolerance_mode,
        "center_types": center_types,
        "class_names": class_names,
        "device_names": device_names,
        "iterations": history,
        "final": history[-1],
        "converged": converged,
    }
