# Design Document

## Overview

The Efficient Logistics Scheduling system is a full-stack application that bridges classical and quantum optimization approaches for supply chain routing problems. The architecture follows a modular pipeline design with clear separation between data processing, optimization engines, API services, and presentation layers. The system uses Qiskit for quantum simulation, OR-Tools for classical optimization, FastAPI for the backend service, and provides both Streamlit and React frontend options.

## Architecture

The system follows a layered architecture with five primary layers:

### Layer 1: Data Layer
- Raw dataset ingestion (CSV/Excel from Kaggle supply chain data)
- Data cleaning and validation
- Cost matrix generation
- Persistent storage of processed instances

### Layer 2: Problem Formulation Layer
- QUBO matrix construction from cost matrices
- TSP encoding with constraint penalties
- Matrix symmetrization and validation
- Serialization for solver consumption

### Layer 3: Solver Layer
- **Classical Solver**: OR-Tools routing library for TSP/VRP
- **Quantum Solver**: Qiskit QAOA with configurable parameters
- Solution decoding and validation
- Cost calculation and metrics

### Layer 4: Service Layer
- FastAPI REST endpoints
- Request validation and error handling
- Solver orchestration
- Result formatting and caching

### Layer 5: Presentation Layer
- **Option A**: Streamlit dashboard (rapid prototyping)
- **Option B**: React + Tailwind SPA (production-ready)
- Interactive visualizations (Plotly, Matplotlib)
- File upload and parameter controls

### Cross-Cutting Concerns
- Logging and monitoring
- Error handling and validation
- Configuration management
- Testing infrastructure

## Components and Interfaces

### 1. Data Preprocessing Module (`src/preprocessing/preprocess.py`)

**Purpose**: Transform raw supply chain data into optimization-ready formats

**Key Functions**:
```python
def load_and_clean(path: str) -> Tuple[pd.DataFrame, Dict[str, int]]
    """Load CSV, drop NA rows, create location-to-index mapping"""
    
def build_cost_matrix(df: pd.DataFrame, mapping: Dict[str, int]) -> Tuple[np.ndarray, List[str]]
    """Generate NxN cost matrix from edge list, handle missing edges"""
    
def save_instance(matrix: np.ndarray, names: List[str], output_path: str) -> None
    """Persist processed instance for reproducibility"""
```

**Inputs**: CSV file with columns: source, destination, transport_cost
**Outputs**: Cost matrix (numpy array), location names (list), mapping (dict)

### 2. QUBO Builder Module (`src/qubo/qubo_builder.py`)

**Purpose**: Encode TSP as QUBO matrix for quantum solving

**Key Functions**:
```python
def build_tsp_qubo(dist: np.ndarray, penalty_A: float = 500, penalty_B: float = 500) -> np.ndarray
    """
    Construct QUBO matrix for TSP with n cities
    Variables: x_{i,p} = 1 if city i is at position p
    Constraints: sum_i x_{i,p} = 1 and sum_p x_{i,p} = 1
    """
    
def validate_qubo(Q: np.ndarray) -> bool
    """Check symmetry and finite values"""
```

**Inputs**: Distance matrix (n x n), penalty weights
**Outputs**: QUBO matrix (n² x n²), symmetric and real-valued

**QUBO Formulation**:
- Decision variables: x_{i,p} ∈ {0,1} for i,p ∈ {0,...,n-1}
- Objective: minimize Σ_p Σ_{i,j} dist[i][j] * x_{i,p} * x_{j,(p+1) mod n}
- Constraint 1: Σ_i x_{i,p} = 1 (each position has one city)
- Constraint 2: Σ_p x_{i,p} = 1 (each city appears once)

### 3. Classical Solver Module (`src/classical/ortools_solver.py`)

**Purpose**: Provide baseline solutions using proven classical algorithms

**Key Functions**:
```python
def solve_tsp(dist_matrix: np.ndarray, time_limit_seconds: int = 30) -> Dict[str, Any]
    """
    Solve TSP using OR-Tools routing library
    Returns: {
        'route': List[int],
        'cost': float,
        'solve_time': float,
        'status': str
    }
    """
    
def calculate_route_cost(route: List[int], dist_matrix: np.ndarray) -> float
    """Compute total cost of a given route"""
```

