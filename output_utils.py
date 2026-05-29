

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


def print_iteration_table(result):
     
    class_names = result["class_names"]
    device_names = result["device_names"]

    print("\nTabela de iterações")
    print("-" * 100)

    header = ["it", "dif_max"]

    for cname in class_names:
        header.append(f"X_{cname}")
        header.append(f"R_{cname}")

    for cname in class_names:
        for dname in device_names:
            header.append(f"n_{dname}_{cname}")

    print(" | ".join(header))
    print("-" * len(" | ".join(header)))

    for data in result["iterations"]:
        row = [
            str(data["iteration"]),
            f"{data['max_difference']:.6f}",
        ]

        for r in range(len(class_names)):
            row.append(f"{data['X_r'][r]:.6f}")
            row.append(f"{data['R_total'][r]:.6f}")

        for r in range(len(class_names)):
            for i in range(len(device_names)):
                row.append(f"{data['n_ir'][r][i]:.6f}")

        print(" | ".join(row))


   