"""Filter.sc"""

from .. import ugen as ugn
from .. import _graphparam as gpp

# Only for VarLag
from .. import env
from . import oscillators as ocl
from . import envgen as egn


class Filter(ugn.PureUGen):
    def _check_inputs(self):  # override
        return self._check_sr_as_first_input()


class Resonz(Filter):
    @classmethod
    def ar(cls, input=0.0, freq=440.0, bwr=1.0, mul=1.0, add=0.0):
        return cls._multi_new('audio', input, freq, bwr).madd(mul, add)

    @classmethod
    def kr(cls, input=0.0, freq=440.0, bwr=1.0, mul=1.0, add=0.0):
        return cls._multi_new('control', input, freq, bwr).madd(mul, add)


class OnePole(Filter):
    @classmethod
    def ar(cls, input=0.0, coef=0.5, mul=1.0, add=0.0):
        return cls._multi_new('audio', input, coef).madd(mul, add)

    @classmethod
    def kr(cls, input=0.0, coef=0.5, mul=1.0, add=0.0):
        return cls._multi_new('control', input, coef).madd(mul, add)


class OneZero(OnePole):
    pass


class TwoPole(Filter):
    @classmethod
    def ar(cls, input=0.0, freq=440.0, radius=0.8, mul=1.0, add=0.0):
        return cls._multi_new('audio', input, freq, radius).madd(mul, add)

    @classmethod
    def kr(cls, input=0.0, freq=440.0, radius=0.8, mul=1.0, add=0.0):
        return cls._multi_new('control', input, freq, radius).madd(mul, add)


class TwoZero(TwoPole):
    pass


class APF(TwoPole):
    pass


class Integrator(Filter):
    @classmethod
    def ar(cls, input=0.0, coef=1.0, mul=1.0, add=0.0):
        return cls._multi_new('audio', input, coef).madd(mul, add)

    @classmethod
    def kr(cls, input=0.0, coef=1.0, mul=1.0, add=0.0):
        return cls._multi_new('control', input, coef).madd(mul, add)


class Decay(Filter):
    @classmethod
    def ar(cls, input=0.0, decay_time=1.0, mul=1.0, add=0.0):
        return cls._multi_new('audio', input, decay_time).madd(mul, add)

    @classmethod
    def kr(cls, input=0.0, decay_time=1.0, mul=1.0, add=0.0):
        return cls._multi_new('control', input, decay_time).madd(mul, add)


class Decay2(Filter):
    @classmethod
    def ar(cls, input=0.0, attack_time=0.01, decay_time=1.0, mul=1.0, add=0.0):
        return cls._multi_new(
            'audio', input, attack_time, decay_time).madd(mul, add)

    @classmethod
    def kr(cls, input=0.0, attack_time=0.01, decay_time=1.0, mul=1.0, add=0.0):
        return cls._multi_new(
            'control', input, attack_time, decay_time).madd(mul, add)


class Lag(Filter):
    @classmethod
    def ar(cls, input=0.0, lag_time=0.1, mul=1.0, add=0.0):
        if gpp.ugen_param(input)._as_ugen_rate() == 'scalar' or lag_time == 0:
            return ugn.MulAdd.new(input, mul, add)
        else:
            return cls._multi_new('audio', input, lag_time).madd(mul, add)

    @classmethod
    def kr(cls, input=0.0, lag_time=0.1, mul=1.0, add=0.0):
        if gpp.ugen_param(input)._as_ugen_rate() == 'scalar' or lag_time == 0:
            return ugn.MulAdd.new(input, mul, add)
        else:
            return cls._multi_new('control', input, lag_time).madd(mul, add)


class Lag2(Lag):
    pass


class Lag3(Lag):
    pass


class Ramp(Lag):
    pass


class LagUD(Filter):
    @classmethod
    def ar(cls, input=0.0, lag_time_up=0.1, lag_time_down=0.1,
           mul=1.0, add=0.0):
        if gpp.ugen_para(input)._as_ugen_rate() == 'scalar':
            return ugn.MulAdd.new(input, mul, add)
        else:
            return cls._multi_new(
                'audio', input, lat_time_up, lag_time_down).madd(mul, add)

    @classmethod
    def kr(cls, input=0.0, lag_time_up=0.1, lag_time_down=0.1,
           mul=1.0, add=0.0):
        if gpp.ugen_para(input)._as_ugen_rate() == 'scalar':
            return ugn.MulAdd.new(input, mul, add)
        else:
            return cls._multi_new(
                'control', input, lat_time_up, lag_time_down).madd(mul, add)


class Lag2UD(LagUD):
    pass


class Lag3UD(LagUD):
    pass


