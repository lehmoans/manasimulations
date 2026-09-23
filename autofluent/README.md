# AutoFluent

AutoFluent is a config-driven framework for automating ANSYS Fluent workflows.

## Current execution lifecycle

The simulation is orchestrated by `AutoFluent`. The case configuration determines which stages are enabled and how each component is configured. The environment determines where and how the simulation is executed.

```text
AutoFluent
  -> environment check
  -> working-directory preparation
  -> session launch
  -> meshing (if enabled)
       -> initialise workflow
       -> load geometry
       -> mesh setup
       -> generate mesh
       -> check mesh
       -> save mesh
  -> solution (if enabled)
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

There is no separate simulation-profile layer. `AutoFluent` owns the orchestration, while the meshing, solver, and post-processing implementations provide the operations. Configuration controls the case-specific behavior.

## Mock execution

The mock environment does not require ANSYS Fluent.

Install the package:

```powershell
cd autofluent
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
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

The mock example uses an in-memory configuration so the execution architecture can be validated independently. The YAML configuration will be expanded as additional Fluent operations are added.

## Environments

AutoFluent currently has environment implementations for:

- `mock`
- `local`
- `m3`

The mock environment is the current integration target. Local Fluent and M3 execution will be brought onto the same lifecycle as their Fluent-specific components are completed.