**Algorithm**: OR-Tools RoutingModel with PATH_CHEAPEST_ARC first solution strategy
**Performance**: Optimal or near-optimal for n < 20, heuristic for larger instances

### 4. Quantum Solver Module (`src/quantum/qiskit_qaoa.py`)

**Purpose**: Solve QUBO using QAOA simulation on Qiskit

**Key Functions**:
```python
def qubo_to_quadraticprogram(Q: np.ndarray) -> QuadraticProgram
    """Convert numpy QUBO matrix to Qiskit QuadraticProgram"""
    
def run_qaoa(Q: np.ndarray, reps: int = 1, shots: int = 1024, optimizer: str = 'COBYLA') -> Dict[str, Any]
    """
    Execute QAOA with specified parameters
    Returns: {
        'solution': List[int],
        'cost': float,
        'raw_result': MinimumEigenOptimizer result,
        'circuit_depth': int,
        'execution_time': float
    }
    """
    
def decode_solution(bitstring: str, n_cities: int) -> List[int]
    """Convert binary solution to route representation"""
```

**QAOA Configuration**:
- Sampler: Qiskit Aer StatevectorSampler or Sampler primitive
- Optimizer: COBYLA with maxiter=100 (configurable)
- Circuit depth: p=1 for Phase 1, p=1-3 for Phase 2
- Shots: 1024 default (configurable)

### 5. Visualization Module (`src/viz/plots.py`)

**Purpose**: Generate static and interactive visualizations

**Key Functions**:
```python
def plot_cost_heatmap(matrix: np.ndarray, names: List[str], output_path: str) -> None
    """Seaborn heatmap of cost matrix"""
    
def plot_route_graph(route: List[int], names: List[str], dist_matrix: np.ndarray, output_path: str) -> None
    """NetworkX graph visualization of route"""
    
def plot_comparison_bar(classical_cost: float, quantum_cost: float, output_path: str) -> None
    """Bar chart comparing solver costs"""
    
def create_interactive_plot(data: Dict[str, Any]) -> str
    """Generate Plotly HTML for embedding in frontend"""
```

**Visualization Types**:
- Cost matrix heatmap (Seaborn)
- Route network graph (NetworkX + Matplotlib)
- Cost comparison bar chart (Matplotlib)
- Interactive parameter sweep (Plotly)

### 6. Backend API Module (`src/api/main.py`)

**Purpose**: Expose HTTP endpoints for frontend consumption

**Endpoints**:
```python
GET /status
    Response: {"status": "ok", "version": "1.0.0"}

POST /api/preprocess
    Request: {"file_path": str, "max_nodes": int}
    Response: {"n_locations": int, "cost_matrix_shape": [int, int], "location_names": List[str]}

POST /api/solve/classical
    Request: {"instance_id": str}
    Response: {"route": List[int], "cost": float, "solve_time": float}

POST /api/solve/quantum
    Request: {"instance_id": str, "reps": int, "shots": int}
    Response: {"solution": List[int], "cost": float, "circuit_depth": int, "execution_time": float}

GET /api/visualizations/{viz_type}
    Response: Image file (PNG) or JSON for interactive plots

POST /api/compare
    Request: {"instance_id": str, "classical_result": Dict, "quantum_result": Dict}
    Response: {"comparison_chart": str, "metrics": Dict}
```

**Error Handling**: All endpoints return appropriate HTTP status codes (400, 404, 500) with error messages

### 7. Frontend Components

**Streamlit Option** (`frontend/streamlit_app.py`):
- Single-file application
- File uploader widget
- Solver parameter sliders
- Inline plot rendering
- Session state management

**React Option** (`frontend/src/`):
- Component structure:
  - `App.tsx`: Main application container
  - `FileUpload.tsx`: Dataset upload component
  - `SolverControls.tsx`: Parameter configuration
  - `ResultsDisplay.tsx`: Route and cost visualization
  - `ComparisonView.tsx`: Side-by-side solver comparison