class VarLag(Filter):
    @classmethod
    def ar(cls, input=0.0, time=0.1, curvature=0, warp=5, start=None,
           mul=1.0, add=0.0):
        if gpp.ugen_param(input)._as_ugen_rate() == 'scalar' or time == 0:
            return ugn.MulAdd.new(input, mul, add)
        else:
            return cls._multi_new(
                'audio', input, time, curvature, warp, start).madd(mul, add)

    @classmethod
    def kr(cls, input=0.0, time=0.1, curvature=0, warp=5, start=None,
           mul=1.0, add=0.0):
        if gpp.ugen_param(input)._as_ugen_rate() == 'scalar' or time == 0:
            return ugn.MulAdd.new(input, mul, add)
        else:
            return cls._multi_new(
                'control', input, time, curvature, warp, start).madd(mul, add)

    @classmethod
    def _new1(cls, rate, input, time, curvature, warp, start):   # *** BUG: TEST.
        # // FIXME: Implement 'curve' input on VLag ugen instead of using EnvGen.
        # // Then 'exp' warp should probably behave as Lag ugen.
        # NOTE: this provisory implementation is low level like in sclang.
        selector = 'ar' if rate == 'audio' else 'kr'
        start = start or input
        try:
            curve = env.Env._SHAPE_NAMES[warp]
        except KeyError:
            curve = warp
        if curve != 1:
            env = env.Env([start, input], [time], warp).envgen_format()
            env = list(env[0])
            env[6] = curve
            env[7] = curvature
            env = [tuple(env)]
            trig = getattr(Changed, selector)(input) +\
                   getattr(ocl.Impulse, selector)(0)
            if gpp.ugen_para(time)._as_ugen_rate() != 'scalar':
                trig += Changed.kr(time)
            return getattr(egn.EnvGen, selector)(env, trig)
        else:
            obj = cls()
            obj._rate = rate
            obj._add_to_synth()
            return obj._init_ugen(input, time, start)


class LeakDC(Filter):
    @classmethod
    def ar(cls, input=0.0, coef=0.995, mul=1.0, add=0.0):
        return cls._multi_new('audio', input, coef).madd(mul, add)

    @classmethod
    def kr(cls, input=0.0, coef=0.995, mul=1.0, add=0.0):
        return cls._multi_new('control', input, coef).madd(mul, add)


class RLPF(Filter):
    @classmethod
    def ar(cls, input=0.0, freq=440.0, rq=1.0, mul=1.0, add=0.0):
        return cls._multi_new('audio', input, freq, rq).madd(mul, add)

    @classmethod
    def kr(cls, input=0.0, freq=440.0, rq=1.0, mul=1.0, add=0.0):
        return cls._multi_new('control', input, freq, rq).madd(mul, add)


class RHPF(RLPF):
    pass


class LPF(Filter):
    @classmethod
    def ar(cls, input=0.0, freq=440.0, mul=1.0, add=0.0):
        return cls._multi_new('audio', input, freq).madd(mul, add)

    @classmethod
    def kr(cls, input=0.0, freq=440.0, mul=1.0, add=0.0):
        return cls._multi_new('control', input, freq).madd(mul, add)


class HPF(LPF):
    pass


class BPF(Filter):
    @classmethod
    def ar(cls, input=0.0, freq=440.0, rq=1.0, mul=1.0, add=0.0):
        return cls._multi_new('audio', input, freq, rq).madd(mul, add)

    @classmethod
    def kr(cls, input=0.0, freq=440.0, rq=1.0, mul=1.0, add=0.0):
        return cls._multi_new('control', input, freq, rq).madd(mul, add)


class BRF(BPF):
    pass


class MidEQ(Filter):
    @classmethod
    def ar(cls, input=0.0, freq=440.0, rq=1.0, db=0.0, mul=1.0, add=0.0):
        return cls._multi_new('audio', input, freq, rq, db).madd(mul, add)

    @classmethod
    def kr(cls, input=0.0, freq=440.0, rq=1.0, db=0.0, mul=1.0, add=0.0):
        return cls._multi_new('control', input, freq, rq, db).madd(mul, add)


class LPZ1(Filter):
    @classmethod
    def ar(cls, input=0.0, mul=1.0, add=0.0):
        return cls._multi_new('audio', input).madd(mul, add)

    @classmethod
    def kr(cls, input=0.0, mul=1.0, add=0.0):
        return cls._multi_new('control', input).madd(mul, add)


class HPZ1(LPZ1):
    pass


class Slope(Filter):
    @classmethod
    def ar(cls, input=0.0, mul=1.0, add=0.0):
        return cls._multi_new('audio', input).madd(mul, add)

    @classmethod
    def kr(cls, input=0.0, mul=1.0, add=0.0):
        return cls._multi_new('control', input).madd(mul, add)


class Changed(Filter):  # is pseudo really
    @classmethod
    def ar(cls, input, threshold=0):
        return HPZ1.ar(input).abs() > threshold

    @classmethod
    def kr(cls, input, threshold=0):
        return HPZ1.kr(input).abs() > threshold


