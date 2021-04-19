import unittest
import sys
sys.path.append("../")
import ludopy
import numpy as np
import cv2
#import Q_Learning



def randwalk():


    g = ludopy.Game([1,2,3])
    there_is_a_winner = False

    while not there_is_a_winner:
        (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner,
         there_is_a_winner), player_i = g.get_observation()
        print("dice", dice)
        print("move_pieces", move_pieces)
        print("player_pieces", player_pieces)
        print("enemy_pieces", enemy_pieces)
        print("player_is_a_winner", player_is_a_winner)
        print("there_is_a_winner", there_is_a_winner)
        print("player_i", player_i)
        print('determind_state',Q_Learning.determind_state(player_pieces))

        if len(move_pieces):
            piece_to_move = move_pieces[np.random.randint(0, len(move_pieces))]
        else:
            piece_to_move = -1

        _, _, _, _, _, there_is_a_winner = g.answer_observation(piece_to_move)

        cv2.imshow('test',(g.render_environment()))
        cv2.waitKey(0)

    print("Saving history to numpy file")
    g.save_hist("game_history.npy")
    print("Saving game video")
    g.save_hist_video("game_video.mp4")

    return True


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, randwalk())


if __name__ == '__main__':
    unittest.main()
