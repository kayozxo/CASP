from optimum.exporters.openvino import main_export

main_export(
    model_name_or_path="sentence-transformers/all-MiniLM-L6-v2",
    output="openvino_models/miniLM_openvino",
    task="feature-extraction"
)
