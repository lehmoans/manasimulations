# Further Work

## AutoFluent Long-Term Vision

AutoFluent should evolve from a PyFluent wrapper into a reusable **simulation execution and experiment framework**.

The core principle is:

> Build around the lifecycle of a computational experiment, not around individual Fluent API operations.

The framework should eventually support defining, executing, reproducing, validating, restarting, analysing, and repeating simulations across different environments and potentially across large parameter studies.

---

## 1. Core Architecture

The long-term conceptual structure is:

```text
                         AutoFluent
                              │
             ┌────────────────┴────────────────┐
             │                                 │
        CASE DEFINITION                  EXECUTION ENVIRONMENT
             │                                 │
        case.yaml                         environment.yaml
             │                                 │
             └──────────────┬──────────────────┘
                            │
                       Simulation
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
     Geometry            Meshing             Solution
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                       Postprocess
                            │
                         Results
                            │
                       Validation
                            │
                     Data / Artifacts
                            │
                    ┌───────┴───────┐
                    │               │
                 Local             HPC
                    │               │
                  M3              SLURM
```

The existing architectural direction should remain focused on:

```text
Simulation
│
├── Environment
│   ├── Local
│   ├── M3
│   └── Mock
│
├── Meshing
├── Solution
└── Postprocess
```

`Simulation` should remain the orchestration layer rather than introducing another abstraction such as a `Profile` layer.

---

# 2. Simulation Lifecycle

The eventual simulation lifecycle should support:

```text
CREATE
  ↓
VALIDATE
  ↓
PREPARE
  ↓
MESH
  ↓
SOLVE
  ↓
POSTPROCESS
  ↓
VALIDATE RESULTS
  ↓
ARCHIVE
```

The API could eventually expose:

```python
simulation.validate()
simulation.prepare()
simulation.mesh()
simulation.solve()
simulation.postprocess()
simulation.validate_results()
simulation.archive()
```

while:

```python
simulation.run()
```

orchestrates the complete workflow.

This allows individual lifecycle stages to be executed independently and provides the foundation for restartability and partial workflows.

---

# 3. Configuration Architecture

Maintain a strong separation between the simulation definition and execution environment.

## `case.yaml`

Defines the simulation:

```yaml
geometry:
meshing:
boundary_conditions:
materials:
solver:
initialization:
reports:
monitors:
postprocess:
```

## `environment.yaml`

Defines where and how the simulation executes:

```yaml
environment:
  type: mock

  ansys:
    root: ...

  resources:
    cores: ...
    memory: ...

  execution:
    ...
```

The same case should eventually be runnable in multiple environments:

```text
case.yaml
   │
   ├── mock
   ├── local
   └── m3
```

The GUI, CLI, and Python API should all ultimately operate through the same underlying configuration and simulation system rather than creating separate configuration mechanisms.

---

# 4. Mock Environment

The mock environment is important as an architectural and integration-testing boundary.

The mock session should resemble the interface actually required from Fluent/PyFluent:

```python
session = environment.launch_session()

meshing = Meshing(session, config)
solution = Solution(session, config)
postprocess = Postprocess(session, config)
```

The higher-level AutoFluent code should not need to know whether it is interacting with:

```text
MockSession
```

or:

```text
FluentSession
```

The immediate v1.0 objective is therefore:

> A configuration-driven simulation can execute from `case.yaml` + `environment.yaml` through meshing → solution → postprocessing using the mock environment.

This should become the main end-to-end acceptance test.

---

# 5. Restart and Checkpointing

Eventually AutoFluent should support restarting simulations rather than assuming every run starts from zero.

A run directory could eventually contain:

```text
simulation/
    input/
    mesh/
    solution/
    results/
    logs/
    checkpoints/
```

A future API could support:

```python
simulation.resume()
```

AutoFluent could determine which stages already completed:

```text
mesh exists       ✓
solution exists   ✓
checkpoint exists ✓

→ resume from checkpoint
```

The architecture should therefore avoid assuming that every `run()` begins from a completely clean state.

---

# 6. Run Management

AutoFluent should eventually distinguish between an individual simulation run and a larger experiment.

Conceptually:

```text
Experiment
    │
    ├── Run 001
    ├── Run 002
    ├── Run 003
    └── Run 004
```

This provides the foundation for:

- parameter sweeps
- design studies
- sensitivity analysis
- uncertainty studies
- optimisation
- automated CFD research

Runs should eventually have unique identifiers and associated metadata.

---

# 7. Parameterisation

AutoFluent should eventually support generating multiple simulations from parameter definitions rather than requiring manually duplicated YAML files.

Example:

```yaml
parameters:
  inlet_velocity:
    values: [1, 2, 3, 4, 5]

  turbulence_model:
    values:
      - k_epsilon
      - k_omega
```

AutoFluent could then generate:

```text
Run 001
Run 002
Run 003
...
```

