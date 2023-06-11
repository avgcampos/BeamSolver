import sympy as sb
import numpy as np
import matplotlib.pyplot as plt
import sys

L = 1.0
EI = 1.0

x = sb.Symbol('x')
C0 = sb.Symbol('C0')
C1 = sb.Symbol('C1')
C2 = sb.Symbol('C2')
C3 = sb.Symbol('C3')

xx = np.linspace(0, L, 500)

l1 = {
    'type': 'apply', # remove, suport
    'order': 0,
    'value': -1.0,
    'begin': 0.0
    }

l2 = {
    'type': 'remove', # rem, sup
    'order': 0,
    'value': 1.0,
    'begin': 0.5*L
    }

l3 = {
    'type': 'apply', # rem, sup
    'order': 0,
    'value': -4.0,
    'begin': 0.75*L
    }

r1 = {
    'type': 'support',
    'order': 0,
    'value': 'R1y',
    'begin':0.25*L
}

r2 = {
    'type': 'support',
    'order': 0,
    'value': 'R2y',
    'begin':0.75*L
}

bc1 = {
    'begin': 0, # 'L'
    'dof': 'v',
    'value': 0,
    }


bc2 = {
    'begin': 0, # 'L'
    'dof': 's',
    'value': 0,
    }

bc3 = {
    'begin': L, # 'L'
    'dof': 'v',
    'value': 0,
    }

bc4 = {
    'begin': L, # 'L'
    'dof': 's',
    'value': 0,
    }

rs1 = {
    'type': 'X', # 'L'
    'dof': 'v',
    'value': 0,
    'begin': 0.25,
    }

rs2 = {
    'type': 'X', # 'L'
    'dof': 'v',
    'value': 0,
    'begin': 0.75,
    }


load_list = [l1]

bc_list = [bc1, bc2, bc3, bc4]


load = []
support = []
for itl in range(len(load_list)):
    if load_list[itl]['type'] == 'apply':
        load.append(+load_list[itl]['value']*sb.SingularityFunction(x, load_list[itl]['begin'], load_list[itl]['order']))

    elif load_list[itl]['type'] == 'remove':
        if np.sign(load_list[itl]['value']) == 1:
            load.append('+')
            load.append(load_list[itl]['value']*sb.SingularityFunction(x, load_list[itl]['begin'], load_list[itl]['order']))
        else:
            load.append(load_list[itl]['value']*sb.SingularityFunction(x, load_list[itl]['begin'], load_list[itl]['order']))
        
    elif load_list[itl]['type'] == 'support':
        sup_sym = sb.Symbol(load_list[itl]['value'])
        support.append(load_list[itl]['value'])
        load.append('+')
        # load.append(load_list[itl]['value'])
        load.append(sup_sym*sb.SingularityFunction(x, load_list[itl]['begin'], load_list[itl]['order']))
    
    else:
        pass

load_str = ' '.join(str(e) for e in load)
load_sympy = sb.parsing.sympy_parser.parse_expr(load_str)

support_cons = ', '.join(str(e) for e in support)
# support_sympy = sb.parsing.sympy_parser.parse_expr(support_cons)


# print(load_sympy)
print(support_cons)

# sys.exit()

# 

load_piecewise = load_sympy.rewrite(sb.Piecewise)
load_vector = sb.lambdify(x, load_piecewise, "numpy")

# # print(load_vector(xx))

# plt.figure()
# plt.plot(xx,load_vector(xx))
# plt.grid('on')
# plt.show()

V = sb.integrate(load_sympy, x) + C0
M = sb.integrate(V, x) + C1
s = sb.integrate(M, x) + C2
v = sb.integrate(s, x) + C3

# print(V)
# print(M)
# print(s)
# print(v)