- State management: React hooks (useState, useEffect)
- API client: Axios for HTTP requests
- Styling: Tailwind CSS utility classes

## Data Models

### CostMatrix
```python
@dataclass
class CostMatrix:
    matrix: np.ndarray  # Shape: (n, n)
    location_names: List[str]  # Length: n
    mapping: Dict[str, int]  # Location name -> index
    
    def __post_init__(self):
        assert self.matrix.shape[0] == self.matrix.shape[1]
        assert len(self.location_names) == self.matrix.shape[0]
```

### QUBOInstance
```python
@dataclass
class QUBOInstance:
    Q: np.ndarray  # Shape: (n², n²)
    n_cities: int
    penalty_A: float
    penalty_B: float
    source_cost_matrix: CostMatrix
    
    def is_symmetric(self) -> bool:
        return np.allclose(self.Q, self.Q.T)
```

### SolverResult
```python
@dataclass
class SolverResult:
    route: List[int]
    cost: float
    solve_time: float
    solver_type: str  # 'classical' or 'quantum'
    metadata: Dict[str, Any]  # Solver-specific info
    
    def is_valid_route(self, n_cities: int) -> bool:
        return len(self.route) == n_cities and set(self.route) == set(range(n_cities))
```

### ComparisonMetrics
```python
@dataclass
class ComparisonMetrics:
    classical_cost: float
    quantum_cost: float
    cost_ratio: float  # quantum / classical
    classical_time: float
    quantum_time: float
    time_ratio: float
    
    def quantum_advantage(self) -> bool:
        return self.quantum_cost < self.classical_cost
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Data preprocessing preserves location count
*For any* valid supply chain dataset with N unique locations, after preprocessing, the cost matrix dimensions should equal N×N and the location names list should have length N.
**Validates: Requirements 1.3, 1.4**

### Property 2: Cost matrix diagonal is zero
*For any* generated cost matrix, all diagonal elements (i,i) should equal zero, representing zero cost to travel from a location to itself.
**Validates: Requirements 1.4**

### Property 3: QUBO matrix symmetry
*For any* QUBO matrix Q generated from a cost matrix, Q should be symmetric: Q[i][j] = Q[j][i] for all i,j.
**Validates: Requirements 2.4**

### Property 4: QUBO dimension correctness
*For any* TSP instance with n cities, the generated QUBO matrix should have dimensions n²×n².
**Validates: Requirements 2.1**

### Property 5: Classical route validity
*For any* classical solver result for an n-city problem, the route should contain each city index from 0 to n-1 exactly once.
**Validates: Requirements 3.2**

### Property 6: Route cost calculation consistency
*For any* route and cost matrix, calculating the route cost by summing edge costs should match the cost reported by the solver.
**Validates: Requirements 3.3**

### Property 7: QAOA solution binary constraint
*For any* QAOA solution vector, all elements should be binary values (0 or 1).
**Validates: Requirements 4.3**

### Property 8: QuadraticProgram conversion preserves QUBO
*For any* QUBO matrix Q, converting to QuadraticProgram and extracting the quadratic coefficients should reproduce the original Q.
**Validates: Requirements 4.1**

### Property 9: Visualization file generation
*For any* successful visualization call, the specified output file should exist and be a valid image format.
**Validates: Requirements 5.4**

### Property 10: API endpoint response structure
*For any* successful API request to solver endpoints, the response should contain 'route', 'cost', and timing fields.
**Validates: Requirements 6.3, 6.4**

### Property 11: Cost comparison non-negativity
*For any* comparison between classical and quantum costs, both cost values should be non-negative.
**Validates: Requirements 5.3**

### Property 12: QAOA circuit depth matches parameter
*For any* QAOA execution with circuit depth parameter p, the constructed circuit should have exactly p repetitions of the cost and mixer layers.
**Validates: Requirements 4.5**

## Error Handling

### Data Layer Errors
- **Missing columns**: Raise `ValueError` with specific missing column names
- **Empty dataset**: Raise `ValueError` indicating no valid records
- **Invalid cost values**: Replace negative costs with absolute values, log warning
- **File not found**: Raise `FileNotFoundError` with helpful message

### QUBO Construction Errors
- **Non-square matrix**: Raise `ValueError` before QUBO construction
- **Invalid penalty weights**: Raise `ValueError` if penalties ≤ 0
- **Matrix too large**: Raise `MemoryError` if n² > 10,000 (configurable threshold)

### Solver Errors
- **OR-Tools no solution**: Return status='INFEASIBLE' with empty route
- **QAOA convergence failure**: Log warning, return best solution found
- **Timeout exceeded**: Return partial solution with timeout flag
- **Invalid parameters**: Raise `ValueError` before solver invocation

### API Errors
- **400 Bad Request**: Invalid request parameters, return error details
- **404 Not Found**: Instance ID not found, suggest valid IDs
- **500 Internal Server Error**: Solver crash, return stack trace in debug mode
- **503 Service Unavailable**: System overloaded, return retry-after header

### Frontend Errors
- **Upload failure**: Display user-friendly message, suggest file format
- **API timeout**: Show loading spinner, implement retry logic
- **Visualization error**: Display placeholder, log error to console

## Testing Strategy

### Unit Testing Framework
- **Framework**: pytest for Python backend
- **Coverage target**: >80% for core modules (preprocessing, QUBO, solvers)
- **Test organization**: Mirror source structure in `tests/` directory

### Unit Test Categories

**Data Preprocessing Tests** (`tests/test_preprocessing.py`):
- Test loading valid CSV files
- Test handling missing values
- Test cost matrix construction with known inputs
- Test edge cases: single location, disconnected graph

**QUBO Builder Tests** (`tests/test_qubo.py`):
- Test QUBO symmetry for various matrix sizes
- Test QUBO dimensions match expected n²
- Test penalty term coefficients
- Test edge case: n=2 (smallest TSP)

**Classical Solver Tests** (`tests/test_classical.py`):
- Test route validity (all cities visited once)
- Test cost calculation matches manual computation
- Test small known instances (n=3,4,5)
- Test timeout handling

**Quantum Solver Tests** (`tests/test_quantum.py`):
- Test QuadraticProgram conversion
- Test QAOA execution completes without errors
- Test solution decoding produces valid routes
- Test parameter variations (reps, shots)

**API Tests** (`tests/test_api.py`):
- Test all endpoints return correct status codes
- Test request validation rejects invalid inputs
- Test response schemas match specifications
- Test error handling for edge cases

### Property-Based Testing Framework
- **Framework**: Hypothesis for Python
- **Configuration**: 100 iterations per property minimum
- **Generators**: Custom strategies for cost matrices, routes, QUBO matrices

### Property-Based Tests

**Property Test 1: Data preprocessing preserves location count** (`tests/test_properties.py`)
```python
@given(st.data())
def test_preprocessing_preserves_count(data):
    """Feature: logistics-qaoa-system, Property 1: Data preprocessing preserves location count"""
    # Generate random supply chain data
    # Run preprocessing
    # Assert: cost_matrix.shape[0] == n_unique_locations
