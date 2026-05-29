from mva_exato import exact_mva


def mixed_multiclass_model(
    D_open,
    lambdas_open,
    D_closed,
    N_closed,
    Z_closed=None,
    open_class_names=None,
    closed_class_names=None,
    device_names=None,
):

    O = len(lambdas_open)      # número de classes abertas
    C = len(N_closed)          # número de classes fechadas
    K = len(D_open[0])         # número de dispositivos

    if Z_closed is None:
        Z_closed = [0.0] * C

    if open_class_names is None:
        open_class_names = [f"Open_{r + 1}" for r in range(O)]

    if closed_class_names is None:
        closed_class_names = [f"Closed_{c + 1}" for c in range(C)]

    if device_names is None:
        device_names = [f"D{i + 1}" for i in range(K)]


    if len(D_open) != O:
        raise ValueError("D_open deve ter uma linha para cada classe aberta.")

    if len(D_closed) != C:
        raise ValueError("D_closed deve ter uma linha para cada classe fechada.")

    for row in D_open:
        if len(row) != K:
            raise ValueError("Todas as linhas de D_open devem ter o mesmo número de dispositivos.")

    for row in D_closed:
        if len(row) != K:
            raise ValueError("Todas as linhas de D_closed devem ter o mesmo número de dispositivos.")


    U_open_ir = [[0.0 for _ in range(K)] for _ in range(O)]

    for r in range(O):
        for i in range(K):
            U_open_ir[r][i] = lambdas_open[r] * D_open[r][i]


    U_open_i = [0.0 for _ in range(K)]

    for i in range(K):
        U_open_i[i] = sum(U_open_ir[r][i] for r in range(O))


    stable = True
    unstable_devices = []

    for i in range(K):
        if U_open_i[i] >= 1.0:
            stable = False
            unstable_devices.append(
                {
                    "device": device_names[i],
                    "utilization": U_open_i[i],
                }
            )

    if not stable:
        return {
            "model_type": "mixed_multiclass",
            "stable": False,
            "unstable_devices": unstable_devices,
            "U_open_ir": U_open_ir,
            "U_open_i": U_open_i,
        }

    D_closed_stretched = [[0.0 for _ in range(K)] for _ in range(C)]

    for c in range(C):
        for i in range(K):
            D_closed_stretched[c][i] = D_closed[c][i] / (1.0 - U_open_i[i])


    closed_result = exact_mva(
        D=D_closed_stretched,
        N=N_closed,
        Z=Z_closed,
        class_names=closed_class_names,
        device_names=device_names,
    )


    n_closed_i = closed_result["final"]["n_i_total"]


    R_open_ir = [[0.0 for _ in range(K)] for _ in range(O)]

    for r in range(O):
        for i in range(K):
            R_open_ir[r][i] = (
                D_open[r][i]
                * (1.0 + n_closed_i[i])
                / (1.0 - U_open_i[i])
            )


    R_open_total = [0.0 for _ in range(O)]

    for r in range(O):
        R_open_total[r] = sum(R_open_ir[r])

  
    n_open_ir = [[0.0 for _ in range(K)] for _ in range(O)]

    for r in range(O):
        for i in range(K):
            n_open_ir[r][i] = lambdas_open[r] * R_open_ir[r][i]

    n_open_i = [0.0 for _ in range(K)]

    for i in range(K):
        n_open_i[i] = sum(n_open_ir[r][i] for r in range(O))

   
    return {
        "model_type": "mixed_multiclass",
        "stable": True,

        "open_class_names": open_class_names,
        "closed_class_names": closed_class_names,
        "device_names": device_names,

        "D_open": D_open,
        "lambdas_open": lambdas_open,

        "D_closed_original": D_closed,
        "D_closed_stretched": D_closed_stretched,
        "N_closed": N_closed,
        "Z_closed": Z_closed,

        "U_open_ir": U_open_ir,
        "U_open_i": U_open_i,

        "open": {
            "R_ir": R_open_ir,
            "R_total": R_open_total,
            "X_r": lambdas_open,
            "n_ir": n_open_ir,
            "n_i_total": n_open_i,
        },

        "closed": closed_result,
    }