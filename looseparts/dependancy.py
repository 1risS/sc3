"""SCLang Object Dependancy"""


class Dependancy():
    dependants_dict = dict()

    def dependants(self):
        """Returns a set of all dependants of the receiver."""
        try:
            return Dependancy.dependants_dict[self]
        except KeyError:
            return set()

    def add_dependant(self, dependant):
        """Add a dependant to the receiver's list of dependants."""
        try:
            dependants = Dependancy.dependants_dict[self]
            dependants.add(dependant)
        except KeyError:
            dependants = set()
            dependants.add(dependant)
            Dependancy.dependants_dict[self] = dependants

    def remove_dependant(self, dependant):
        """Remove dependant from the receiver's list of dependants."""
        try:
            dependants = Dependancy.dependants_dict[self]
            dependants.remove(dependant)
            if len(dependants) == 0:
                del Dependancy.dependants_dict[self]
        except KeyError:
            pass # TODO: es comportamiento típico de sclang, no se si es correcto acá.

    def dependancy_changed(self, what, *args): # BUG: nombre chambiado de 'changed' para evitar posibles colisiones.
        """Notify the receiver's dependants that the receiver has changed.
        The object making the change should be passed as the changer."""
        if self not in Dependancy.dependants_dict:
            return # no es try porque llama a otros objetos.
        for item in Dependancy.dependants_dict[self].copy(): # RECORDAR: siempre que hace copy.do es porque la colección sobre la que itera puede ser alterada por las operaciones de la iteración.
            item.update_dependant(self, what, *args)

    # // respond to a change in a model
    def update_dependant(self, changed, changer, *args): # BUG: nombre cambiado de 'update' para evitar posibles colisiones.
        """An object upon which the receiver depends has changed.
        changed is the object that changed and changer is the object
        that made the change."""
        pass

    # release # BUG: este sería el método de interfaz y release_dependants sería privado en sclang, acá se usa solo el segundo como interfaz para evitar posibles colisiones.
    def release_dependats(self):
        """OD: Remove all dependants of the receiver. Any object that has
        had dependants added must be released in order for it or its
        dependants to get garbage collected."""
        try:
            del Dependancy.dependants_dict[self]
        except KeyError:
            pass # TODO: es comportamiento típico de sclang, no se si es correcto acá.


class SimpleController():
    def __init__(self, model):
        self.model = model
        self.model.add_dependant(self)
        self.actions = dict()

    def put(self, what, action):
        self.actions[what] = action

    def update(self, changer, what, *args):
        if len(self.actions) > 0 and what in self.actions:
            self.actions[what](changer, what, *args)

    def remove(self):
        self.model.remove_dependant(self)

    def remove_at(self, what):
        if len(self.actions) > 0 and what in self.actions:
            del self.actions[what]


# class TestDependant(): pass # BUG: no sé para qué es esta clase (está en Model.sc)
