# BeamSolver Examples
# ---------------------------------------------------
# Ex: 01: Viga bi-apoiada c/ carga concentrada 
# Antonio Campos 2023
#
#                               v/->>     q(x) =  0 | V(x = L) = +100 e M(x = L) = +100
#    xx|_________________________|
#    xx|                         
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
    'value': 100.0,
}

bc_4 = {
    'dof': 'M',
    'begin': L,
    'value': 100.0,
}

# adicao da lista de cargas na formulacao da viga
# beam.load([load_1, load_2])

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
solution = beam.linsolve(constraeq)

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