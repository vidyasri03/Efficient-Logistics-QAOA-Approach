# Implementation Plan

- [x] 1. Set up project structure and dependencies



  - Create directory structure: src/, tests/, frontend/, data/, docs/
  - Create requirements.txt with all Python dependencies
  - Create .gitignore for Python, Node, and data files
  - Create README.md with project overview and setup instructions
  - _Requirements: 10.1, 10.5_




- [x] 2. Implement data preprocessing module


  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [ ] 2.1 Create preprocessing core functions
  - Implement `load_and_clean()` to parse CSV and handle missing values
  - Implement `build_cost_matrix()` to generate NxN cost matrix from edge list


  - Implement `save_instance()` to persist processed data
  - Add input validation and error handling

  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [x] 2.2 Write property test for preprocessing location count preservation


  - **Property 1: Data preprocessing preserves location count**
  - **Validates: Requirements 1.3, 1.4**



- [x] 2.3 Write property test for cost matrix diagonal


  - **Property 2: Cost matrix diagonal is zero**
  - **Validates: Requirements 1.4**

- [ ] 2.4 Write unit tests for preprocessing edge cases
  - Test empty dataset handling


  - Test single location dataset
  - Test disconnected graph handling

  - _Requirements: 1.1, 1.2_

- [x] 3. Implement QUBO builder module

  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [ ] 3.1 Create QUBO construction functions
  - Implement `build_tsp_qubo()` with TSP encoding and constraint penalties


  - Implement `validate_qubo()` to check symmetry and finite values
  - Add configurable penalty weights (A, B parameters)
  - Implement matrix symmetrization


  - _Requirements: 2.1, 2.2, 2.3, 2.4_




- [ ] 3.2 Write property test for QUBO symmetry
  - **Property 3: QUBO matrix symmetry**
  - **Validates: Requirements 2.4**



- [ ] 3.3 Write property test for QUBO dimensions
  - **Property 4: QUBO dimension correctness**

  - **Validates: Requirements 2.1**

- [x] 3.4 Implement QUBO persistence

  - Add save/load functions for QUBO matrices
  - Support both .npy and .csv formats
  - _Requirements: 2.5_



- [ ] 3.5 Write unit tests for QUBO builder
  - Test n=2 edge case (smallest TSP)


  - Test penalty term coefficients
  - Test invalid input handling
  - _Requirements: 2.1, 2.2, 2.3_

- [x] 4. Implement classical solver module

  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 4.1 Create OR-Tools TSP solver

  - Implement `solve_tsp()` using OR-Tools RoutingModel
  - Implement `calculate_route_cost()` for cost computation
  - Add timeout configuration

  - Return structured result with route, cost, solve_time, status
  - _Requirements: 3.1, 3.2, 3.3, 3.4_


- [ ] 4.2 Write property test for classical route validity
  - **Property 5: Classical route validity**
  - **Validates: Requirements 3.2**

- [ ] 4.3 Write property test for route cost consistency
  - **Property 6: Route cost calculation consistency**
  - **Validates: Requirements 3.3**



- [x] 4.4 Write unit tests for classical solver


  - Test small known instances (n=3, 4, 5)
  - Test timeout handling
  - Test infeasible problem handling
  - _Requirements: 3.1, 3.4, 3.5_


- [ ] 5. Implement quantum solver module
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 5.1 Create QAOA solver functions

  - Implement `qubo_to_quadraticprogram()` for Qiskit conversion
  - Implement `run_qaoa()` with configurable reps and shots
  - Implement `decode_solution()` to convert bitstring to route

  - Configure Qiskit Sampler and COBYLA optimizer
  - _Requirements: 4.1, 4.2, 4.3_

- [-] 5.2 Write property test for QAOA binary solution

  - **Property 7: QAOA solution binary constraint**
  - **Validates: Requirements 4.3**



- [ ] 5.3 Write property test for QuadraticProgram conversion
  - **Property 8: QuadraticProgram conversion preserves QUBO**
  - **Validates: Requirements 4.1**


- [ ] 5.4 Write property test for QAOA circuit depth
  - **Property 12: QAOA circuit depth matches parameter**
  - **Validates: Requirements 4.5**


- [ ] 5.5 Write unit tests for quantum solver
  - Test QAOA execution completes without errors
  - Test parameter variations (reps=1,2,3)
  - Test solution decoding
  - _Requirements: 4.2, 4.4_


- [ ] 6. Checkpoint - Ensure all core solver tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 7. Implement visualization module
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_


- [ ] 7.1 Create static visualization functions
  - Implement `plot_cost_heatmap()` using Seaborn

  - Implement `plot_route_graph()` using NetworkX and Matplotlib
  - Implement `plot_comparison_bar()` for cost comparison
  - Add output directory management
  - _Requirements: 5.1, 5.2, 5.3, 5.4_



