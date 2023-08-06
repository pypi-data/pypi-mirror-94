from podnuit.joueur import Joueur
from podnuit.victoire import Victoire
import random

class Jeu:
    """Jeu de loup-garou pas de nuit.
    """

    def __init__(self, roles=None):
        if roles is None:
            self.roles = ["tony", "pede", "loup-garou", "ble"]
        else:
            self.roles = roles
        self.joueurs = dict()
        self.votes = None
        self.n_votes = None
        self.target_n = None
        self.last_dead = None
        self.round_number = 0
        self._victory = None
        self.lock_vote = False
        self.game_state = "lobby"

    def setup(self, player_names, roles=None):
        """player_names is a dict: player_names[id] = display_name"""
        if roles is None:
            self.__init__(roles=self.roles)
        else:
            self.__init__(roles=roles)
        for name in player_names:
            if name in self.joueurs.keys():
                raise ValueError("Trying to add this player twice: {}".format(name))
            self.joueurs[name] = Joueur(name, player_names[name])
        self.set_roles()


    def get_game_state(self):
        return self.game_state

    def set_roles(self):
        names = self.get_alive_players()
        for r in self.roles:
            if r != "ble":
                chosen = random.choice(names)
                names.remove(chosen)
                self.joueurs[chosen].set_ident(r)
        for n in names:
            self.joueurs[n].set_ident("ble")

    def get_alive_players(self):
        """Getter for the list of alive players.

        Returns:
            list: The list of alive players (str names).
        """
        return [x for x in self.joueurs.keys() if self.joueurs[x].is_alive()]

    def remove_player(self, name):
        """Removes the player from the game by killing them (everybody votes for that player).
        """
        self.lock_vote = True
        for voter in self.votes:
            self.votes[voter] = name
        self.game_state = "just_voted"

    def start_round(self):
        """Has to be called at the beginning of each round.

        """
        self.game_state = "voting"
        self.round_number += 1
        self.votes = dict()
        for p in self.get_alive_players():
            self.votes[p] = ""
        self.n_votes = 0
        self.target_n = len(self.get_alive_players())
        self.lock_vote = False

    def vote(self, voter, voted):
        """Method for voting.

        Args:
            voter (str): The name of the player who is voting.
            voted (str): The name of the player against whom the voter votes.
        """
        if self.lock_vote:
            return
        assert voter in self.votes
        assert voted in self.votes
        if self.votes[voter] == "":
            self.votes[voter] = voted
            self.n_votes += 1
        else:
            self.votes[voter] = voted
        self.joueurs[voter].voted_for(voted)

    def vote_is_done(self):
        """Tells the server when voting is done.

        Returns:
            bool: True if everyone has voted.
        """
        if self.n_votes == self.target_n:
            self.game_state = "just_voted"
            return True
        return False


    def get_dead_folk(self):
        """When voting is finished, determines dead person(s).

        Returns:
            list: A list of dead player(s) as instances of the Joueur class.
        """
        if not self.vote_is_done():
            raise ValueError("get_dead_folk() called while voting still going on")
        dead = dict()
        for vote in self.votes.values():
            if vote in dead:
                dead[vote] += 1
            else:
                dead[vote] = 1
        max = 0
        for n in dead.values():
            if n > max:
                max = n
        dead_folk = []
        for d in dead:
            if dead[d] == max:
                dead_folk.append(self.joueurs[d])
                self.joueurs[d].kill(self.round_number)
        self.last_dead = dead_folk
        return dead_folk

    def game_is_done(self):
        """Determines if the game is finished.

        Returns:
            bool: True if the game is finished.
        """
        alive_players = self.get_alive_players()
        identities = set()
        for p in alive_players:
            identities.add(self.joueurs[p].get_ident())
        if len(alive_players) <= 2:
            if "loup-garou" in identities:
                if "pede" in identities:
                    self._victory = Victoire("pede", alive_players, self.joueurs)
                else:
                    self._victory = Victoire("loup-garou", alive_players, self.joueurs)
                return True
        if "loup-garou" not in identities:
            self._victory = Victoire("ble", alive_players, self.joueurs)
            return True
        if "tony" not in identities and self.round_number == 1:
            self._victory = Victoire("tony", alive_players, self.joueurs)
            self.game_state = "victory"
            return True
        return False

    def get_victory(self):
        if self._victory is not None:
            return self._victory
        raise ValueError("get_victory() called before victory achieved")

    def restart_game(self):
        self.__init__(self.roles)


if __name__ == "__main__":
    test = Jeu()
    test.setup(["Ben", "Etienne", "Méthieu", "Tony"])
    print(test.get_alive_players())
    for j in test.joueurs.values():
        print(j.get_ident(), j.get_name())
    for killed in ["Tony", "Méthieu"]:
        test.start_round()
        print(test.round_number)
        if "Ben" in set(test.get_alive_players()): test.vote("Ben", killed)
        if "Etienne" in set(test.get_alive_players()): test.vote("Etienne", killed)
        if "Méthieu" in set(test.get_alive_players()): test.vote("Méthieu", killed)
        if "Tony" in set(test.get_alive_players()): test.vote("Tony", killed)
        print(test.vote_is_done())
        print(test.get_dead_folk())
        if test.game_is_done():
            v = test.get_victory()
            print(v.message, v.gagnants)
