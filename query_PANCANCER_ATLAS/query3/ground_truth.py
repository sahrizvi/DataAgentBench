import pandas as pd
import numpy as np

def compute_chi_square(mutation_path, clinical_path, output_path):
    """
    Ground truth for query:
    Chi-square test between histological types and CDH1 mutations in BRCA.
    - Only BRCA patients
    - Exclude missing histology
    - Only FEMALE patients
    - Only FILTER=PASS mutations
    - Exclude histology/mutation categories with marginal total <= 10
    """

    # 1. Load data
    mutation = pd.read_csv(mutation_path)
    clinical = pd.read_csv(clinical_path)

    # 2. Filter clinical (BRCA + non-null histology + FEMALE only)
    clinical_filtered = clinical[
        (clinical["acronym"] == "BRCA") &
        (clinical["histological_type"].notna()) &
        (clinical["gender"] == "FEMALE")
    ][["bcr_patient_barcode", "histological_type"]].copy()

    # 3. Filter mutation (BRCA + CDH1 + FILTER=PASS)
    mutation_filtered = mutation[
        (mutation["Study"] == "BRCA") &
        (mutation["Hugo_Symbol"] == "CDH1") &
        (mutation["FILTER"] == "PASS")
    ][["ParticipantBarcode"]].drop_duplicates()

    # 4. Merge clinical with mutation
    merged = clinical_filtered.merge(
        mutation_filtered,
        left_on="bcr_patient_barcode",
        right_on="ParticipantBarcode",
        how="left"
    )
    merged["mutation_status"] = np.where(
        merged["ParticipantBarcode"].notna(), "YES", "NO"
    )

    # 5. Build contingency table (counts Nij)
    contingency = merged.groupby(
        ["histological_type", "mutation_status"]
    ).size().reset_index(name="Nij")

    # 6. Apply marginal total filtering (>10)
    row_totals = contingency.groupby("histological_type")["Nij"].sum()
    col_totals = contingency.groupby("mutation_status")["Nij"].sum()

    valid_rows = row_totals[row_totals > 10].index
    valid_cols = col_totals[col_totals > 10].index

    contingency = contingency[
        contingency["histological_type"].isin(valid_rows) &
        contingency["mutation_status"].isin(valid_cols)
    ]

    # 7. Recompute with full cross join (fill missing Nij=0)
    all_rows = contingency["histological_type"].unique()
    all_cols = contingency["mutation_status"].unique()
    full_index = pd.MultiIndex.from_product([all_rows, all_cols],
                                            names=["histological_type", "mutation_status"])
    contingency = contingency.set_index(
        ["histological_type", "mutation_status"]
    ).reindex(full_index, fill_value=0).reset_index()

    # 8. Compute expected counts
    grand_total = contingency["Nij"].sum()
    contingency["row_total"] = contingency.groupby("histological_type")["Nij"].transform("sum")
    contingency["col_total"] = contingency.groupby("mutation_status")["Nij"].transform("sum")
    contingency["Eij"] = contingency["row_total"] * contingency["col_total"] / grand_total

    # 9. Compute chi-square statistic
    contingency["chi2_contrib"] = (contingency["Nij"] - contingency["Eij"])**2 / contingency["Eij"]
    chi2 = contingency["chi2_contrib"].sum()

    # 10. Save result
    result = pd.DataFrame([{"Chi2": chi2}])
    result.to_csv(output_path, index=False)

    return chi2, contingency


if __name__ == "__main__":
    mutation_path = "../ground_truth_dataset/Mutation_Data.csv"
    clinical_path = "../ground_truth_dataset/Clinical_Info_gt.csv"
    output_path = "ground_truth.csv"

    chi2, contingency = compute_chi_square(mutation_path, clinical_path, output_path)
    print("✅ Ground truth saved to:", output_path)
    print("Chi-square value:", chi2)
    print(contingency.head())
