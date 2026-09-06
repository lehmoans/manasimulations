# Mini-SLURM Simulation Management Platform

A local, modular simulation job-management platform inspired by HPC workload managers such as SLURM.

The purpose of this project is **not to recreate SLURM** or build a production HPC scheduler. The goal is to develop practical experience in:

* Python software architecture
* job scheduling
* queues
* worker processes
* process management
* concurrency
* resource management
* databases
* APIs
* logging and monitoring
* failure recovery
* simulation automation
* meshing workflows
* solver execution
* post-processing
* testing
* Docker
* distributed systems concepts
* eventual HPC/SLURM integration

The system will initially run entirely on a normal local computer using **mock simulations**. Expensive CFD simulations do not need to actually complete.

Eventually, the same architecture can be extended to real simulation software such as ANSYS Fluent and real HPC environments such as SLURM.

---

# 1. Project Goal

The final system should allow a user to submit a simulation job such as:

```text
Case:
    heart_pump_001

Parameters:
    flow_rate = 2.5 L/min
    frequency = 1.2 Hz
    mesh_size = 0.5 mm

Resources:
    CPUs = 4
    Memory = 8 GB
```

The system should then automatically:

```text
Submit Job
    ↓
Create Job
    ↓
Queue Job
    ↓
Schedule Job
    ↓
Allocate Resources
    ↓
Prepare Case
    ↓
Validate Inputs
    ↓
Generate Mesh
    ↓
Validate Mesh
    ↓
Setup Solver
    ↓
Run Solver
    ↓
Monitor Progress
    ↓
Detect Completion / Failure
    ↓
Post-process Results
    ↓
Validate Results
    ↓
Store Results
    ↓
Generate Report
```

Initially, every expensive operation can be simulated.

For example:

```text
Mock Meshing
    ↓
sleep(5)
    ↓
generate fake mesh statistics
```

and:

```text
Mock Solver
    ↓
simulate iterations
    ↓
generate fake residuals
    ↓
simulate convergence
```

This allows the entire software system to be developed and tested without needing HPC resources.

---

# 2. Important Architecture Decision

## One Repository, Multiple Subsystems

This is one complete project.

It should **not** initially be split into several repositories or microservices.

The recommended architecture is:

```text
mini-slurm/
│
├── scheduler/
├── workers/
├── simulation/
├── backends/
├── database/
├── api/
├── cli/
└── tests/
```

The components have different responsibilities, but they remain part of the same application.

This gives the project modularity without unnecessary complexity.

---

# 3. Core Design Principle

The most important architectural separation is:

```text
Scheduler ≠ Simulation
```

The scheduler should know about:

```text
Jobs
Queues
Priorities
Workers
Resources
States
Scheduling
```

It should **not** know that a particular job is an ANSYS Fluent simulation.

The simulation system should know about:

```text
Preparation
Meshing
Solver setup
Solver execution
Monitoring
Post-processing
Validation
```

This separation makes the system extensible.

For example:

```text
                    USER
                      │
                 CLI / API
                      │
                      ▼
                Job Manager
                      │
                      ▼
                  Scheduler
                      │
                  Job Queue
                      │
                      ▼
                   Worker
                      │
                      ▼
              Compute Backend
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
        Mock        Local       SLURM
          │
          ▼
    Simulation Pipeline
          │
    ┌─────┼─────┬─────────┐
    ▼     ▼     ▼         ▼
 Prepare Mesh Solver Postprocess
                       │
                       ▼
                   Validation
                       │
                       ▼
                    Results
```

---

# 4. Execution Backend Abstraction

The worker should not directly care how a job is executed.

Instead:

```text
Worker
   ↓
ComputeBackend
   ↓
┌─────────────┬─────────────┬─────────────┐
│             │             │
MockBackend  LocalBackend  SlurmBackend
```

Possible future backends:

```text
MockBackend
LocalBackend
DockerBackend
SlurmBackend
AWSBackend
```

This means the scheduler can remain unchanged while the execution environment changes.

For example:

```python
backend.run(job)
```

could eventually execute:

```text
Mock simulation
```

or:

```text
python simulation.py
```

or:

```text
docker run ...
```

or:

```text
sbatch simulation.sh
```

---

# 5. Simulation Pipeline

