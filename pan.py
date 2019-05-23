"""Pan.sc"""

import supercollie.ugens as ugn


class Pan2(ugn.MultiOutUGen):
    @classmethod
    def ar(cls, input, pos=0.0, level=1.0):
        return cls.multi_new('audio', input, pos, level)

    @classmethod
    def kr(cls, input, pos=0.0, level=1.0):
        return cls.multi_new('control', input, pos, level)

    def init_ugen(self, *inputs):
        self.inputs = inputs
        self.channels = [
            ugn.OutputProxy.new(self.rate, self, 0),
            ugn.OutputProxy.new(self.rate, self, 1)
        ]
        return self.channels # NOTE: RECORDAR: las ugens retornan self en init_ugen que es método de interfaz, pero las output ugens retornan self.channels (o init_outputs que retorna self.channels)

    def check_inputs(self):
        return self.check_n_inputs(1)


# TODO: todo el resto...
