# -*- coding: utf-8 -*-
""" CentralizedNotFair: a multi-player policy which uses a centralized intelligence to affect users to a FIXED arm.

- It allows to have absolutely *no* collision, if there is more channels than users (always assumed).
- But it is NOT fair on ONE run: the best arm is played only by one player.
- Note that in average, it is fair (who plays the best arm is randomly decided).
- Note that it is NOT affecting players on the best arms: it has no knowledge of the means of the arms, only of the number of arms nbArms.
"""
from __future__ import print_function

__author__ = "Lilian Besson"
__version__ = "0.1"

import numpy as np

from .ChildPointer import ChildPointer


class Fixed(object):
    """ Fixed: always select a fixed arm, as decided by the CentralizedNotFair multi-player policy.
    """

    def __init__(self, nbArms, armIndex):
        self.nbArms = nbArms
        self.armIndex = armIndex
        self.params = str(armIndex)

    def __str__(self):
        return "Fixed({})".format(self.params)

    def startGame(self):
        pass

    def getReward(self, arm, reward):
        pass

    def choice(self):
        return self.armIndex


class CentralizedNotFair(object):
    """ CentralizedNotFair: a multi-player policy which uses a centralized intelligence to affect users to a FIXED arm.
    """

    def __init__(self, nbPlayers, nbArms):
        """
        - nbPlayers: number of players to create (in self._players).
        - nbArms: number of arms.

        Examples:
        >>> s = CentralizedNotFair(10, 14)

        - To get a list of usable players, use s.childs.
        - Warning: s._players is for internal use
        """
        assert nbPlayers > 0, "Error, the parameter 'nbPlayers' for CentralizedNotFair class has to be > 0."
        if nbPlayers > nbArms:
            print("Warning, there is more users than arms ... (nbPlayers > nbArms)")  # XXX
        # Attributes
        self.nbPlayers = nbPlayers
        self.nbArms = nbArms
        # Internal vectorial memory
        if nbPlayers <= nbArms:
            self._affectations = np.random.choice(nbArms, size=nbPlayers, replace=False)
        else:
            self._affectations = np.zeros(nbPlayers, dtype=int)
            self._affectations[:nbArms] = np.random.choice(nbArms, size=nbArms, replace=False)
            # Try to minimize the number of doubled affectations, so all the other players are affected to the *same* arm
            # 1. first option : chose a random arm, put everyone else in it. Plus: minimize collisions, Minus: maybe it's a bad arm
            trashArm = np.random.choice(nbArms)
            # XXX this "trash" arm with max number of collision will not change: that can be very good (if it is the worse!) or very bad (if it is the best!)
            self._affectations[nbArms:] = trashArm
            # 2. second option : chose a random affectation. Plus: minimize risk, Minus: increase collisions
            # self._affectations[nbArms:] = np.random.choice(nbArms, size=nbPlayers - nbArms, replace=True)
        # Shuffle it once, just to be fair, IN AVERAGE (by repetitions)
        np.random.shuffle(self._affectations)
        print("CentralizedNotFair: initialized with {} arms and {} players ...".format(nbArms, nbPlayers))  # DEBUG
        print("It decided to use this affectation of arms :")  # DEBUG
        # Internal object memory
        self._players = [None] * nbPlayers
        self.childs = [None] * nbPlayers
        for playerId in range(nbPlayers):
            print(" - Player number {} will always choose the arm number {} ...".format(playerId + 1, self._affectations[playerId]))  # DEBUG
            self._players[playerId] = Fixed(nbArms, self._affectations[playerId])
            self.childs[playerId] = ChildPointer(self, playerId)
        self._printNbCollisions()  # DEBUG
        self.params = '{} x {}'.format(nbPlayers, str(self._players[0]))

    def __str__(self):
        return "CentralizedNotFair({})".format(self.params)

    def _printNbCollisions(self):
        """ Print number of collisions. """
        nbDifferentAffectation = len(set(self._affectations))
        if nbDifferentAffectation != self.nbPlayers:
            print("\n==> This affectation will bring collisions! Exactly {} at each step...".format(self.nbPlayers - nbDifferentAffectation + 1))
            for armId in range(self.nbArms):
                nbAffected = np.count_nonzero(self._affectations == armId)
                if nbAffected > 1:
                    print(" - For arm number {}, there is {} different child players affected on this arm ...".format(armId, nbAffected))

    def startGame(self):
        # XXX Not used right now!
        for player in self._players:
            player.startGame()

    def getReward(self, arm, reward):
        # XXX Not used right now!
        for player in self._players:
            player.getReward(arm, reward)()

    def choice(self):
        # XXX Not used right now!
        choices = np.zeros(self.nbPlayers)
        for i, player in enumerate(self._players):
            choices[i] = player.choice()
        return choices  # XXX What to do with this ?

    def _startGame_one(self, playerId):
        # FIXME It should re-generate the affectations every time a game is started!
        return self._players[playerId].startGame()

    def _getReward_one(self, playerId, arm, reward):
        return self._players[playerId].getReward(arm, reward)

    def _choice_one(self, playerId):
        return self._players[playerId].choice()