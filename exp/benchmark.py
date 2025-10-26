import os
from pathlib import Path

from hls_rtl_llm_rewriting.core import (
    attempt_rewrite__variables,
    attempt_rewrite__zeroshot,
    build_model_openrouter,
)

DIR_CURRENT = Path(__file__).parent
DIR_DESIGNS = DIR_CURRENT.parent / "test_designs"

if __name__ == "__main__":
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable not set")
    if api_key.strip() == "":
        raise ValueError("OPENROUTER_API_KEY environment variable is empty")

    model_id = "openai/gpt-oss-120b"
    llm = build_model_openrouter(model_id, api_key)

    design_dirs = DIR_DESIGNS.glob("*")

    for design_dir in design_dirs:
        # TODO: figure out how we want to benchmark each module in a single design
        # ex. just the top
        # ex. ignore any low level operators or memory modules
        # ex. auto extract module heirarchy and benchmark each module individually

        # for now just do top level module, we know for our test designs this is kernel_<design_name> in the file kernel_<design_name>.v
        # so we hardcode that here for our inital benchmark

        top_module = "kernel_" + design_dir.stem
        test_file_fp = design_dir / f"{top_module}.v"
        input_verilog = test_file_fp.read_text()

        N = 10
        N_JOBS = 6

        attempt_rewrite__zeroshot(
            input_verilog=input_verilog,
            work_dir=DIR_CURRENT / "work" / (top_module + "__zeroshot"),
            top_module=top_module,
            design_dir=design_dir,
            llm=llm,
            n=N,
            n_jobs=N_JOBS,
        )

        attempt_rewrite__variables(
            input_verilog=input_verilog,
            work_dir=DIR_CURRENT / "work" / (top_module + "__variables"),
            top_module=top_module,
            design_dir=design_dir,
            llm=llm,
            n=N,
            n_jobs=N_JOBS,
        )
