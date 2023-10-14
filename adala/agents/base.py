from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import Any, Optional, List
from adala.datasets.base import Dataset
from adala.skills.base import Experience, LongTermMemory

# following the protocol https://agentprotocol.ai/protocol


class AgentArtifact(BaseModel):
    """
    Base class for agent artifacts
    """
    pass


class AgentStep(BaseModel):
    """
    Base class for agent steps results
    """
    artifacts: List[AgentArtifact]
    is_last: bool


class Agent(BaseModel, ABC):
    """
    Base class for agents.
    """
    dataset: Dataset
    memory: Optional[LongTermMemory]

    @abstractmethod
    def step(self, learn=True) -> AgentStep:
        """
        Run agent step and return results
        If learn=False, agent will only act and not learn from environment
        """