```
**Validates: Requirements 1.3, 1.4**

**Property Test 2: Cost matrix diagonal is zero** (`tests/test_properties.py`)
```python
@given(cost_matrices())
def test_cost_matrix_diagonal_zero(cost_matrix):
    """Feature: logistics-qaoa-system, Property 2: Cost matrix diagonal is zero"""
    # Assert: np.diag(cost_matrix) == 0
```
**Validates: Requirements 1.4**

**Property Test 3: QUBO matrix symmetry** (`tests/test_properties.py`)
```python
@given(cost_matrices())
def test_qubo_symmetry(cost_matrix):
    """Feature: logistics-qaoa-system, Property 3: QUBO matrix symmetry"""
    Q = build_tsp_qubo(cost_matrix)
    # Assert: np.allclose(Q, Q.T)
```
**Validates: Requirements 2.4**

**Property Test 4: QUBO dimension correctness** (`tests/test_properties.py`)
```python
@given(st.integers(min_value=2, max_value=10))
def test_qubo_dimensions(n):
    """Feature: logistics-qaoa-system, Property 4: QUBO dimension correctness"""
    cost_matrix = generate_random_cost_matrix(n)
    Q = build_tsp_qubo(cost_matrix)
    # Assert: Q.shape == (n*n, n*n)
