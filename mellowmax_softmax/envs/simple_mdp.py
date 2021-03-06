from typing import Optional, Union

import gym
from gym import logger
from gym import spaces
import numpy as np


class SimpleMDP(gym.Env):
    """
    ### Description

    This environment is a implementation of the simple MDP described by Kavosh Asadi and Michael L. Littman in
    ["An Alternative Softmax Operator for Reinforcement Learning"](https://arxiv.org/pdf/1612.05628.pdf)

    ### Action Space

    The action is a `ndarray` with shape `(1,)` which can take values `{0, 1}` indicating the
    action `a` and `b`.

    | Num | Action |
    |-----|--------|
    | 0   | a      |
    | 1   | b      |

    ### Observation Space

    The observation is a `ndarray` with shape `(1,)` which indicates the current state:

    | Num | Observation |
    |-----|-------------|
    | 0   | S1          |
    | 1   | S2          |

    ### Rewards

    Accoring to the description in the paper, the reward is `0.122` if the action is `a` and `0.033`
    if the action is `b`.

    | state | action | reward |
    |-------|--------|--------|
    | S1    | a      | 0.122  |
    | S1    | b      | 0.033  |

    ### Starting State

    Each episode will starts from S1.

    ### Episode Termination

    The episode terminates if it reachs S2.

    """

    def __init__(self):
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Discrete(2)

        self.state = None

        # S x A x S' -> R
        self.transition = np.array([[[0.66, 0.34], [0.99, 0.01]],
                                    [[0.0, 1.0], [0.0, 1.0]]])

        self.P = {
            0: {
                0: [(0.66, 0, 0.122, False), (0.34, 1, 0.122, True)],
                1: [(0.99, 0, 0.033, False), (0.01, 1, 0.033, True)]
            },
            1: {
                0: [(0, 0, 0, False), (1, 1, 0, True)],
                1: [(0, 0, 0, False), (1, 1, 0, True)]
            }
        }

        self.reward = np.array([[0.122, 0.033], [0.0, 0.0]])
        self.steps_beyond_done = None

    def step(self, action: Union[int, np.ndarray]):
        assert self.action_space.contains(action)
        assert self.state is not None, 'Call reset before using step method.'

        self.state = self.np_random.choice(
            2,
            p=self.transition[self.state, action, :],
        )
        reward = self.reward[self.state][action]

        done = self.state == 1

        if done:
            if self.steps_beyond_done is None:
                self.steps_beyond_done = 0
            else:
                if self.steps_beyond_done == 0:
                    logger.warn(
                        "You are calling 'step()' even though this "
                        "environment has already returned done = True. You "
                        "should always call 'reset()' once you receive 'done = "
                        "True' -- any further steps are undefined behavior.")
                self.steps_beyond_done += 1
                reward = 0.0

        return np.array(self.state, dtype=np.int32), reward, done, {}

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        return_info: bool = False,
        options: Optional[dict] = None,
    ):
        super().reset(seed=seed)
        self.state = 0
        self.steps_beyond_done = None

        if not return_info:
            return np.array(self.state, dtype=np.int32)

        return np.array(self.state, dtype=np.int32), {}

    def render(self, mode: str = 'human'):
        logger.warn("This environment doesn't support rendering.")