The simulation itself should be treated as a pipeline.

```text
SimulationPipeline
        │
        ├── Preparation
        │
        ├── Input Validation
        │
        ├── Meshing
        │
        ├── Mesh Validation
        │
        ├── Solver Setup
        │
        ├── Solver Execution
        │
        ├── Monitoring
        │
        ├── Post-processing
        │
        └── Result Validation
```

Each stage should have a clear interface.

For example:

```python
class Mesher:
    def generate(self, case):
        ...
```

Implementations can then be swapped:

```text
Mesher
   │
   ├── MockMesher
   └── FluentMesher
```

Similarly:

```text
Solver
   │
   ├── MockSolver
   └── FluentSolver
```

This means the system can be developed entirely with mock components first.

---

# 6. Project Structure

Recommended structure:

```text
mini-slurm/
│
├── README.md
├── pyproject.toml
├── requirements.txt
├── .gitignore
│
├── src/
│   └── minislurm/
│       │
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── logger.py
│       │
│       ├── jobs/
│       │   ├── __init__.py
│       │   ├── job.py
│       │   ├── state.py
│       │   ├── queue.py
│       │   └── scheduler.py
│       │
│       ├── workers/
│       │   ├── __init__.py
│       │   ├── worker.py
│       │   └── manager.py
│       │
│       ├── simulation/
│       │   ├── __init__.py
│       │   ├── pipeline.py
│       │   ├── preparation.py
│       │   ├── validation.py
│       │   ├── meshing.py
│       │   ├── solver.py
│       │   ├── monitoring.py
│       │   └── postprocess.py
│       │
│       ├── backends/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── mock.py
│       │   ├── local.py
│       │   └── slurm.py
│       │
│       ├── database/
│       │   ├── __init__.py
│       │   ├── database.py
│       │   ├── models.py
│       │   └── repositories.py
│       │
│       ├── api/
│       │   ├── __init__.py
│       │   └── server.py
│       │
│       └── solvers/
│           ├── __init__.py
│           └── mock_solver.py
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── configs/
│   ├── default.yaml
│   └── development.yaml
│
├── cases/
│   └── example_case/
│
├── data/
│   ├── inputs/
│   ├── meshes/
│   └── raw_results/
│
├── results/
│
├── logs/
│
├── scripts/
│
└── docker/
```

Do not implement all of this immediately.

Start small and expand the architecture as functionality is added.

---

# 7. Job Model

A job represents one computational task.

Example:

```python
Job(
    id="job_001",
    name="heart_pump_test",
    status="PENDING",
    priority=10,
    cpu=4,
    memory_gb=8,
)
```

A job should eventually contain:

```text
ID
Name
Description
Status
Priority
Created time
Started time
Finished time

Input parameters
Resource requirements
Working directory
Case directory

Current stage
Current iteration
Progress
Exit code

Retry count
Maximum retries

Worker ID
Backend

Result location
Log location
Error information
```

---

# 8. Job State Machine

Jobs should have explicit states.

Recommended initial states:

```text
CREATED
   ↓
PENDING
   ↓
PREPARING
   ↓
MESHING
   ↓
MESH_VALIDATION
   ↓
SETUP
   ↓
RUNNING
   ↓
POST_PROCESSING
   ↓
VALIDATING
   ↓
COMPLETED
```

Failure states:

```text
FAILED
CANCELLED
TIMEOUT
```

A job should never arbitrarily change state.

For example:

```text
PENDING → RUNNING
```

should happen through the scheduler/worker system.

Invalid transitions should be rejected.

---

# 9. Job Submission

The CLI should eventually support commands such as:

```bash
minislurm submit case.yaml
```

```bash
minislurm status
```

```bash
minislurm status job_001
```

```bash
minislurm cancel job_001
```

```bash
minislurm logs job_001
```

```bash
minislurm queue
```

```bash
minislurm workers
```

Eventually:

```bash
minislurm results job_001
```

and:

```bash
minislurm retry job_001
```

---

# 10. Job Preparation

Before simulation execution, create an isolated working directory.

Example:

```text
runs/
└── job_001/
    ├── input/
    ├── mesh/
    ├── solver/
    ├── output/
    ├── logs/
    └── metadata.json
```

The preparation stage should:

