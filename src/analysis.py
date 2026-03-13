import pandas as pd


def collect_result(results, year, gp, driver, stint, compound, deg_rate, r2):
    """
        Salva i risultati di ogni stint in un dataframe.
    """

    results.append({
        "Year": year,
        "GP": gp,
        "Driver": driver,
        "Stint": stint,
        "Compound": compound,
        "Degradation": deg_rate,
        "R2": r2
    })

    return results


def results_to_dataframe(results):

    return pd.DataFrame(results)