eqbc = []
for itbc in range(len(bc_list)):
    # bc1 = {
    # 'type': '0', # 'L'
    # 'dof': 'v',
    # 'value': 0,
    # }
    # if bc_list[itbc]['type'] == '0':
        # dof = sb.parsing.sympy_parser.parse_expr(bc_list[itbc]['dof'])
    #     if bc_list[itbc]['dof'] == 'V':
    #         eqbc.append(V.subs(x, 0) - bc_list[itbc]['value'])
    #     elif bc_list[itbc]['dof'] == 'M':
    #         eqbc.append(M.subs(x, 0) - bc_list[itbc]['value'])
    #     elif bc_list[itbc]['dof'] == 's':
    #         eqbc.append(s.subs(x, 0) - bc_list[itbc]['value'])
    #     elif bc_list[itbc]['dof'] == 'v':
    #         eqbc.append(v.subs(x, 0) - bc_list[itbc]['value'])
    
    # elif bc_list[itbc]['type'] == 'L':
    #     # dof = sb.parsing.sympy_parser.parse_expr(bc_list[itbc]['dof'])
    #     if bc_list[itbc]['dof'] == 'V':
    #         eqbc.append(V.subs(x, L) - bc_list[itbc]['value'])
    #     elif bc_list[itbc]['dof'] == 'M':
    #         eqbc.append(M.subs(x, L) - bc_list[itbc]['value'])
    #     elif bc_list[itbc]['dof'] == 's':
    #         eqbc.append(s.subs(x, L) - bc_list[itbc]['value'])
    #     elif bc_list[itbc]['dof'] == 'v':
    #         eqbc.append(v.subs(x, L) - bc_list[itbc]['value'])
            
    # elif bc_list[itbc]['type'] == 'X':
        
    if bc_list[itbc]['dof'] == 'V':
        eqbc.append(V.subs(x, bc_list[itbc]['begin']) - bc_list[itbc]['value'])
    
    elif bc_list[itbc]['dof'] == 'M':
        eqbc.append(M.subs(x, bc_list[itbc]['begin']) - bc_list[itbc]['value'])
    
    elif bc_list[itbc]['dof'] == 's':
        eqbc.append(s.subs(x, bc_list[itbc]['begin']) - bc_list[itbc]['value'])
    
    elif bc_list[itbc]['dof'] == 'v':
        eqbc.append(v.subs(x, bc_list[itbc]['begin']) - bc_list[itbc]['value'])

print(eqbc)



symbols = sb.symbols('C0, C1, C2, C3, '+support_cons)

print(symbols)



sol = sb.linsolve(eqbc, symbols)
const_val = list(sol)[0]
print(const_val)

print(support)

# sys.exit()

# const = {}

# const['C0'] = const_val[0]
# const['C1'] = const_val[1]
# const['C2'] = const_val[2]
# const['C3'] = const_val[3]
# const[support]

ss_str = []
for e in symbols: ss_str.append(str(e))
const = dict(zip(ss_str, list(const_val)))

# fruits = ["Apple", "Pear", "Peach", "Banana"]
# prices = [0.35, 0.40, 0.40, 0.28]
# fruit_dictionary = dict(zip(fruits, prices))
# {'Apple': 0.35, 'Pear': 0.4, 'Peach': 0.4, 'Banana': 0.28}
# for i in my_list:
#   final_string.append(str(i))


# print(const)

# sys.exit()

V_array = (V.subs(const)).rewrite(sb.Piecewise)
M_array = (M.subs(const)).rewrite(sb.Piecewise)
s_array = (1/EI*s.subs(const)).rewrite(sb.Piecewise)
v_array = (1/EI*v.subs(const)).rewrite(sb.Piecewise)

# print(V_array)
# print(M_array)
# print(s_array)
# print(v_array)

# sys.exit()

V_array_numpy = ((sb.lambdify(x, V_array, "numpy"))(xx))*np.ones_like(xx)
M_array_numpy = ((sb.lambdify(x, M_array, "numpy"))(xx))*np.ones_like(xx)
s_array_numpy = ((sb.lambdify(x, s_array, "numpy"))(xx))*np.ones_like(xx)
v_array_numpy = ((sb.lambdify(x, v_array, "numpy"))(xx))*np.ones_like(xx)


plt.close('all')
plt.figure()
plt.subplot(411)
plt.plot(xx,V_array_numpy,'g')
plt.grid('on')
plt.subplot(412)
plt.plot(xx,M_array_numpy,'b')
plt.grid('on')
plt.subplot(413)
plt.plot(xx,s_array_numpy,'m')
plt.grid('on')
plt.subplot(414)
plt.plot(xx,v_array_numpy,'k')
plt.grid('on')
plt.show()