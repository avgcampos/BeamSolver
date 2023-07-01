# BeamSolver Examples
# ---------------------------------------------------
# Ex: 06: Viga engastada e apoiada c/ carga distribuida e concentrada
# Antonio Campos 2023
#
#       |vvvvvvvvvvvvvvvvvvvvvvvv|    q(x) =  -1 [N/mm] + R1y(= ?) [N @ x = 0.75L]
#     xx|_________________________
#     xx|                  /\
#      @x = 0                      @x = L = 1000 [mm]
#
# E = 200E3 [MPa]
# I = 65E6  [mm4]
# ---------------------------------------------------

# importe NewBeam e BeamEB 
from beamsolver import NewBeam, BeamEB

# importacoes adicionais
import numpy as np
import matplotlib.pyplot as plt

# configure uma nova viga com BeamEB
beam = NewBeam(BeamEB)

# parametros da viga, utilize unidades consistentes
L = 1000  # comprimento
E = 200E3 # modulo de elasticidade
I = 65E6  # momento de inercia da secao Izz

beam.length(L)
beam.EI(E, I)

# crie um vetor numpy array para validar os resultados
x = np.linspace(0, L, 500)

# definicao da carga 1 --> P<x - a>**n
load_1 = {
    'type': 'apply', # tipo de forca, neste caso é aplicada na viga ou forca externa
    'order': 0,      # ordem (n) da interpolacao 
    'value': -1.0,  # valor da forca (P), o sinal define a direcao, para baixo negativo
    'begin': 0.0*L   # inicio de ativacao da forca (a)
}

apoio_1 = {
    'type': 'support', # tipo de forca, neste caso é um suporte
    'order': -1,      # ordem (n) da interpolacao 
    'value': 'R1y',  # valor da forca (P), o sinal define a direcao, para baixo negativo
    'begin': 0.75*L   # inicio de ativacao da forca (a)
}

# definicao das condicoes de contorno 
bc_1 = {
    'dof': 'v',      # tipo de grau de liberdade esta restrito
    'begin': 0,      # posicao da restricao
    'value': 0.0,    # valor do dof no ponto, pode ser diferente de zero
}

bc_2 = {
    'dof': 's',
    'begin': 0,
    'value': 0.0,
}

bc_3 = {
    'dof': 'V',
    'begin': L,
    'value': 0.0,
}

bc_4 = {
    'dof': 'M',
    'begin': L,
    'value': 0.0,
}

restricao_apoio = {
    'dof': 'v',
    'begin': 0.75*L,
    'value': 0.0,
}

# adicao da lista de cargas na formulacao da viga
beam.load([load_1, apoio_1])

# adicao da lista de condicoes de fronteira na formulacao da viga
beam.bc([bc_1, bc_2, bc_3, bc_4, restricao_apoio])

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
solution = beam.linsolve(constraeq)

# valor da forca no apoio
print(solution['R1y'])

# validacao numerica das variaveis de integracao
beam.eval_constant(solution)

# validacao numerica dos esforcos e cinematica da viga
beam_shear = beam.getshear_array(x)
beam_bending = beam.getbending_array(x)
beam_slope = beam.getslope_array(x)
beam_displ = beam.getdisplacement_array(x)

# plot dos resultados
plt.close('all')
plt.figure()
plt.subplot(411)
plt.title('Cortante')
plt.plot(x,beam_shear,'g')
plt.grid('on')
plt.subplot(412)
plt.title('Momento')
plt.plot(x,beam_bending,'b')
plt.grid('on')
plt.subplot(413)
plt.title('Rotação')
plt.plot(x,beam_slope,'m')
plt.grid('on')
plt.subplot(414)
plt.title('Deslocamento')
plt.plot(x,beam_displ,'k')
plt.grid('on')
plt.show()