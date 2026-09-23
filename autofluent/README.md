# AutoFluent

AutoFluent is a config-driven framework for automating ANSYS Fluent workflows.

## Current execution profile

The first supported simulation profile is **fixed**.

It intentionally follows one stable workflow before the framework is generalized:

```text
AutoFluent
  -> environment check
  -> working-directory preparation
  -> session launch
  -> meshing
       -> initialise workflow
       -> load geometry
       -> mesh setup
       -> generate mesh
       -> check mesh
       -> save mesh
  -> solution setup
       -> models
       -> materials
       -> zones
       -> reference values
       -> boundary conditions
       -> initialization
       -> solution controls
       -> solution methods
       -> monitors
       -> report definitions
  -> solve
  -> post-process
       -> iso-surfaces
       -> contours
  -> save result
  -> close environment
```

The fixed sequence is implemented by `FixedSimulationProfile`. The profile is deliberately separate from `AutoFluent` so additional simulation profiles can be introduced later.

## Mock execution

The mock environment does not require ANSYS Fluent.

Install the package:

```powershell
cd autofluent
py -3.10 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -e .
```

Run the end-to-end example:

```powershell
python examples/mock_run.py
```

Run the regression tests:

```powershell
python -m unittest discover tests -v
```

The mock workflow produces:

- `mock_mesh.msh`
- `mock_result.json`

The result JSON contains the solver result and execution workflow trace.

## Configuration status

The production `case.yaml` and `environment.yaml` architecture is intentionally not being redesigned in this stage.

The mock example uses an in-memory configuration so the execution architecture can be validated independently. The YAML configuration will be finalized after the fixed execution profile is stable.

## Environments

AutoFluent currently has environment implementations for:

- `mock`
- `local`
- `m3`

The mock environment is the current integration target. Local Fluent and M3 execution will be brought onto the same lifecycle after the mock profile is validated.