```
**Validates: Requirements 2.1**

**Property Test 5: Classical route validity** (`tests/test_properties.py`)
```python
@given(cost_matrices())
def test_classical_route_validity(cost_matrix):
    """Feature: logistics-qaoa-system, Property 5: Classical route validity"""
    result = solve_tsp(cost_matrix)
    n = cost_matrix.shape[0]
    # Assert: set(result['route']) == set(range(n))
    # Assert: len(result['route']) == n
```
**Validates: Requirements 3.2**

**Property Test 6: Route cost calculation consistency** (`tests/test_properties.py`)
```python
@given(cost_matrices(), valid_routes())
def test_route_cost_consistency(cost_matrix, route):
    """Feature: logistics-qaoa-system, Property 6: Route cost calculation consistency"""
    manual_cost = sum(cost_matrix[route[i], route[(i+1)%len(route)]] for i in range(len(route)))
    calculated_cost = calculate_route_cost(route, cost_matrix)
    # Assert: np.isclose(manual_cost, calculated_cost)
```
**Validates: Requirements 3.3**

**Property Test 7: QAOA solution binary constraint** (`tests/test_properties.py`)
```python
@given(qubo_matrices())
def test_qaoa_binary_solution(Q):
    """Feature: logistics-qaoa-system, Property 7: QAOA solution binary constraint"""
    result = run_qaoa(Q, reps=1, shots=100)
    solution = result['solution']
    # Assert: all(x in [0, 1] for x in solution)
```
**Validates: Requirements 4.3**

**Property Test 8: QuadraticProgram conversion preserves QUBO** (`tests/test_properties.py`)
```python
@given(qubo_matrices())
def test_quadratic_program_conversion(Q):
    """Feature: logistics-qaoa-system, Property 8: QuadraticProgram conversion preserves QUBO"""
    qp = qubo_to_quadraticprogram(Q)
    reconstructed_Q = extract_qubo_from_qp(qp)
    # Assert: np.allclose(Q, reconstructed_Q)
```
**Validates: Requirements 4.1**

**Property Test 9: Visualization file generation** (`tests/test_properties.py`)
```python
@given(cost_matrices())
def test_visualization_creates_file(cost_matrix):
    """Feature: logistics-qaoa-system, Property 9: Visualization file generation"""
    output_path = "test_output.png"
    plot_cost_heatmap(cost_matrix, names=[], output_path=output_path)
    # Assert: os.path.exists(output_path)
    # Assert: is_valid_image(output_path)
```
**Validates: Requirements 5.4**

**Property Test 10: API endpoint response structure** (`tests/test_properties.py`)
```python
@given(st.data())
def test_api_response_structure(data):
    """Feature: logistics-qaoa-system, Property 10: API endpoint response structure"""
    # Make API request to solver endpoint
    response = client.post("/api/solve/classical", json={"instance_id": "test"})
    # Assert: 'route' in response.json()
    # Assert: 'cost' in response.json()
    # Assert: 'solve_time' in response.json()
```
**Validates: Requirements 6.3, 6.4**

**Property Test 11: Cost comparison non-negativity** (`tests/test_properties.py`)
```python
@given(solver_results(), solver_results())
def test_cost_non_negativity(classical_result, quantum_result):
    """Feature: logistics-qaoa-system, Property 11: Cost comparison non-negativity"""
    # Assert: classical_result['cost'] >= 0
    # Assert: quantum_result['cost'] >= 0
```
**Validates: Requirements 5.3**

**Property Test 12: QAOA circuit depth matches parameter** (`tests/test_properties.py`)
```python
@given(st.integers(min_value=1, max_value=5))
def test_qaoa_circuit_depth(p):
    """Feature: logistics-qaoa-system, Property 12: QAOA circuit depth matches parameter"""
    Q = generate_small_qubo()
    result = run_qaoa(Q, reps=p, shots=100)
    # Assert: result['circuit_depth'] == p
