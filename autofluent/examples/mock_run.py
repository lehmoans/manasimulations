from pathlib import Path
import tempfile

from autofluent import AutoFluent


def main():
    with tempfile.TemporaryDirectory(prefix="autofluent_mock_") as run_dir:
        config = {
            "environment": {"type": "mock"},
            "save_dir": {"path": run_dir},
            "meshing": {
                "enabled": True,
                "file": "mock_mesh.msh",
            },
            "solver": {
                "enabled": True,
                "run_calc_settings": {"iter_count": 5},
                "post_process": {
                    "iso_surface": [{"name": "x0"}],
                    "contour": [{"name": "velocity-mag"}],
                },
                "save": {"name": "mock_result.json"},
            },
        }

        result = AutoFluent(config).run()

        print("\nMOCK RUN RESULT")
        print(result)
        print(f"Mesh exists: {Path(run_dir, 'mock_mesh.msh').exists()}")
        print(f"Result exists: {Path(result['output']).exists()}")


if __name__ == "__main__":
    main()