- [ ] 7.2 Create interactive visualization functions
  - Implement `create_interactive_plot()` using Plotly


  - Generate HTML output for web embedding
  - _Requirements: 5.5_

- [ ] 7.3 Write property test for visualization file generation
  - **Property 9: Visualization file generation**

  - **Validates: Requirements 5.4**

- [ ] 7.4 Write unit tests for visualizations
  - Test heatmap generation
  - Test route graph generation
  - Test comparison chart generation

  - _Requirements: 5.1, 5.2, 5.3_

- [ ] 8. Implement Backend API
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_


- [ ] 8.1 Create FastAPI application structure
  - Set up FastAPI app with CORS middleware
  - Define Pydantic models for request/response schemas
  - Implement error handlers for common exceptions


  - _Requirements: 6.1, 6.5_

- [ ] 8.2 Implement preprocessing endpoint
  - Create POST /api/preprocess endpoint
  - Integrate with preprocessing module
  - Return location count and matrix shape
  - _Requirements: 6.2_



- [x] 8.3 Implement solver endpoints

  - Create POST /api/solve/classical endpoint

  - Create POST /api/solve/quantum endpoint
  - Integrate with solver modules
  - Return structured JSON responses
  - _Requirements: 6.3, 6.4_


- [ ] 8.4 Implement utility endpoints
  - Create GET /status endpoint
  - Create GET /api/visualizations/{viz_type} endpoint
  - Create POST /api/compare endpoint
  - _Requirements: 6.1_


- [ ] 8.5 Write property test for API response structure
  - **Property 10: API endpoint response structure**
  - **Validates: Requirements 6.3, 6.4**




- [x] 8.6 Write unit tests for API endpoints

  - Test all endpoints return correct status codes

  - Test request validation rejects invalid inputs
  - Test error handling for edge cases
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 9. Implement Frontend (Streamlit option)

  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ] 9.1 Create Streamlit application
  - Set up main app.py with page layout
  - Implement file uploader widget

  - Implement data preview display
  - Add session state management
  - _Requirements: 7.1, 7.2_

- [ ] 9.2 Implement solver controls
  - Add classical solver button with API integration
  - Add QAOA parameter sliders (reps, shots)
  - Add quantum solver button with API integration
  - Display loading states during execution
  - _Requirements: 7.3, 7.4_

- [ ] 9.3 Implement results display
  - Render route and cost information
  - Embed visualizations inline
  - Display comparison metrics
  - _Requirements: 7.5_

- [ ] 9.4 Write integration tests for frontend
  - Test file upload flow
  - Test solver invocation
  - Test results rendering
  - _Requirements: 7.1, 7.2, 7.3, 7.5_

- [ ] 10. Create sample dataset and demo script
  - Create sample supply_chain_data.csv with 5-8 locations
  - Create demo.py script that runs full pipeline
  - Add example outputs to docs/
  - _Requirements: 1.1, 10.5_

- [ ] 11. Checkpoint - Ensure all integration tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 12. Implement Docker containerization
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ] 12.1 Create Dockerfile for backend
  - Define Python 3.10 base image
  - Copy requirements.txt and install dependencies
  - Copy source code
  - Set CMD to run uvicorn
  - _Requirements: 8.1, 8.2_

- [ ] 12.2 Create docker-compose configuration
  - Define backend service
  - Define frontend service (if using React)
  - Configure networking and volumes
  - _Requirements: 8.3, 8.4_

- [ ] 12.3 Test Docker deployment
  - Build Docker image
  - Verify image size < 2GB
  - Test container startup
  - Test API accessibility
  - _Requirements: 8.1, 8.2, 8.4, 8.5_

- [ ] 13. Add comprehensive documentation
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 13.1 Complete README.md
  - Add project overview and architecture diagram
  - Add installation instructions
  - Add usage examples with exact commands
  - Add API endpoint documentation
  - _Requirements: 10.1, 10.2, 10.3, 10.5_

- [ ] 13.2 Add code documentation
  - Add docstrings to all public functions
  - Document function parameters and return values
  - Add usage examples in docstrings
  - _Requirements: 10.4_

- [ ] 13.3 Create additional documentation
  - Create CONTRIBUTING.md with development guidelines
  - Create API.md with detailed endpoint specs
  - Create ARCHITECTURE.md with system design
  - _Requirements: 10.2, 10.3_

- [ ] 14. Set up continuous integration
  - _Requirements: 9.5_

- [ ] 14.1 Create GitHub Actions workflow
  - Add linting job (flake8, black)
  - Add type checking job (mypy)
  - Add unit test job with coverage
  - Add property test job
  - Add Docker build job
  - _Requirements: 9.5_

- [ ] 15. Final checkpoint - Complete system validation
  - Run full end-to-end test: upload → preprocess → solve (classical & quantum) → visualize
  - Verify all tests pass
  - Verify Docker deployment works
  - Verify documentation is complete
  - Ensure all tests pass, ask the user if questions arise.
