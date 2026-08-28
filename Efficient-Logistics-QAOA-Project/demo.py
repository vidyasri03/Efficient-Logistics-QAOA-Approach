"""Complete demo script for Efficient Logistics Scheduling.

This script demonstrates the full pipeline: preprocessing, QUBO building,
classical solving, quantum solving, and visualization.
"""

import numpy as np
from pathlib import Path
import sys

print("=" * 70)
print(" " * 15 + "EFFICIENT LOGISTICS SCHEDULING")
print(" " * 10 + "Quantum-Enhanced Supply Chain Optimization")
print("=" * 70)
print()

# Step 1: Preprocessing
print("📊 STEP 1: Data Preprocessing")
print("-" * 70)

from src.preprocessing.preprocess import preprocess_pipeline

try:
    matrix, names, mapping = preprocess_pipeline(
        "data/supply_chain_data.csv",
        "data/instance_small.csv",
        max_nodes=6  # Small instance for demo
    )
    
    print(f"✓ Loaded and preprocessed {len(names)} locations")
    print(f"✓ Cost matrix shape: {matrix.shape}")
    print(f"✓ Locations: {', '.join(names)}")
    print()
    
except Exception as e:
    print(f"✗ Preprocessing failed: {e}")
    sys.exit(1)

# Step 2: QUBO Building
print("🔢 STEP 2: QUBO Formulation")
print("-" * 70)

from src.qubo.qubo_builder import build_tsp_qubo, validate_qubo

try:
    Q = build_tsp_qubo(matrix, penalty_A=500, penalty_B=500)
    
    print(f"✓ Built QUBO matrix: {Q.shape}")
    print(f"✓ Number of variables: {Q.shape[0]}")
    
    if validate_qubo(Q):
        print(f"✓ QUBO validation passed")
    else:
        print(f"✗ QUBO validation failed")
        sys.exit(1)
    
    print()
    
except Exception as e:
    print(f"✗ QUBO building failed: {e}")
    sys.exit(1)

# Step 3: Classical Solving
print("🏛️  STEP 3: Classical Optimization (OR-Tools)")
print("-" * 70)

from src.classical.ortools_solver import solve_tsp, calculate_route_cost

try:
    classical_result = solve_tsp(matrix, time_limit_seconds=30)
    
    if classical_result['status'] in ['OPTIMAL', 'FEASIBLE']:
        print(f"✓ Status: {classical_result['status']}")
        print(f"✓ Total cost: {classical_result['cost']:.2f}")
        print(f"✓ Solve time: {classical_result['solve_time']:.2f}s")
        print(f"✓ Route: {' → '.join([names[i] for i in classical_result['route']])}")
        
        # Verify cost
        verified_cost = calculate_route_cost(classical_result['route'], matrix)
        print(f"✓ Verified cost: {verified_cost:.2f}")
        print()
    else:
        print(f"✗ Classical solver failed: {classical_result['status']}")
        sys.exit(1)
    
except Exception as e:
    print(f"✗ Classical solving failed: {e}")
    sys.exit(1)

# Step 4: Quantum Solving
print("⚛️  STEP 4: Quantum Optimization (QAOA)")
print("-" * 70)

from src.quantum.qiskit_qaoa import run_qaoa, decode_qaoa_solution

try:
    print("Running QAOA with circuit depth p=1...")
    quantum_result = run_qaoa(Q, reps=1, shots=1024)
    
    if quantum_result['success']:
        decoded = decode_qaoa_solution(quantum_result['solution'], len(names))
        
        print(f"✓ QAOA completed successfully")
        print(f"✓ Total cost: {quantum_result['cost']:.2f}")
        print(f"✓ Execution time: {quantum_result['execution_time']:.2f}s")
        print(f"✓ Circuit depth: {quantum_result['circuit_depth']}")
        print(f"✓ Solution valid: {decoded['is_valid']}")
        
        if decoded['is_valid']:
            print(f"✓ Route: {' → '.join([names[i] for i in decoded['route']])}")
        else:
            print(f"⚠ Constraint violations: {decoded['constraint_violations']}")
        
        print()
    else:
        print(f"✗ QAOA failed")
        print()
    
except Exception as e:
    print(f"✗ Quantum solving failed: {e}")
    print()

# Step 5: Visualization
print("📊 STEP 5: Visualization Generation")
print("-" * 70)

from src.viz.plots import (
    plot_cost_heatmap,
    plot_route_graph,
    plot_comparison_bar
)

try:
    # Create results directory
    Path("results").mkdir(exist_ok=True)
    
    # Generate heatmap
    plot_cost_heatmap(matrix, names, "results/cost_heatmap.png")
    print("✓ Generated cost heatmap")
    
    # Generate route graph
    plot_route_graph(
        classical_result['route'],
        names,
        matrix,
        "results/route_graph.png"
    )
    print("✓ Generated route graph")
    
    # Generate comparison
    if quantum_result['success']:
        plot_comparison_bar(
            classical_result['cost'],
            quantum_result['cost'],
            "results/comparison.png",
            classical_result['solve_time'],
            quantum_result['execution_time']
        )
        print("✓ Generated comparison chart")
    
    print()
    
except Exception as e:
    print(f"✗ Visualization failed: {e}")
    print()

# Step 6: Summary
print("📈 SUMMARY")
print("=" * 70)

print("\n🏛️  Classical Solver (OR-Tools):")
print(f"   Cost: {classical_result['cost']:.2f}")
print(f"   Time: {classical_result['solve_time']:.2f}s")
print(f"   Status: {classical_result['status']}")

if quantum_result['success']:
    print("\n⚛️  Quantum Solver (QAOA):")
    print(f"   Cost: {quantum_result['cost']:.2f}")
    print(f"   Time: {quantum_result['execution_time']:.2f}s")
    print(f"   Valid: {decoded['is_valid']}")
    
    print("\n⚖️  Comparison:")
    cost_diff = quantum_result['cost'] - classical_result['cost']
    cost_ratio = (cost_diff / classical_result['cost']) * 100
    
    if cost_diff < 0:
        print(f"   🎉 Quantum solver found a {abs(cost_ratio):.1f}% better solution!")
    elif abs(cost_ratio) < 5:
        print(f"   📊 Solutions are comparable (within 5%)")
    else:
        print(f"   📊 Classical solver performed {cost_ratio:.1f}% better")
    
    time_ratio = quantum_result['execution_time'] / classical_result['solve_time']
    print(f"   ⏱️  Quantum solver took {time_ratio:.1f}x longer")

print("\n📁 Output Files:")
print("   - results/cost_heatmap.png")
print("   - results/route_graph.png")
if quantum_result['success']:
    print("   - results/comparison.png")

print("\n" + "=" * 70)
print("✓ Demo completed successfully!")
print("\nNext steps:")
print("  1. View visualizations in the results/ directory")
print("  2. Run the Streamlit app: streamlit run frontend/streamlit_app.py")
print("  3. Start the API server: uvicorn src.api.main:app --reload")
print("=" * 70)
