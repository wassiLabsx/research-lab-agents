# -*- coding: utf-8 -*-
"""
Instances partagees de l'application : un seul bus, un seul agent MIS,
crees une fois et reutilises partout (main.py, routers...).
"""
from app.agents.mis_agent import MISAgent
from app.core.event_bus import InMemoryEventBus

event_bus = InMemoryEventBus()
mis_agent = MISAgent(name="mis", event_bus=event_bus)