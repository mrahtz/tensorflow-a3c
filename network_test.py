import unittest

import numpy as np
import tensorflow as tf

from network import create_network


class TestNetwork(unittest.TestCase):

    def test_policy_loss(self):
        """
        Does calculating policy loss based on the cross-entropy really give
        the right result?
        """
        network = create_network('foo_scope', n_actions=6, entropy_bonus=0)
        sess = tf.Session()
        sess.run(tf.global_variables_initializer())

        obs = np.random.rand(3, 84, 84, 4)
        action_probs = sess.run(network.a_softmax,
                                feed_dict={network.s: obs})

        # Check that that the policy loss is calculated correctly
        rewards = [4, 5, 6]
        actions = [1, 3, 2]
        advantage, actual_loss = sess.run([network.advantage,
                                           network.policy_loss],
                                          feed_dict={network.s: obs,
                                                     network.a: actions,
                                                     network.r: rewards})
        expected_loss = -np.log(action_probs[0][1]) * advantage[0] + \
                        -np.log(action_probs[1][3]) * advantage[1] + \
                        -np.log(action_probs[2][2]) * advantage[2]
        expected_loss /= 3
        self.assertAlmostEqual(expected_loss, actual_loss, places=5)


if __name__ == '__main__':
    unittest.main()