from typing import Dict

from src.entities.policy.dto import ConditionsDTO


Policy = Dict[str, Dict[str, Dict[str, ConditionsDTO]]]