This should be built above the individual `Simulation` abstraction rather than embedded into the core simulation components.

---

# 8. Dependency and Workflow Management

AutoFluent should eventually understand dependencies between stages.

For example:

```text
Geometry
   ↓
Mesh
   ↓
Solution
   ↓
Postprocess
```

If geometry changes:

```text
geometry changed
      ↓
mesh invalid
      ↓
solution invalid
      ↓
results invalid
```

If only postprocessing changes:

```text
postprocessing changed
      ↓
mesh still valid
solution still valid
```

A mature AutoFluent system should eventually determine:

> What actually needs to be rerun?

rather than blindly rerunning the complete simulation.

This is essentially a future workflow/DAG capability.

---

# 9. Results Management

Results should eventually become first-class objects rather than simply files scattered through a run directory.

Potential structure:

```text
Results
├── scalar results
├── field results
├── convergence
├── monitors
├── reports
└── metadata
```

A future API could expose results such as:

```python
result = simulation.run()

result.drag_coefficient
result.pressure_drop
result.mass_flow
result.convergence
```

This will be particularly useful for automated experiments and parameter studies.

---

# 10. Validation

Validation should be separated into at least two categories.

## Configuration Validation

Before execution:

```text
✓ geometry exists
✓ boundary names exist
✓ environment exists
✓ Fluent installation exists
✓ requested cores valid
✓ requested memory valid
```

## Simulation/Result Validation

After execution:

```text
✓ converged
✓ mass imbalance acceptable
✓ residual criteria satisfied
✓ expected reports produced
✓ no NaNs
✓ no negative cell volumes
```

A run should eventually be able to report something such as:

```text
Simulation completed

Status: FAILED VALIDATION

Reason:
Mass imbalance = 3.7%
Required < 0.1%
```

Successful process execution should not automatically mean that the engineering result is valid.

---

# 11. Logging and Provenance

For research and reproducibility, AutoFluent should eventually record the provenance of every run.

Useful metadata includes:

```text
case
geometry
mesh
solver settings
AutoFluent version
Fluent version
environment
machine
CPU/resources
execution time
parameters
```

A future run could contain something such as:

```text
run_metadata.yaml
```

This allows results to be reproduced and traced months or years later.

---

# 12. Execution Environment Abstraction

The environment abstraction should represent **where and how a computational job executes**, rather than being tied specifically to M3.

Conceptually:

```text
Execution
   │
   ├── Local
   ├── Mock
   ├── SLURM
   └── Future environments
```

M3 should be treated as one specific SLURM environment.

This could eventually allow AutoFluent to support:

```text
local workstation
M3
AWS
other university clusters
other SLURM systems
cloud workstations
```

without redesigning the simulation layer.

---

# 13. Resource Management

Eventually resources should be defined independently from the simulation itself:

```yaml
resources:
  cores: 16
  memory: 64GB
  walltime: 24h
```

The environment can then translate these requirements into its execution mechanism.

For example:

```text
Local
→ Fluent -t16

SLURM
→ --cpus-per-task=16
→ --mem=64G
→ --time=24:00:00
```

The case should not need to know how different execution environments represent these resources.

---

# 14. Error Handling and Recovery

A mature framework should eventually distinguish between error categories such as:

```text
ConfigurationError
EnvironmentError
MeshingError
SolverError
ConvergenceError
PostprocessError
ResourceError
```

A future failure workflow could be:

```text
Fluent crashes
     ↓
AutoFluent detects failure
     ↓
collect logs
     ↓
identify failure category
     ↓
save state
     ↓
report useful error
```

This should make AutoFluent more useful than simply reporting that Fluent exited unsuccessfully.

---

# 15. Job Scheduler Integration

Eventually AutoFluent should support job submission as a separate concern from simulation definition.

For example:

```text
case
  ↓
Simulation
  ↓
Environment
  ↓
Execution backend
  ↓
Local / SLURM / other scheduler
```

This provides the foundation for:

- local execution
- batch execution
- queue submission
- resource allocation
- job monitoring
- job cancellation
- job status tracking

The scheduler layer should not leak into case-specific simulation logic.

---

# 16. Experiment Layer

Eventually the individual `Simulation` should become the primitive underneath a larger `Experiment` abstraction.

Conceptually:

```text
Experiment
    │
    ├── Simulation 001
    ├── Simulation 002
    ├── Simulation 003
    ├── Simulation 004
    └── ...
```

The experiment layer can eventually manage:

```text
parameter generation
       ↓
AutoFluent simulations
       ↓
result collection
       ↓
result analysis
       ↓
optimisation/design exploration
```

This provides a natural path from single CFD cases to automated research workflows.

---

# 17. CLI

A command-line interface should eventually provide a convenient interface to the same core API.

Potential commands:

