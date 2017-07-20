import tensorflow as tf
import numpy as np

def copy_network(sess, from_scope, to_scope):
    # TODO: only trainable variables?
    from_tvs = tf.get_collection(
        tf.GraphKeys.TRAINABLE_VARIABLES,
        scope=from_scope)
    to_tvs = tf.get_collection(
        tf.GraphKeys.TRAINABLE_VARIABLES,
        scope=to_scope)
    
    from_dict = {var.name: var for var in from_tvs}
    to_dict = {var.name: var for var in to_tvs}
    copy_ops = []
    for to_name, to_var in to_dict.items():
        op = to_var.assign(from_dict[to_name.replace(to_scope, from_scope)].value())
        copy_ops.append(op)
    sess.run(copy_ops)
    
def with_prob(p):
    if np.random.random() < p:
        return True
    else:
        return False

def discount_rewards(r, G):
    r2 = np.zeros_like(np.array(r).astype(np.float32))
    r2[-1] = r[-1]
    for i in range(len(r2)-2, -1, -1):
        r2[i] = G * r2[i+1]
    return r2

def rewards_to_returns(r, G):
    r2 = np.zeros_like(np.array(r).astype(np.float32))
    r2[-1] = r[-1]
    for i in range(len(r2)-2, -1, -1):
        r2[i] = r[i] + G * r2[i+1]
    return r2