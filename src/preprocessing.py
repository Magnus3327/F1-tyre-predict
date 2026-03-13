import pandas as pd

def clean_data(laps_data):

    print("🧹 Inizio preprocessing")

    # ---------------------------
    # GREEN FLAG FILTER
    # ---------------------------

    laps = laps_data[
        laps_data['TrackStatus'].astype(str).str.contains('1')
    ].copy()

    # rimozione pit
    laps = laps[
        laps['PitInTime'].isna() &
        laps['PitOutTime'].isna()
    ].copy()

    # lap time in secondi
    laps.loc[:, 'LapTime_Sec'] = laps['LapTime'].dt.total_seconds()

    # --------------------------------
    # WARMUP TYRE
    # --------------------------------

    laps = laps[laps['TyreLife'] > 2]

    # --------------------------------
    # OUTLIER FILTER PER STINT
    # --------------------------------

    filtered = []

    for stint in sorted(laps['Stint'].unique()):

        stint_df = laps[laps['Stint'] == stint].copy()

        if len(stint_df) < 3:
            continue

        fastest = stint_df['LapTime_Sec'].min()

        threshold = fastest * 1.04

        stint_df = stint_df[
            stint_df['LapTime_Sec'] <= threshold
        ]

        filtered.append(stint_df)

    if not filtered:
        return pd.DataFrame()

    df = pd.concat(filtered)

    # --------------------------------
    # FEATURE ENGINEERING
    # --------------------------------

    df['TyreLife2'] = df['TyreLife'] ** 2

    features = [
        'Stint',
        'Compound',
        'TyreLife',
        'TyreLife2',
        'TrackTemp',
        'Fuel_Est',
        'LapNumber',
        'LapTime_Sec'
    ]

    df = df[features].dropna()

    print(f"✅ Giri utilizzabili: {len(df)}")

    return df