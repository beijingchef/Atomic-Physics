from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
u=np.linspace(0,2,1601)
d=np.linspace(-10,10,2001)
amplitude=1/np.sqrt(1+d*d)
phase=np.arctan2(1.,-d)/np.pi
in_phase=-d/(1+d*d)
quadrature=1/(1+d*d)
fig,ax=plt.subplots(2,2,figsize=(10,7),layout='constrained')
ax[0,0].plot(d,amplitude,color='#176b78')
ax[0,1].plot(d,phase,color='#176b78')
ax[1,0].plot(d,in_phase,color='#3b6ea8')
ax[1,1].plot(d,quadrature,color='#b44832')
for a in ax.flat:
    a.set_xlabel(r'Detuning $\Delta/\gamma$');a.axvline(0,color='.7',ls=':',lw=1);a.grid(alpha=.16)
ax[0,0].set_ylabel(r'Dipole amplitude $p_0/p_{00}$')
ax[0,1].set_ylabel(r'Dipole phase lag $\delta_p/\pi$');ax[0,1].set_yticks([0,.5,1])
ax[1,0].set_ylabel(r'In-phase coefficient $p_{\parallel}/p_{00}$')
ax[1,1].set_ylabel(r'Quadrature coefficient $p_{\perp}/p_{00}$')
ax[1,0].axhline(0,color='.7',lw=1)
ax[1,1].axhline(0,color='.7',lw=1)
assert amplitude[1000]==1 and phase[1000]==.5
assert in_phase[1000]==0 and quadrature[1000]==1
assert abs((1/np.sqrt(1+1.**2))**2-.5)<1e-12
fig.savefig(root/'images/lorentz-resonance.svg')
fig.savefig(root/'images/lorentz-resonance.pdf')
plt.close(fig)
dopt=np.linspace(-10,10,2001)
index_shape=-dopt/(1+dopt*dopt)
absorption_shape=1/(1+dopt*dopt)
fig,ax=plt.subplots(1,2,figsize=(10,3.7),layout='constrained')
ax[0].plot(dopt,index_shape,color='#176b78');ax[0].axhline(0,color='.7',lw=1);ax[0].set_ylabel(r'Normalized index correction')
ax[1].plot(dopt,absorption_shape,color='#b44832');ax[1].set_ylabel(r'Normalized absorption $\sigma_{\rm abs}/\sigma_{\rm abs,res}$')
for a in ax:
    a.set_xlabel(r'Detuning $\Delta/\gamma$');a.axvline(0,color='.7',ls=':',lw=1);a.grid(alpha=.16)
assert np.all(absorption_shape>=0) and absorption_shape[1000]==1
fig.savefig(root/'images/dispersion-absorption.svg');plt.close(fig)
print('Plots created; resonance peaks and absorption sign verified.')
