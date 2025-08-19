import pandas as pd

def compute_ground_truth(mutation_path, clinical_path, output_path):
    """
    Ground truth for query:
    "Which top two histological types of BRCA (with vital_status = Alive) 
    in the PanCancer Atlas exhibit the highest percentage of CDH1 gene mutations?"

    Steps:
    1. Load mutation and clinical data
    2. Filter BRCA patients in clinical data with valid histology type AND vital_status = Alive
    3. Filter mutation data for BRCA, gene = CDH1, FILTER = PASS
    4. Merge on ParticipantBarcode
    5. For each histology type: compute mutation percentage
    6. Take top 2 histology types by mutation percentage
    """

    # 1. Load CSVs
    mutation = pd.read_csv(mutation_path)
    clinical = pd.read_csv(clinical_path)

    # 2. Filter clinical (BRCA only, valid histology type, Alive only)
    clinical_filtered = clinical[
        (clinical["acronym"] == "BRCA") &
        (clinical["histological_type"].notna()) &
        (clinical["vital_status"] == "Alive")
    ].copy()

    clinical_filtered = clinical_filtered[["bcr_patient_barcode", "histological_type"]]

    # 3. Filter mutation (BRCA + CDH1 + FILTER=PASS)
    mutation_filtered = mutation[
        (mutation["Study"] == "BRCA") &
        (mutation["Hugo_Symbol"] == "CDH1") &
        (mutation["FILTER"] == "PASS")
    ].copy()

    mutation_filtered = mutation_filtered[["ParticipantBarcode", "Hugo_Symbol"]].drop_duplicates()

    # 4. Merge clinical & mutation
    merged = pd.merge(
        clinical_filtered,
        mutation_filtered,
        left_on="bcr_patient_barcode",
        right_on="ParticipantBarcode",
        how="left",
        indicator=True
    )

    # Create mutation flag
    merged["mutation_flag"] = merged["_merge"].apply(lambda x: 1 if x == "both" else 0)

    # 5. Group by histology type
    grouped = merged.groupby("histological_type").agg(
        mutation_count=("mutation_flag", "sum"),
        total=("mutation_flag", "count")
    ).reset_index()

    grouped["mutation_percentage"] = grouped["mutation_count"] / grouped["total"]

    # 6. Select top 2
    result = grouped.sort_values("mutation_percentage", ascending=False).head(3)


    # 7. Save result
    result.rename(columns={"histological_type": "Histological_Type"}, inplace=True)
    result.to_csv(output_path, index=False)

    return result


if __name__ == "__main__":
    mutation_path = "../ground_truth_dataset/Mutation_Data.csv"
    clinical_path = "../ground_truth_dataset/Clinical_Info_gt.csv"
    output_path = "ground_truth.csv"

    result = compute_ground_truth(mutation_path, clinical_path, output_path)

    print("✅ Ground truth saved to:", output_path)
    print(result)
