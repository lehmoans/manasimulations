# AutoFluent

AutoFluent is a config-driven framework for automating ANSYS Fluent workflows.

## Configuration architecture

AutoFluent separates **what to run** from **where and how to run it**.

```text
case.yaml
    -> simulation/case parameters

environment.yaml
    -> local / m3 / mock execution environments
```

The GUI edits case configuration. It can save reusable configurations without overwriting the current `case.yaml`.

```text
saved_case_configurations/
    pump_baseline.yaml
    pump_fsi.yaml
    mesh_refinement.yaml
```

A saved configuration can be selected directly for a headless HPC run.

## GUI

Open the case configuration editor:

```powershell
autofluent gui
```

The GUI supports:

- creating a new case configuration
- loading the current `config/case.yaml`
- loading a saved case configuration
- saving the current case
- saving a new named case configuration
- keeping saved configurations separate from `case.yaml`

Saved configurations are stored in:

```text
saved_case_configurations/
```

## Running cases

Run the current case on the local environment:

```powershell
autofluent run --case config/case.yaml --environment local
```

Run a saved configuration:

```powershell
autofluent run --case pump_fsi --environment m3
```

The saved-case name resolves to:

```text
saved_case_configurations/pump_fsi.yaml
```

List available saved configurations:

```powershell
autofluent saved-cases
```

The same case YAML can therefore be created locally with the GUI and then copied to an HPC system without modifying the HPC machine's working `case.yaml`.

## Environment configuration

All execution environments live in one file:

```text
config/environment.yaml
```

The current environments are:

- `local`
- `m3`
- `mock`

Local and M3 environments first attempt to detect the Fluent installation through PyFluent. If detection fails, specify the installation root explicitly in `environment.yaml`:

```yaml
type:
  local:
    fluent:
      root: "C:/Program Files/ANSYS Inc/v252"

  m3:
    fluent:
      root: "/apps/ansys_inc/v252"
```

PyFluent's launcher supports an explicit `fluent_path`, while its normal installation discovery uses Ansys installation environment variables. AutoFluent uses the explicit root only as the configured fallback.

## Execution lifecycle

`AutoFluent` owns orchestration. There is no separate simulation-profile layer.

```text
AutoFluent
  -> environment check
  -> working-directory preparation
  -> session launch
  -> meshing (if enabled)
  -> solution (if enabled)
  -> post-process
  -> save result
  -> close environment
```

The environment supplies the execution context. The case configuration supplies the simulation instructions.

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
