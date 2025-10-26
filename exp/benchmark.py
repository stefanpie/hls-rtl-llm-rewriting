import os
from pathlib import Path

from hls_rtl_llm_rewriting.core import (
    attempt_rewrite__oneshot,
    attempt_rewrite__variables,
    build_model_openrouter,
)

if __name__ == "__main__":
    DIR_CURRENT = Path(__file__).parent

    DIR_DESIGNS = DIR_CURRENT.parent / "test_designs"

    design_dirs = DIR_DESIGNS.glob("*")

    for design_dir in design_dirs:
        for module_fp in design_dir.glob("*.v"):
            top_module = module_fp.stem

            input_verilog = module_fp.read_text()

            test_file_fp = module_fp
            top_module = module_fp.stem

            input_verilog = test_file_fp.read_text()

            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                raise ValueError("OPENROUTER_API_KEY environment variable not set")
            if api_key.strip() == "":
                raise ValueError("OPENROUTER_API_KEY environment variable is empty")

            MODEL_ID = "openai/gpt-oss-120b"
            llm = build_model_openrouter(MODEL_ID, api_key)

            N = 2
            N_JOBS = 2

            attempt_rewrite__oneshot(
                input_verilog=input_verilog,
                work_dir=DIR_CURRENT / "work" / top_module,
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