```
**Validates: Requirements 4.5**

### Integration Testing
- Test end-to-end flow: upload → preprocess → solve → visualize
- Test API + frontend integration with mock data
- Test Docker container startup and health checks

### Performance Testing
- Benchmark classical solver on instances n=5,10,15,20
- Benchmark QAOA simulation time vs circuit depth
- Test API response times under concurrent requests

### Continuous Integration
- **Platform**: GitHub Actions
- **Triggers**: Push to main, pull requests
- **Jobs**:
  1. Lint (flake8, black)
  2. Type check (mypy)
  3. Unit tests (pytest with coverage)
  4. Property tests (pytest with Hypothesis)
  5. Build Docker image
  6. Integration tests

## Deployment Architecture

### Development Environment
- Local Python virtual environment
- Qiskit Aer simulator (no cloud access needed)
- SQLite for instance storage (optional)
- Hot reload for API and frontend

### Production Deployment Options

**Option 1: Docker Compose (Recommended for Phase 1)**
- Backend container: Python + FastAPI + Qiskit
- Frontend container: Node + React build or Streamlit
- Shared volume for data and results
- Nginx reverse proxy (optional)

**Option 2: Cloud Platform (Phase 2)**
- Backend: Heroku, Render, or AWS ECS
- Frontend: Vercel, Netlify, or S3 + CloudFront
- Storage: AWS S3 or Google Cloud Storage
- Database: PostgreSQL for instance metadata

### Configuration Management
- Environment variables for:
  - API base URL
  - QAOA default parameters
  - File upload limits
  - Solver timeouts
- Config files: `.env` for local, secrets manager for production

### Monitoring and Logging
- Structured logging with Python `logging` module
- Log levels: DEBUG (development), INFO (production)
- Metrics to track:
  - Solver execution times
  - API request counts and latencies
  - Error rates by endpoint
  - QAOA convergence statistics

## Technology Stack Summary

**Backend**:
- Python 3.10+
- Qiskit 0.45+ (quantum simulation)
- qiskit-optimization (QAOA utilities)
- OR-Tools 9.7+ (classical optimization)
- FastAPI 0.104+ (REST API)
- NumPy, Pandas (data processing)
- Hypothesis (property-based testing)

**Visualization**:
- Matplotlib 3.8+ (static plots)
- Seaborn 0.13+ (heatmaps)
- Plotly 5.18+ (interactive charts)
- NetworkX 3.2+ (graph visualization)

**Frontend Option A**:
- Streamlit 1.28+ (rapid dashboard)

**Frontend Option B**:
- React 18+ with TypeScript
- Tailwind CSS 3.3+
- Axios (HTTP client)
- Recharts or Plotly.js (charts)

**DevOps**:
- Docker 24+ and Docker Compose
- pytest 7.4+ (testing)
- GitHub Actions (CI/CD)
- Black, flake8 (code quality)

## Security Considerations

- **File Upload**: Validate file types, limit size to 10MB
- **API Rate Limiting**: Implement per-IP limits to prevent abuse
- **Input Validation**: Sanitize all user inputs, reject malicious payloads
- **CORS**: Configure appropriate origins for frontend access
- **Secrets**: Never commit API keys or credentials, use environment variables
- **Dependencies**: Regular security audits with `pip-audit` or Snyk

## Performance Optimization

- **Caching**: Cache QUBO matrices and solver results by instance hash
- **Async Processing**: Use FastAPI background tasks for long-running solvers
- **Matrix Operations**: Use NumPy vectorization, avoid Python loops
- **QAOA Optimization**: Start with p=1, increase only if needed
- **Frontend**: Lazy load visualizations, paginate large result sets
- **Database Indexing**: Index instance IDs for fast lookup (if using DB)

## Future Enhancements (Out of Scope for Phase 1-2)

- Real quantum hardware execution via IBM Quantum or AWS Braket
- Multi-vehicle routing problem (VRP) support
- Genetic algorithm baseline for comparison
- Real-time optimization with streaming data
- User authentication and project management
- Advanced visualizations: 3D route maps, animation
- Hyperparameter tuning for QAOA (grid search, Bayesian optimization)
- Distributed solving for large instances