```bash
autofluent run case.yaml --environment m3
autofluent check case.yaml --environment local
autofluent mesh case.yaml --environment m3
autofluent resume RUN-042
```

The CLI should not contain separate simulation logic. It should call the same AutoFluent core used by Python and the GUI.

---

# 18. GUI

A GUI can eventually provide a user-friendly front end.

Potential interface:

```text
┌──────────────────────────────┐
│         AutoFluent           │
├──────────────────────────────┤
│ Case:       [case.yaml   ▼]  │
│ Environment:[Mock        ▼]  │
│                              │
│ Geometry                     │
│   File:       [geom.scdC]    │
│                              │
│ Meshing                      │
│   Enabled:    [✓]            │
│                              │
│ Solver                       │
│   Cores:      [4]            │
│                              │
│        [ Check ] [ Run ]     │
└──────────────────────────────┘
```

The GUI should be a **front end**, not the owner of simulation logic.

The architecture should remain:

```text
                  AutoFluent Core
                        │
          ┌─────────────┼─────────────┐
          │             │             │
        Python         CLI           GUI
          │             │             │
          └─────────────┴─────────────┘
                        │
                   Simulation
```

---

# 19. Plugin and Solver Extensibility

This is a long-term consideration rather than an immediate implementation target.

Avoid unnecessary assumptions that AutoFluent must forever be tightly coupled to one solver.

A possible future architecture could support:

```text
AutoSimulation
    │
    ├── Fluent
    ├── Mechanical
    ├── OpenFOAM
    └── other solvers
```

This should **not** be implemented prematurely. The priority remains building a good Fluent-focused framework.

However, interfaces should avoid unnecessary hardcoding when a clean abstraction costs little.

---

# 20. Maturity Roadmap

## Level 1 — Current Foundation

```text
Configuration
Environment
Session
Simulation
Meshing
Solution
Postprocess
Mock
Local
M3
```

Primary goal:

> Complete and validate the end-to-end mock simulation.

---

## Level 2 — Framework Maturity

```text
Validation
Logging
Results
Run management
Checkpoint/restart
CLI
```

Primary goal:

> Make individual simulations reliable, inspectable, reproducible, and restartable.

---

## Level 3 — Automation

```text
Experiments
Parameter sweeps
Batch execution
SLURM
Result aggregation
```

Primary goal:

> Run and analyse many simulations systematically.

---

## Level 4 — Advanced AutoFluent

```text
Optimisation
Design exploration
Automatic recovery
Workflow DAGs
GUI
Plugin architecture
AI-assisted workflow generation
```

Primary goal:

> Turn AutoFluent into a general computational engineering automation platform.

---

# 21. What Should Be Designed Now vs Later

The most important distinction is between **architectural requirements** and **features that can be implemented later**.

## Design for now

The current architecture should leave room for:

- simulation lifecycle stages
- separate case/environment configuration
- multiple environments
- mock vs real sessions
- independent execution stages
- run directories
- persistent artifacts
- logging
- validation
- restart/checkpointing
- unique run identifiers
- resource abstraction
- scheduler abstraction
- future experiment management
- CLI/GUI front ends
- future extensibility

## Implement later

These do not need to distract from the current v1.0 work:

- optimisation
- parameter sweeps
- advanced experiment management
- automatic recovery
- sophisticated dependency/DAG systems
- GUI
- plugin architecture
- AI-assisted workflows
- support for other CFD/FEA solvers

---

# 22. Immediate Objective: AutoFluent v1.0

The immediate target should remain deliberately narrow.

AutoFluent v1.0 should demonstrate:

```text
case.yaml
    +
environment.yaml
        ↓
Simulation
        ↓
Environment
        ↓
Session
        ↓
Meshing
        ↓
Solution
        ↓
Postprocess
        ↓
Results
```

using the mock environment.

The key acceptance criterion is:

> A complete configuration-driven simulation can execute end-to-end without Fluent installed.

Once this is reliable, the project can be tagged as the first stable architectural milestone.

After that, the individual Fluent-facing functions/classes can be refined and expanded without repeatedly redesigning the overall project structure.

---

# 23. Overall Design Principle

The long-term direction can be summarized as:

```text
                    AutoFluent
                        │
              ┌─────────┴─────────┐
              │                   │
        Simulation            Experiment
              │                   │
      ┌───────┼───────┐           │
      │       │       │           │
   Meshing Solution Postprocess   Runs
      │       │       │           │
      └───────┼───────┘           │
              │                   │
           Results ───────────────┘
              │
         Validation
              │
       Reproducibility
              │
       Automation/Optimisation
```

The central idea is:

> **AutoFluent should eventually automate the lifecycle of computational engineering experiments, with Fluent being the first execution engine rather than the definition of the entire architecture.**

The current project structure is therefore the foundation. The immediate task is not to implement every future capability, but to ensure the foundation can grow into these capabilities without requiring another architectural rewrite.
