"""
Instances partagees de l'application : un seul bus, un seul agent MIS,
un seul Orchestrateur, crees une fois et reutilises partout.
"""
from app.agents.mis_agent import MISAgent
from app.agents.orchestrateur_agent import OrchestratorAgent
from app.core.event_bus import InMemoryEventBus

event_bus = InMemoryEventBus()
mis_agent = MISAgent(name="mis", event_bus=event_bus)
orchestrator_agent = OrchestratorAgent(name="orchestrateur", event_bus=event_bus)