1. Create the working directory.
2. Copy required input files.
3. Store parameters.
4. Generate configuration files.
5. Record software/version information.
6. Create stage-specific directories.
7. Validate required files.

The goal is reproducibility.

A job should be able to answer:

```text
What was run?
With which parameters?
Using which files?
Using which solver?
Using which mesh?
When?
On which worker?
What happened?
Where are the results?
```

---

# 11. Input Validation

Validate simulation inputs before spending resources.

Examples:

```text
frequency > 0
density > 0
viscosity > 0
mesh_size > 0
time_step > 0
```

Also validate:

```text
Required files exist
File formats are valid
Parameters are within allowed ranges
Configuration is internally consistent
```

Bad jobs should fail during preparation rather than halfway through a simulation.

---

# 12. Mock Geometry

The project does not need a real CAD system initially.

Create simple mock geometry descriptions.

Example:

```json
{
    "type": "cylinder",
    "radius": 0.05,
    "height": 0.1
}
```

Eventually this interface could support:

```text
STEP
IGES
STL
CAD APIs
ANSYS geometry
```

But don't implement those initially.

---

# 13. Meshing System

The meshing subsystem should have a generic interface.

```python
class Mesher:

    def generate(self, case):
        raise NotImplementedError
```

Initial implementation:

```text
MockMesher
```

It can generate fake values such as:

```text
Elements: 1,250,000
Nodes: 230,000
Minimum quality: 0.31
Maximum skewness: 0.82
```

It can also simulate:

```text
Successful mesh
Poor-quality mesh
Mesh failure
Timeout
```

Eventually:

```text
MockMesher
     │
     └── FluentMesher
```

The Fluent implementation could eventually automate:

```text
Geometry import
Named selections
Sizing
Inflation
Local refinement
Mesh generation
Mesh export
```

---

# 14. Mesh Validation

A generated mesh should not automatically be accepted.

Check:

```text
Element count
Node count
Minimum quality
Maximum skewness
Orthogonal quality
Negative volumes
Connectivity
Required regions
Boundary names
```

Example:

```text
Mesh quality:
    minimum quality >= 0.2
    maximum skewness <= 0.95
```

If validation fails:

```text
Mesh
 ↓
Validation
 ↓
FAIL
 ↓
Adjust mesh settings
 ↓
Retry
 ↓
Mesh again
```

This introduces realistic simulation workflow behavior.

---

# 15. Solver Setup

Solver setup should be separate from solver execution.

Example:

```text
Solver Setup
    ↓
Create solver configuration
    ↓
Set physics
    ↓
Set material properties
    ↓
Set boundary conditions
    ↓
Set numerical settings
    ↓
Set convergence criteria
    ↓
Create solver input
```

Eventually this could generate real Fluent journal files or other solver configuration files.

---

# 16. Solver Abstraction

Create a generic solver interface:

```python
class Solver:

    def setup(self, case):
        ...

    def run(self, case):
        ...

    def stop(self):
        ...

    def status(self):
        ...
```

Initial implementation:

```text
MockSolver
```

Later:

```text
MockSolver
FluentSolver
OpenFOAMSolver
MATLABSolver
PythonSolver
```

This is one of the most important extensibility points in the project.

---

# 17. Mock Solver

The mock solver should behave like a real computational process.

For example:

```text
Iteration 1
Residual = 1.0e-1

Iteration 2
Residual = 7.4e-2

Iteration 3
Residual = 5.1e-2

...

Iteration 100
Residual = 8.2e-7

CONVERGED
```

The mock solver should take time.

For example:

```python
time.sleep(0.1)
```

This allows the scheduler and monitoring system to interact with an actual running process.

It should support simulated outcomes:

```text
SUCCESS
CONVERGED
FAILED
TIMEOUT
CRASH
NON_CONVERGENCE
CANCELLED
```

---

# 18. Process Management

Do not initially implement the solver as merely:

```python
run_solver()
```

Instead, run it as a separate process.

Conceptually:

```text
Worker
   │
   └── subprocess
          │
          └── Mock Solver
```

The worker should be able to:

```text
Start process
Monitor process
Read stdout
Read stderr
Detect exit code
Terminate process
Kill process
Detect timeout
```

This is valuable real-world systems experience.

---

# 19. Solver Monitoring

