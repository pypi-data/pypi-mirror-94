class Joueur:
    def __init__(self, name, display_name):
        self._name = name
        self._display_name = display_name
        self._ident = None
        self._alive = True
        self._death_round = 0
        self._voted_for = "N/A"
        self._n_votes_for = 0

    def get_name(self):
        return self._name

    def set_n_votes_for(self, n):
        self._n_votes_for = n

    def get_ident(self):
        return self._ident

    def set_ident(self, ident):
        if self._ident is not None:
            raise ValueError("Trying to set identity twice for this player: {}".format(self._name))
        self._ident = ident

    def reset(self):
        self._ident = None
        self._alive = True
        self._death_round = 0
        self._voted_for = "N/A"

    def voted_for(self, voted):
        self._voted_for = voted

    def is_alive(self):
        return self._alive

    def serialize(self):
        return {"display_name": self._display_name,
                "is_alive": self._alive,
                "ident": self._ident,
                "death_round": self._death_round,
                "voted_for": self._voted_for,
                "n_votes_for": self._n_votes_for}

    def kill(self, round_number):
        if not self._alive:
            raise ValueError("Trying to kill already dead player: {}".format(self._name))
        self._alive = False