class LPZ2(Filter):
    @classmethod
    def ar(cls, input=0.0, mul=1.0, add=0.0):
        return cls._multi_new('audio', input).madd(mul, add)

    @classmethod
    def kr(cls, input=0.0, mul=1.0, add=0.0):
        return cls._multi_new('control', input).madd(mul, add)


class HPZ2(LPZ2):
    pass


class BPZ2(LPZ2):
    pass


class BRZ2(LPZ2):
    pass


class Median(Filter):
    @classmethod
    def ar(cls, length=3, input=0.0, mul=1.0, add=0.0):
        return cls._multi_new('audio', length, input).madd(mul, add)

    @classmethod
    def kr(cls, length=3, input=0.0, mul=1.0, add=0.0):
        return cls._multi_new('control', length, input).madd(mul, add)

    def _check_inputs(self):
        if self.rate == 'audio'\
        and gpp.ugen_para(self.inputs[1])._as_ugen_rate() != 'audio':
            return 'input was not audio rate'
        else:
            return self._check_valid_inputs()


# Lost UGen AvgAbsAmp.


class Slew(Filter):
    @classmethod
    def ar(cls, input=0.0, up=1.0, dn=1.0, mul=1.0, add=0.0):
        if gpp.ugen_param(input)._as_ugen_rate() == 'scalar':
            return ugn.MulAdd.new(input, mul, add)
        else:
            return cls._multi_new('audio', input, up, dn).madd(mul, add)

    @classmethod
    def kr(cls, input=0.0, up=1.0, dn=1.0, mul=1.0, add=0.0):
        if gpp.ugen_param(input)._as_ugen_rate() == 'scalar':
            return ugn.MulAdd.new(input, mul, add)
        else:
            return cls._multi_new('control', input, up, dn).madd(mul, add)


# Lost UGen RLPF4.


class FOS(Filter):
    @classmethod
    def ar(cls, input=0.0, a0=0.0, a1=0.0, b1=0.0, mul=1.0, add=0.0):
        return cls._multi_new('audio', input, a0, a1, b1).madd(mul, add)

    @classmethod
    def kr(cls, input=0.0, a0=0.0, a1=0.0, b1=0.0, mul=1.0, add=0.0):
        return cls._multi_new('control', input, a0, a1, b1).madd(mul, add)


class SOS(Filter):
    @classmethod
    def ar(cls, input=0.0, a0=0.0, a1=0.0, a2=0.0, b1=0.0, b2=0.0,
           mul=1.0, add=0.0):
        return cls._multi_new(
            'audio', input, a0, a1, a2, b1, b2).madd(mul, add)

    @classmethod
    def kr(cls, input=0.0, a0=0.0, a1=0.0, a2=0.0, b1=0.0, b2=0.0,
           mul=1.0, add=0.0):
        return cls._multi_new(
            'control', input, a0, a1, a2, b1, b2).madd(mul, add)


class Ringz(Filter):
    @classmethod
    def ar(cls, input=0.0, freq=440.0, decay_time=1.0, mul=1.0, add=0.0):
        return cls._multi_new('audio', input, freq, decay_time).madd(mul, add)

    @classmethod
    def kr(cls, input=0.0, freq=440.0, decay_time=1.0, mul=1.0, add=0.0):
        return cls._multi_new('control', input, freq, decay_time).madd(mul, add)


class Formlet(Filter):
    @classmethod
    def ar(cls, input=0.0, freq=440.0, attack_time=1.0, decay_time=1.0,
           mul=1.0, add=0.0):
        return cls._multi_new(
            'audio', input, freq, attack_time, decay_time).madd(mul, add)

    @classmethod
    def kr(cls, input=0.0, freq=440.0, attack_time=1.0, decay_time=1.0,
           mul=1.0, add=0.0):
        return cls._multi_new(
            'control', input, freq, attack_time, decay_time).madd(mul, add)


# // the doneAction arg lets you cause the EnvGen to stop or end the
# // synth without having to use a PauseSelfWhenDone or FreeSelfWhenDone ugen.
# // It is more efficient to use a doneAction.
# // doneAction = 0   do nothing when the envelope has ended.
# // doneAction = 1   pause the synth running, it is still resident.
# // doneAction = 2   remove the synth and deallocate it.
# // doneAction = 3   remove and deallocate both this synth and the preceeding node.
# // doneAction = 4   remove and deallocate both this synth and the following node.
# // doneAction = 5   remove and deallocate this synth and free all children in the preceeding group (if it is a group).
# // doneAction = 6   remove and deallocate this synth and free all children in the following group (if it is a group).
class DetectSilence(Filter):
    @classmethod
    def ar(cls, input=0.0, amp=0.0001, time=0.1, done_action=0):
        return cls._multi_new('audio', input, amp, time, done_action)

    @classmethod
    def kr(cls, input=0.0, amp=0.0001, time=0.1, done_action=0):
        return cls._multi_new('control', input, amp, time, done_action)

    def _optimize_graph(self):
        pass


# Lost UGen FlagNaN.