The monitoring system should track:

```text
Current iteration
Simulation time
Residuals
Progress
CPU usage
Memory usage
Elapsed time
Estimated completion
```

Example:

```text
JOB: job_001
STATUS: RUNNING

Iteration: 453 / 1000
Progress: 45.3%

Residual:
    continuity = 2.1e-5
    momentum    = 8.4e-6

Elapsed: 00:04:32
```

Eventually this information can be exposed through the API or CLI.

---

# 20. Completion vs Convergence

A solver process finishing does not necessarily mean the simulation succeeded.

For example:

```text
Process exited: 0
```

does not necessarily mean:

```text
Simulation converged
```

Therefore distinguish:

```text
PROCESS SUCCESS
```

from:

```text
SIMULATION SUCCESS
```

A simulation might finish while:

```text
Residuals remain high
Mass imbalance is unacceptable
Solution is unstable
Required iterations were reached
```

The validation stage should determine whether the result is acceptable.

---

# 21. Timeouts

Every job should support a maximum runtime.

Example:

```text
Maximum runtime = 10 minutes
```

If exceeded:

```text
RUNNING
   ↓
TIMEOUT
   ↓
Terminate process
   ↓
Save logs
   ↓
Record failure
```

This prevents workers from becoming permanently occupied.

---

# 22. Cancellation

Users should be able to cancel jobs:

```bash
minislurm cancel job_001
```

The system should:

1. Find the worker.
2. Find the process.
3. Request termination.
4. Force termination if necessary.
5. Update job state.
6. Save logs.
7. Release resources.

---

# 23. Queue

Jobs should not necessarily run immediately.

Example:

```text
QUEUE

job_001   RUNNING
job_002   PENDING
job_003   PENDING
job_004   PENDING
job_005   PENDING
```

The queue should eventually support:

```text
FIFO
Priority
Resource availability
Dependencies
```

---

# 24. Multiple Workers

Start with:

```text
1 worker
```

Then:

```text
2 workers
```

Then:

```text
4 workers
```

Example:

```text
                 Scheduler
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       Worker 1   Worker 2   Worker 3
          │          │          │
        Job 1      Job 2      Job 3
```

This introduces concurrency.

---

# 25. Resource Management

Each job should request resources.

Example:

```yaml
resources:
  cpus: 4
  memory_gb: 8
```

Workers have capacities:

```text
Worker 1:
    CPUs = 8
    Memory = 16 GB
```

The scheduler should not assign:

```text
Job:
    CPUs = 16
```

to:

```text
Worker:
    CPUs = 8
```

Initially these resources can be **simulated** rather than actually enforced.

---

# 26. Resource Simulation

This is particularly useful because the project does not require HPC.

For example:

```text
Virtual cluster:

Worker 1
    CPU: 8
    RAM: 16 GB

Worker 2
    CPU: 8
    RAM: 16 GB
```

A job requesting:

```text
CPU: 4
RAM: 8 GB
```

consumes:

```text
4 CPU
8 GB RAM
```

while running.

The scheduler tracks:

```text
Available resources
Allocated resources
```

---

# 27. Job Priority

Jobs can have priorities.

Example:

```text
Priority 100 → urgent
Priority 50  → normal
Priority 10  → low
```

Queue:

```text
job_001  priority=10
job_002  priority=50
job_003  priority=100
```

Scheduler chooses:

```text
job_003
```

first.

Eventually implement:

```text
priority
+
FIFO tie-breaking
```

---

# 28. Job Dependencies

Eventually support:

```text
Job A
  ↓
Job B
  ↓
Job C
```

For example:

```text
Mesh generation
      ↓
Simulation
      ↓
Post-processing
      ↓
Report generation
```

A job should not start until its dependencies have completed successfully.

This turns the system into a basic workflow engine as well as a scheduler.

---

# 29. Failure Handling

Failures are expected.

Possible failures:

```text
Input validation failure
Mesh failure
Mesh quality failure
Solver crash
Process crash
Timeout
Non-convergence
Worker failure
Disk failure
Invalid result
```

The system should never simply disappear when something fails.

Instead:

```text
Failure
   ↓
Capture error
   ↓
Save logs
   ↓
Update database
   ↓
Release resources
   ↓
Retry or mark FAILED
```

