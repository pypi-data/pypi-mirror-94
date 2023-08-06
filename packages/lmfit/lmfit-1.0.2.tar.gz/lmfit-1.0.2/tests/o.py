import lmfit
import numpy as np
mod = lmfit.models.SineModel()
x = np.linspace(-10, 10, 201)
pars = dict(amplitude=1.5, frequency=0.5, shift=0.4)

y = pars['amplitude']*np.sin(x*pars['frequency'] + pars['shift'])

params = mod.guess(y, x=x)

print(params)
