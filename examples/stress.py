# BeamSolver Examples
# ---------------------------------------------------
# Ex: 01: Viga bi-apoiada c/ carga distribuida
# Antonio Campos 2023
#
#      |vvvvvvvvvvvvvvvvvvvvvvvvvvv| q(x) = -1 [N/mm]
#       ___________________________
#      /\                         /\
#      @x = 0                      @x = L = 1000 [mm]
#
# E = 200E3 [MPa]
# I = 65E6  [mm4]
# ---------------------------------------------------

# importe NewBeam e BeamEB 
from beamsolver.beam import NewBeam, BeamEB

# importacoes adicionais
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# configure uma nova viga com BeamEB
beam = NewBeam(BeamEB)

# parametros da viga, utilize unidades consistentes
H = 100   # altura retangulo
B = 50    # largura
L = 2000  # comprimento
E = 200E3 # modulo de elasticidade
I = (B*H**3)/12  # momento de inercia da secao Izz

beam.length(L)
beam.EI(E, I)

# crie um vetor numpy array para validar os resultados
x = np.linspace(0, L, 500)

# definicao da carga 1 --> P<x - a>**n
load_1 = {
    'type': 'apply', # tipo de forca, neste caso é aplicada na viga ou forca externa
    'order': -1,      # ordem (n) da interpolacao 
    'value': -1000.0,  # valor da forca (P), o sinal define a direcao, para baixo negativo
    'begin': L/3   # inicio de ativacao da forca (a)
}

load_2 = {
    'type': 'apply', # tipo de forca, neste caso é aplicada na viga ou forca externa
    'order': -1,      # ordem (n) da interpolacao 
    'value': -1000.0,  # valor da forca (P), o sinal define a direcao, para baixo negativo
    'begin': 2*L/3   # inicio de ativacao da forca (a)
}

# definicao das condicoes de contorno 
bc_1 = {
    'dof': 'v',      # tipo de grau de liberdade esta restrito
    'begin': 0,      # posicao da restricao
    'value': 0.0,    # valor do dof no ponto, pode ser diferente de zero
}

bc_2 = {
    'dof': 'M',
    'begin': 0,
    'value': 0.0,
}

bc_3 = {
    'dof': 'v',
    'begin': L,
    'value': 0.0,
}

bc_4 = {
    'dof': 'M',
    'begin': L,
    'value': 0.0,
}

# adicao da lista de cargas na formulacao da viga
beam.load([load_1, load_2])

# adicao da lista de condicoes de fronteira na formulacao da viga
beam.bc([bc_1, bc_2, bc_3, bc_4])

# verificacao da forca
get_load = beam.getload()
print(get_load)

# integracao dos parametros
beam.shear()        # esforco cortante
beam.bending()      # momento fletor
beam.slope()        # rotacao da secao
beam.displacement() # deslocamento vertical

# definicao das equacoes de restricao (das condicoes de fronteira) para o solucionador
constraeq = beam.constraint()

# obtencao da solucao e variaveis de integracao
beam.linsolve(constraeq)

# validacao numerica das variaveis de integracao
print(beam.getshear())

# validacao numerica dos esforcos e cinematica da viga
beam_shear = beam.getshear_array(x)
beam_bending = beam.getbending_array(x)
beam_slope = beam.getslope_array(x)
beam_displ = beam.getdisplacement_array(x)

# plot dos resultados
plt.close('all')
plt.figure()
plt.subplot(211)
plt.title('Esforço Cortante')
plt.plot(x,beam_shear,'g')
plt.grid('on')
plt.subplot(212)
plt.title('Momento Fletor')
plt.plot(x,beam_bending,'b')
plt.grid('on')
# plt.subplot(413)
# plt.title('Rotação')
# plt.plot(x,beam_slope,'m')
# plt.grid('on')
# plt.subplot(414)
# plt.title('Deslocamento')
# plt.plot(x,beam_displ,'k')
# plt.grid('on')
# plt.show()

# Stress
beam.thick(H/2, -H/2)
beam.width(B)
X, Y, SXX = beam.stressxx(beam_bending)

SXY = (6*beam_shear)/(B*H**3)*((H**2)/4 - Y**2) # shear stress na secao retangular
        
C = SXX/2
R = np.sqrt((SXX/2)**2 + SXY**2)

S1 = C + R
S2 = C - R
S_xy_max = np.abs(R)

arg = np.divide(SXY, R, out=np.zeros_like(SXY), where=R!=0)
theta_p = np.rad2deg((np.arcsin(arg))/2)
        
plt.figure(2)
plt.contourf(X, Y, SXX, levels=20,cmap=cm.jet)
cbar = plt.colorbar()
cbar.set_label('Tensão Normal SXX')
plt.show()

plt.figure(3)
plt.contourf(X, Y, SXY, levels=20,cmap=cm.jet)
cbar = plt.colorbar()
cbar.set_label('Tensão Cisalhante SXY')
plt.show()

plt.figure(4)
plt.contour(X, Y, S1, levels=10,cmap=cm.jet)
plt.grid('on')
cbar = plt.colorbar()
cbar.set_label('Tensão Principal S1')
plt.show()

plt.figure(5)
plt.contour(X, Y, S2, levels=10,cmap=cm.jet)
cbar = plt.colorbar()
cbar.set_label('Tensão Principal S2')
plt.show()

plt.figure(6)
plt.contour(X, Y, S_xy_max, levels=10,cmap=cm.jet)
plt.grid('on')
cbar = plt.colorbar()
cbar.set_label('Tensão Cisalhante Máxima')
plt.show()

plt.figure(7)
plt.contourf(X, Y, theta_p, levels=6,cmap=cm.jet)
plt.grid('on')
cbar = plt.colorbar()
cbar.set_label('Plano Principal de S1')
plt.show()