---

# 30. Retry System

Jobs can have:

```text
max_retries = 3
```

Example:

```text
Attempt 1
    ↓
Solver crashes
    ↓
Retry

Attempt 2
    ↓
Timeout
    ↓
Retry

Attempt 3
    ↓
Success
```

Track every attempt separately.

Example:

```text
job_001
    attempt_1 → FAILED
    attempt_2 → TIMEOUT
    attempt_3 → COMPLETED
```

---

# 31. Adaptive Retry

Eventually retries can modify parameters.

Example:

```text
Mesh fails
    ↓
Increase mesh size
    ↓
Retry
```

or:

```text
Solver fails
    ↓
Reduce timestep
    ↓
Retry
```

or:

```text
Non-convergence
    ↓
Increase iteration limit
    ↓
Retry
```

This begins introducing automated simulation engineering logic.

---

# 32. Post-processing

After solver completion:

```text
Solver
   ↓
Post-processing
```

Possible operations:

```text
Extract convergence data
Calculate statistics
Generate plots
Calculate engineering quantities
Extract probes
Calculate forces
Calculate pressure drop
Calculate flow rate
Generate CSV files
Generate images
```

For the mock solver, generate fake result data.

Eventually this can process real solver output.

---

# 33. Result Validation

Results should be checked before being marked successful.

Example:

```text
Check:
    residual < tolerance
    mass imbalance < tolerance
    pressure range valid
    temperature range valid
    required files exist
```

A simulation should only reach:

```text
COMPLETED
```

if:

```text
Solver finished
AND
Results are valid
AND
Required outputs exist
```

---

# 34. Results Storage

Each completed job should have a predictable structure:

```text
results/
└── job_001/
    ├── metadata.json
    ├── mesh/
    ├── solver/
    ├── raw/
    ├── processed/
    ├── plots/
    └── report/
```

This makes simulations reproducible and inspectable.

---

# 35. Database

Start with SQLite.

Store information such as:

```text
jobs
workers
attempts
stages
results
logs
```

Example job record:

```text
ID
Name
Status
Priority
Created
Started
Finished
Worker
Resources
Current stage
Retry count
Exit code
Error
Result path
```

The database should become the persistent source of truth.

---

# 36. Why a Database?

Without persistence:

```text
Program closes
    ↓
Everything disappears
```

With persistence:

```text
Program closes
    ↓
Restart
    ↓
Recover jobs
    ↓
Continue monitoring
```

This is an important systems concept.

---

# 37. Logging

Use structured logging.

Example:

```text
2026-09-06 18:32:10 INFO  job=job_001 stage=PREPARING Starting preparation
2026-09-06 18:32:11 INFO  job=job_001 stage=MESHING Starting mesh
2026-09-06 18:32:16 INFO  job=job_001 stage=MESHING Mesh generated
2026-09-06 18:32:17 INFO  job=job_001 stage=RUNNING Solver started
```

Maintain:

```text
Global logs
Job logs
Stage logs
Worker logs
```

---

# 38. Worker Heartbeats

Eventually workers should report that they are alive.

Example:

```text
Worker 1
    status = RUNNING
    last_heartbeat = 18:32:10
```

If:

```text
current_time - heartbeat > threshold
```

the worker may be considered dead.

This enables worker failure detection.

---

# 39. Worker Failure Recovery

Eventually simulate:

```text
Worker 1
   ↓
running Job 42
   ↓
Worker crashes
```

The manager should detect:

```text
Worker unavailable
```

and then:

```text
Job 42
   ↓
recover
   ↓
requeue
   ↓
Worker 2
```

This is a major systems feature.

---

# 40. Experiment Tracking

The system should eventually support parameter sweeps.

Example:

```text
frequency:
    0.5
    1.0
    1.5

mesh:
    0.5 mm
    1.0 mm

viscosity:
    0.001
    0.002
```

Generate:

```text
3 × 2 × 2 = 12 jobs
```

Each job receives its own:

```text
parameters
job ID
results
logs
status
```

This turns the platform into a basic computational experiment manager.

---

# 41. Parameter Sweep

Eventually support something like:

```bash
minislurm sweep sweep.yaml
```

Example:

