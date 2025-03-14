
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler, Session
from dotenv import load_dotenv
import os

# Constantes et configuration
BACKEND_NAME = "ibm_brisbane"
OPTIMIZATION_LEVEL = 3

# Charger la clé API depuis .env
load_dotenv()
api_token = os.getenv("IBM_API_TOKEN")
if not api_token:
    print("Erreur: IBM_API_TOKEN manquant dans le fichier .env")
    exit(1)

try:
    service = QiskitRuntimeService(channel="ibm_quantum", token=api_token)
    backend = service.backend(BACKEND_NAME)
except Exception as e:
    print(f"Erreur de connexion à IBM Quantum: {e}")
    exit(1)

qc = QuantumCircuit(2)
qc.h(0)                # Porte Hadamard sur le qubit 0
qc.cx(0, 1)            # Porte CNOT avec qubit 0 comme contrôle et qubit 1 comme cible
qc.measure_all()       # Mesurer tous les qubits

# Transpiler le circuit pour le backend cible
try:
    transpiled_circuit = transpile(qc, backend=backend, optimization_level=OPTIMIZATION_LEVEL)
except Exception as e:
    print(f"Erreur lors de la transpilation: {e}")
    exit(1)

# Exécuter le circuit sur le backend
try:
    with Session(backend=backend) as session:
        sampler = Sampler(mode=session)
        job = sampler.run([transpiled_circuit])
        print(f"Job ID: {job.job_id()}")
except Exception as e:
    print(f"Erreur lors de l'exécution du circuit: {e}")
    exit(1)
