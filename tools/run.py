from datetime import datetime as dt
from pathlib import Path

import click
from loguru import logger

from llm_engineering import settings
from pipelines import (
    digital_data_etl,
    end_to_end_data,
    evaluating,
    export_artifact_to_json,
    feature_engineering,
    generate_datasets,
    training,
)


@click.command(
    help="""
LLM Engineering project CLI v0.0.1 — Customized for Aziz Sancar Digital Twin.

Main entry point for the pipeline execution.
This entrypoint is where all ZenML pipelines come together.

Examples:

  \b
  # Run the pipeline with default options
  python run.py

  \b
  # Run the ETL pipeline using Aziz Sancar configuration
  python run.py --run-etl --etl-config-filename end_to_end_aziz_sancar.yaml

  \b
  # Run full feature engineering
  python run.py --run-feature-engineering

"""
)
@click.option(
    "--no-cache",
    is_flag=True,
    default=False,
    help="Disable caching for the pipeline run.",
)
@click.option(
    "--run-end-to-end-data",
    is_flag=True,
    default=False,
    help="Whether to run all the data pipelines in one go.",
)
@click.option(
    "--run-etl",
    is_flag=True,
    default=False,
    help="Whether to run the ETL pipeline.",
)
@click.option(
    "--run-export-artifact-to-json",
    is_flag=True,
    default=False,
    help="Whether to run the Artifact -> JSON pipeline",
)
@click.option(
    "--etl-config-filename",
    default="end_to_end_aziz_sancar.yaml",
    help="Filename of the ETL config file.",
)
@click.option(
    "--run-feature-engineering",
    is_flag=True,
    default=False,
    help="Whether to run the feature engineering pipeline.",
)
@click.option(
    "--run-generate-instruct-datasets",
    is_flag=True,
    default=False,
    help="Whether to run the instruction dataset generation pipeline.",
)
@click.option(
    "--run-generate-preference-datasets",
    is_flag=True,
    default=False,
    help="Whether to run the preference dataset generation pipeline.",
)
@click.option(
    "--run-training",
    is_flag=True,
    default=False,
    help="Whether to run the training pipeline.",
)
@click.option(
    "--run-evaluation",
    is_flag=True,
    default=False,
    help="Whether to run the evaluation pipeline.",
)
@click.option(
    "--run-rag",
    is_flag=True,
    default=False,
    help="Whether to run the RAG (Retrieval-Augmented Generation) pipeline.",
)

@click.option(
    "--export-settings",
    is_flag=True,
    default=False,
    help="Whether to export your settings to ZenML or not.",
)
@click.option("--mock", is_flag=True, help="Use mock mode (FakeListLLM instead of OpenAI).")