```yaml
parameters:
  frequency:
    - 0.5
    - 1.0
    - 1.5

  mesh_size:
    - 0.5
    - 1.0
```

The system automatically creates the jobs.

---

# 42. API

After the CLI works, add a REST API.

Possible endpoints:

```text
POST /jobs
GET  /jobs
GET  /jobs/{id}
POST /jobs/{id}/cancel
POST /jobs/{id}/retry

GET /workers
GET /queue

GET /jobs/{id}/logs
GET /jobs/{id}/results
```

Possible architecture:

```text
Browser / Python Client
          │
          ▼
        REST API
          │
          ▼
      Job Manager
          │
          ▼
       Scheduler
```

---

# 43. CLI and API Should Share the Same Core

Do not put business logic directly into CLI commands.

Bad:

```text
CLI
 └── directly manipulates database
```

Better:

```text
CLI ───────┐
           ▼
       Job Manager
           │
API ───────┘
```

Both interfaces use the same application logic.

---

# 44. Configuration

Keep configuration separate from code.

Example:

```yaml
scheduler:
  max_workers: 4
  scheduling_policy: priority

resources:
  cpu: 8
  memory_gb: 32

jobs:
  max_retries: 3
  default_timeout: 3600

database:
  path: data/minislurm.db
```

---

# 45. Testing

Testing is a major part of the project.

## Unit Tests

Test individual components:

```text
Job
State machine
Queue
Scheduler
Resource manager
Mesh validator
Result validator
Database
```

Example:

```text
test_job_state_transition()
test_priority_queue()
test_resource_allocation()
test_mesh_quality_validation()
```

## Integration Tests

Test complete workflows:

```text
Submit
 ↓
Queue
 ↓
Worker
 ↓
Prepare
 ↓
Mesh
 ↓
Solver
 ↓
Post-process
 ↓
Validate
 ↓
Complete
```

## Failure Tests

Intentionally cause:

```text
Mesh failure
Solver crash
Timeout
Worker crash
Invalid input
Non-convergence
```

and verify the system responds correctly.

---

# 46. Mock Everything Expensive

A major design rule:

> Expensive computation should be replaceable with a mock.

Examples:

```text
MockMesher
MockSolver
MockPostProcessor
MockBackend
```

This means the entire platform can be developed and tested locally.

You do **not** need:

```text
HPC
SLURM
large CFD simulations
GPU clusters
AWS
```

to develop most of the architecture.

---

# 47. Docker

After the local version works, containerize components.

Possible architecture:

```text
Docker
│
├── manager
├── worker
├── API
└── database
```

Initially, don't overcomplicate this.

Start with:

```text
docker run worker
```

Then eventually:

```text
Manager
   │
   ├── Worker container
   ├── Worker container
   └── Worker container
```

---

# 48. Local Backend

The local backend should eventually execute real commands.

For example:

```python
subprocess.Popen(command)
```

This could run:

```text
python simulation.py
```

or eventually:

```text
fluent ...
```

The scheduler does not need to change.

---

# 49. Future Fluent Integration

Eventually create:

```text
FluentSolver
FluentMesher
```

Potential workflow:

```text
Job
 ↓
Preparation
 ↓
Geometry
 ↓
Meshing
 ↓
Fluent mesh
 ↓
Fluent setup
 ↓
Fluent solver
 ↓
Monitor
 ↓
Post-process
 ↓
Results
```

The existing architecture should already support this.

The first implementation should **not** attempt to automate the entire Fluent ecosystem.

Start with one real operation at a time.

---

# 50. Future SLURM Integration

The eventual architecture should support:

```text
Simulation Manager
       │
       ▼
ComputeBackend
       │
       ├── LocalBackend
       └── SlurmBackend
                  │
                  ▼
              sbatch
                  │
                  ▼
             HPC Cluster
```

The SLURM backend might eventually:

```text
Generate job script
Submit with sbatch
Capture job ID
Poll squeue/sacct
Read output
Detect completion
Retrieve results
```

But this should be implemented **after the local system works**.

---

# 51. Future Cloud Integration

The same backend concept can eventually support cloud computing.

For example:

```text
ComputeBackend
│
├── MockBackend
├── LocalBackend
├── DockerBackend
├── SlurmBackend
└── AWSBackend
```

The application can then decide:

