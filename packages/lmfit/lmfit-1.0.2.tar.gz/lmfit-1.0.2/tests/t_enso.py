from numpy import arctan, array, cos, exp, log, sin
from lmfit import Parameters, minimize, report_fit
from NISTModels import Models, ReadNistData

def read_params(params):
    if isinstance(params, Parameters):
        return [par.value for par in params.values()]
    else:
        return params


def ENSO(b, x, y=0):
    b = read_params(b)
    print("ENSO ", b)
    pi = 3.141592653589793238462643383279

    return y - b[0] + (b[1]*cos(2*pi*x/12)   + b[2]*sin(2*pi*x/12) +
                       b[4]*cos(2*pi*x/b[3]) + b[5]*sin(2*pi*x/b[3]) +
                       b[7]*cos(2*pi*x/b[6]) + b[8]*sin(2*pi*x/b[6]))

NISTdata = ReadNistData('ENSO')
resid, npar, dimx = Models['ENSO']
y = NISTdata['y']
x = NISTdata['x']
cert_values = NISTdata['cert_values']

resid_cert = ENSO(cert_values, x=x, y=y)
print("ENSO -> " , (resid_cert**2).sum())

print(NISTdata.keys())
params = Parameters()
for i in range(npar):
    pname = 'b%i' % (i+1)
    pval1 = NISTdata['start2'][i]
    params.add(pname, value=pval1)

myfit = minimize(resid, params, method='leastsq', args=(x,), kws={'y': y})
print(report_fit(myfit))
# digs, buff = Compare_NIST_Results(DataSet, myfit, myfit.params, NISTdata)
# print(buff)
