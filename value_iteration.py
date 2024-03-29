import numpy as np 
import matplotlib
import matplotlib.pyplot as plt
from gamblers_problem import GP

def value_iteration(env, discount_factor=1.0, epsilon=0.0001):
    
    def one_step_lookahead(s, vfn):
        actions = np.zeros(env.nA)

        for a, action in enumerate(env.P[s]):
            for outcome in range(len(action)):
                (prob, next_state, reward, done) = action[outcome]
                actions[a] += prob*(reward + discount_factor*vfn[next_state])

        return actions


    policy = np.zeros([env.nS, env.nA])
    vfn = np.zeros(env.nS)

    while True:
        delta = 0

        for s in range(env.nS):

            action_values = one_step_lookahead(s, vfn)

            best_action_value = max(action_values)

            delta = max(delta, abs(vfn[s] - best_action_value))

            vfn[s] = best_action_value

            best_action = np.argmax(action_values)

            policy[s] = np.eye(env.nA)[best_action]

        if delta < epsilon:
            return policy, vfn

if __name__ == "__main__":
    env = GP()
    p, v = value_iteration(env)

    matplotlib.use('TkAgg')
    
    fig = plt.figure(figsize=(20,20))

    vfn = fig.add_subplot(121)
    pol = fig.add_subplot(122)

    vfn.plot(v)
    vfn.set_xlabel('Capital', fontsize=16)
    vfn.set_ylabel('State Value', fontsize=16)
    vfn.set_title('Value function Gamblers Problem', fontsize=22)

    actions = np.argmax(np.array(p), axis=1)
    pol.plot(actions)
    pol.set_xlabel('Capital', fontsize=16)
    pol.set_ylabel('Stake', fontsize=16)
    pol.set_title('Policy Gamblers Problem', fontsize=22)

    plt.show()