```text
Run locally
Run in Docker
Run on HPC
Run in cloud
```

without rewriting the scheduler.

---

# 52. Software Architecture Principles

The project should deliberately practice:

## Separation of Concerns

Each component has one major responsibility.

```text
Scheduler → scheduling
Worker → execution
Pipeline → simulation workflow
Database → persistence
API → communication
CLI → user interface
```

## Dependency Inversion

High-level components should depend on interfaces.

For example:

```text
Worker
   ↓
Backend interface
```

rather than:

```text
Worker
   ↓
directly calls SLURM
```

## Reproducibility

Every job should record:

```text
parameters
inputs
versions
configuration
environment
outputs
```

## Observability

The system should make it easy to determine:

```text
What is happening?
Why did it fail?
Where is the job?
What is the worker doing?
How long has it been running?
```

## Failure as a Normal State

Failures should be designed for rather than treated as unexpected exceptions.

---

# 53. Development Roadmap

Do **not** build everything at once.

Build vertically.

---

## Phase 1 — One Job

Implement:

```text
Job
 ↓
Worker
 ↓
Mock Solver
```

Requirements:

* Create job
* Run job
* Track status
* Save logs
* Detect completion

---

## Phase 2 — Queue

Add:

```text
Job
 ↓
Queue
 ↓
Worker
```

Support:

* multiple jobs
* FIFO
* pending/running/completed

---

## Phase 3 — Multiple Workers

Implement:

```text
Scheduler
   │
   ├── Worker 1
   └── Worker 2
```

Run multiple jobs concurrently.

---

## Phase 4 — Process Management

Add:

```text
subprocess
stdout
stderr
exit codes
termination
timeouts
```

---

## Phase 5 — Full Simulation Pipeline

Add:

```text
Preparation
 ↓
Validation
 ↓
Meshing
 ↓
Mesh validation
 ↓
Solver setup
 ↓
Solver
 ↓
Post-processing
 ↓
Result validation
```

All components can initially be mocked.

---

## Phase 6 — Persistence

Add:

```text
SQLite
```

Store:

```text
Jobs
Attempts
Workers
Stages
Results
Logs
```

---

## Phase 7 — Failure Recovery

Implement:

```text
Retries
Timeouts
Cancellation
Worker failure
Job recovery
```

---

## Phase 8 — Resources

Implement:

```text
CPU
Memory
Resource allocation
Resource release
```

---

## Phase 9 — Priority

Add:

```text
Priority scheduling
```

---

## Phase 10 — Experiment Management

Add:

```text
Parameter sweeps
Experiment IDs
Run comparison
```

---

## Phase 11 — API

Add:

```text
REST API
```

---

## Phase 12 — Docker

Containerize:

```text
Worker
Manager
API
```

---

## Phase 13 — Real Local Computation

Replace mock solver with a lightweight real computation.

Examples:

```text
Python numerical model
MATLAB model
small CFD model
OpenFOAM case
```

---

## Phase 14 — Real Meshing

Add a real meshing backend.

---

## Phase 15 — Real Fluent Integration

Implement:

```text
FluentMesher
FluentSolver
Fluent monitoring
```

incrementally.

---

## Phase 16 — SLURM Backend

Eventually integrate:

```text
sbatch
squeue
sacct
scancel
```

---

# 54. Suggested Git Workflow

Use Git throughout the project.

Example:

```text
main
 │
 ├── feature/job-model
 ├── feature/queue
 ├── feature/workers
 ├── feature/database
 ├── feature/resources
 ├── feature/retry-system
 └── feature/fluent-backend
```

Commit small, meaningful changes.

Examples:

```text
Add job state machine
Add FIFO queue
Add worker process
Add mock solver
Add SQLite persistence
Add retry handling
Add resource allocation
```

---

# 55. Definition of Done

The project should eventually be capable of:

```text
[✓] Submit jobs
[✓] Queue jobs
[✓] Schedule jobs
[✓] Run multiple workers
[✓] Manage resources
[✓] Prepare simulation cases
[✓] Validate inputs
[✓] Generate meshes
[✓] Validate meshes
[✓] Configure solver
[✓] Run solver processes
[✓] Monitor progress
[✓] Detect convergence
[✓] Detect failures
[✓] Handle timeouts
[✓] Cancel jobs
[✓] Retry jobs
[✓] Recover failed workers
[✓] Post-process results
[✓] Validate results
[✓] Store results
[✓] Persist state
[✓] Track experiments
[✓] Run parameter sweeps
[✓] Expose API
[✓] Provide CLI
[✓] Run tests
[✓] Run in Docker
[ ] Run real Fluent jobs
[ ] Run on SLURM
[ ] Run on cloud infrastructure
```