def main(
        no_cache: bool = False,
        run_end_to_end_data: bool = False,
        run_etl: bool = False,
        etl_config_filename: str = "end_to_end_aziz_sancar.yaml",
        run_export_artifact_to_json: bool = False,
        run_feature_engineering: bool = False,
        run_generate_instruct_datasets: bool = False,
        run_generate_preference_datasets: bool = False,
        run_training: bool = False,
        run_evaluation: bool = False,
        run_rag: bool = False,
        export_settings: bool = False,
        mock: bool = False,
) -> None:
    """
    Main CLI entry point for running different pipelines.
    """

    # Ensure at least one pipeline flag is provided
    assert (
            run_end_to_end_data
            or run_etl
            or run_export_artifact_to_json
            or run_feature_engineering
            or run_generate_instruct_datasets
            or run_generate_preference_datasets
            or run_training
            or run_evaluation
            or run_rag
            or export_settings
    ), "Please specify at least one action to run."

    if export_settings:
        logger.info("Exporting settings to ZenML secrets.")
        settings.export()

    pipeline_args = {
        "enable_cache": not no_cache,
    }
    root_dir = Path(__file__).resolve().parent.parent

    # ✅ End-to-end pipeline
    if run_end_to_end_data:
        run_args_end_to_end = {}
        pipeline_args["config_path"] = root_dir / "configs" / "end_to_end_aziz_sancar.yaml"
        assert pipeline_args["config_path"].exists(), f"Config file not found: {pipeline_args['config_path']}"
        pipeline_args["run_name"] = f"end_to_end_aziz_sancar_run_{dt.now().strftime('%Y_%m_%d_%H_%M_%S')}"

        # ✅ YAML dosyasındaki linkleri oku ve author_links parametresine ata
        import yaml
        config_file = pipeline_args["config_path"]
        with open(config_file, "r", encoding="utf-8") as f:
            yaml_data = yaml.safe_load(f)
        run_args_end_to_end["author_links"] = yaml_data.get("links", [])

        # ✅ Pipeline'ı çalıştır
        run_args_end_to_end["mock"] = mock
        end_to_end_data.with_options(**pipeline_args)(**run_args_end_to_end)

    # ✅ ETL pipeline (data extraction & crawling)
    if run_etl:
        pipeline_args["config_path"] = root_dir / "configs" / etl_config_filename
        assert pipeline_args["config_path"].exists(), f"Config file not found: {pipeline_args['config_path']}"
        pipeline_args["run_name"] = f"aziz_sancar_etl_run_{dt.now().strftime('%Y_%m_%d_%H_%M_%S')}"

        import yaml
        with open(pipeline_args["config_path"], "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        run_args_etl = {
            "user_full_name": cfg.get("user_full_name"),
            "links": cfg.get("links")
        }

        digital_data_etl.with_options(**pipeline_args)(**run_args_etl)

    # ✅ Export JSON
    if run_export_artifact_to_json:
        run_args_etl = {}
        pipeline_args["config_path"] = root_dir / "configs" / "export_artifact_to_json.yaml"
        pipeline_args["run_name"] = f"export_json_run_{dt.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        export_artifact_to_json.with_options(**pipeline_args)(**run_args_etl)

    # ✅ Feature engineering
    if run_feature_engineering:
        run_args_fe = {}
        pipeline_args["config_path"] = root_dir / "configs" / "feature_engineering.yaml"
        pipeline_args["run_name"] = f"feature_engineering_run_{dt.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        feature_engineering.with_options(**pipeline_args)(**run_args_fe)

    # ✅ Instruction dataset generation
    if run_generate_instruct_datasets:
        run_args_cd = {}
        pipeline_args["config_path"] = root_dir / "configs" / "generate_instruct_datasets.yaml"
        pipeline_args["run_name"] = f"instruct_datasets_run_{dt.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        generate_datasets.with_options(**pipeline_args)(**run_args_cd)

    # ✅ Preference dataset generation (DPO / RLHF)
    if run_generate_preference_datasets:
        run_args_cd = {}
        pipeline_args["config_path"] = root_dir / "configs" / "generate_preference_datasets.yaml"
        pipeline_args["run_name"] = f"preference_datasets_run_{dt.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        generate_datasets.with_options(**pipeline_args)(**run_args_cd)

    # ✅ Model training
    if run_training:
        run_args_cd = {}
        pipeline_args["config_path"] = root_dir / "configs" / "training.yaml"
        pipeline_args["run_name"] = f"training_run_{dt.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        training.with_options(**pipeline_args)(**run_args_cd)

    # ✅ Evaluation pipeline
    if run_evaluation:
        run_args_cd = {}
        pipeline_args["config_path"] = root_dir / "configs" / "evaluating.yaml"
        pipeline_args["run_name"] = f"evaluation_run_{dt.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        evaluating.with_options(**pipeline_args)(**run_args_cd)

    if run_rag:
        pipeline_args["config_path"] = root_dir / "configs" / "rag.yaml"
        pipeline_args["run_name"] = f"rag_run_{dt.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        from pipelines.rag import rag
        rag.with_options(**pipeline_args)()


if __name__ == "__main__":
    main()