The final three are deliberately future goals.

---

# 56. What This Project Demonstrates

This project should demonstrate more than:

> "I wrote a Python script that runs simulations."

It demonstrates:

### Software Engineering

```text
Architecture
Interfaces
Modularity
Testing
Git
Configuration
Error handling
```

### Systems Engineering

```text
Processes
Queues
Scheduling
Concurrency
Resources
Failure recovery
Persistence
Monitoring
```

### Simulation Engineering

```text
Case preparation
Meshing
Mesh validation
Solver setup
Solver execution
Convergence
Post-processing
Result validation
```

### HPC Concepts

```text
Workers
Resource allocation
Job states
Queues
Priorities
Job dependencies
SLURM abstraction
```

### Engineering Automation

```text
Parameter sweeps
Experiment tracking
Automated validation
Automated retries
Reproducible simulations
```

---

# 57. What NOT to Do

Do not start by implementing:

```text
Distributed Kubernetes cluster
Full SLURM clone
Real CFD solver
Complete Fluent automation
Cloud infrastructure
Microservices
Complex frontend
```

That will create a huge amount of complexity before the fundamentals work.

Instead:

```text
1 job
 ↓
1 worker
 ↓
mock solver
```

Then:

```text
10 jobs
 ↓
2 workers
 ↓
queue
```

Then:

```text
database
 ↓
failure recovery
 ↓
resources
 ↓
simulation pipeline
```

Then add real computational backends.

---

# 58. Recommended Initial Version

The first meaningful version should be surprisingly small.

```text
mini-slurm/
│
├── src/
│   └── minislurm/
│       ├── job.py
│       ├── queue.py
│       ├── worker.py
│       └── mock_solver.py
│
├── tests/
│
└── README.md
```

It should be able to do:

```bash
minislurm submit
```

and produce:

```text
Job submitted: job_001

Status:
    PENDING

Worker:
    worker_01

Starting...

Stage:
    RUNNING

Iteration:
    50 / 100

Residual:
    2.4e-4

Completed successfully.
```

Once this works, add complexity one feature at a time.

---

# 59. Final Architecture

The eventual complete architecture is:

```text
                              USER
                               │
                     ┌─────────┴─────────┐
                     │                   │
                    CLI                 API
                     │                   │
                     └─────────┬─────────┘
                               │
                        ┌──────▼──────┐
                        │ Job Manager │
                        └──────┬──────┘
                               │
                        ┌──────▼──────┐
                        │  Scheduler  │
                        └──────┬──────┘
                               │
                           Job Queue
                               │
                    ┌──────────▼──────────┐
                    │     Worker Manager  │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
          Worker 1          Worker 2         Worker 3
              │                │                │
              └────────────────┼────────────────┘
                               │
                        Compute Backend
                               │
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
          Mock             Local             SLURM
             │                 │                 │
             └─────────────────┼─────────────────┘
                               │
                     Simulation Pipeline
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
     Preparation            Meshing              Solver
          │                    │                    │
          ▼                    ▼                    ▼
       Validate          Mesh Validate        Monitor
          │                    │                    │
          └────────────────────┼────────────────────┘
                               │
                               ▼
                       Post-processing
                               │
                               ▼
                         Result Validation
                               │
                               ▼
                       Results / Reports
                               │
                               ▼
                          Persistence
                               │
                         ┌─────┴─────┐
                         ▼           ▼
                      SQLite       Logs
```

The important architectural idea is:

> **One project. Separate responsibilities. Replaceable implementations.**

The scheduler does not care whether the job is Fluent, OpenFOAM, MATLAB, Python, or a mock computation.

The simulation pipeline does not care whether it is running locally, inside Docker, on SLURM, or eventually in the cloud.

That separation is what allows this relatively small local project to eventually grow into a genuine **simulation workflow and compute-management platform**.
