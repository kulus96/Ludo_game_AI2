def move_piece(self, piece, dice, enemys):
    """
    Move the players piece the given dice following the game rules. Returns the new locations of the enemy's pieces

    :param piece: The piece to move
    :type piece: int
    :param dice: The dice to make the move with
    :type dice: int
    :param enemys: The enemy's pieces
    :type enemys: list with 4 lists each with 4 int's
    :return enemys: The new locations of the enemy's pieces
    :rtype enemys: list with 4 lists each with 4 int's

    """
    old_piece_pos = piece
    new_piece_pos = old_piece_pos + dice

    return_piece_pos = -1

    enemy_at_pos, enemy_pieces_at_pos = player.get_enemy_at_pos(new_piece_pos, enemys)

    # If the dice is 0 then no movement can be done
    if dice == 0:
        pass

    # At goal
    elif old_piece_pos == player.GOAL_INDEX:
        # The piece can not move
        pass

    # Goal areal
    elif old_piece_pos in player.HOME_AREAL_INDEXS:
        if new_piece_pos <= player.GOAL_INDEX:
            return_piece_pos = new_piece_pos
        else:
            overshoot = new_piece_pos - player.GOAL_INDEX
            new_piece_pos_corrected = old_piece_pos - overshoot
            return_piece_pos = new_piece_pos_corrected

    # The Home areal
    elif old_piece_pos == player.HOME_INDEX:
        if dice == player.DICE_MOVE_OUT_OF_HOME:
            return_piece_pos = player.START_INDEX

    # Star before the home areal
    elif new_piece_pos == player.STAR_AT_GOAL_AREAL_INDX:
        return_piece_pos = player.GOAL_INDEX

    # The other stars
    elif new_piece_pos in player.STAR_INDEXS:
        present_star_index = player.STAR_INDEXS.index(new_piece_pos)
        next_star_index = present_star_index + 1
        if next_star_index >= len(player.STAR_INDEXS):
            next_star_index = 0
        next_star_pos = player.STAR_INDEXS[next_star_index]

        return_piece_pos = next_star_pos

    # Globs there are not own by enemy
    elif new_piece_pos in player.GLOB_INDEXS:
        if enemy_at_pos != player.NO_ENEMY:
            return_piece_pos = player.HOME_INDEX
        else:
            return_piece_pos = new_piece_pos

    # Globs there are own by enemy
    elif new_piece_pos in player.LIST_ENEMY_GLOB_INDEX:
        # Get the enemy their own the glob
        globs_enemy = player.LIST_TAILE_ENEMY_GLOBS.index(player.BORD_TILES[new_piece_pos])
        # Check if there is a enemy at the glob
        if enemy_at_pos != player.NO_ENEMY:
            # If there is a other enemy then send them home and move there
            if enemy_at_pos != globs_enemy:
                return_piece_pos = new_piece_pos
            # If it is the same enemy there is there them move there
            else:
                return_piece_pos = player.HOME_INDEX
        # If there ant any enemy at the glob then move there
        else:
            return_piece_pos = new_piece_pos

    # If it is a TAILE_FREE or if we move from a GLOB/STAR to a not done case
    else:
        return_piece_pos = new_piece_pos

    return return_piece_pos


    def find_next_state(self,piece, enemy_pieces, dice, game):
        next_state_of_piece = normal_state

        old_piece_pos = piece
        new_piece_pos = old_piece_pos + dice
        enemy_at_pos, enemy_pieces_at_pos = player.get_enemy_at_pos(new_piece_pos, enemy_pieces)
        if old_piece_pos == player.HOME_INDEX and not (dice == 6):  # home index but not a 6
            next_state_of_piece = home_state

        elif old_piece_pos == player.HOME_INDEX and dice == 6:  # home index and a 6
            next_state_of_piece = safe_state

        elif old_piece_pos == player.GOAL_INDEX:  # at goal
            next_state_of_piece = goal_state

        elif old_piece_pos in player.HOME_AREAL_INDEXS or new_piece_pos in player.HOME_AREAL_INDEXS:
            if new_piece_pos == player.GOAL_INDEX:  # at the goal zone
                next_state_of_piece = goal_state
            else:
                next_state_of_piece = goal_zone_state

        elif new_piece_pos == player.STAR_AT_GOAL_AREAL_INDX:  # star before goal
            next_state_of_piece = goal_state

        elif (new_piece_pos in player.GLOB_INDEXS) or (new_piece_pos == player.START_INDEX):  # at the globe
            if enemy_at_pos != player.NO_ENEMY:
                next_state_of_piece = home_state
            else:
                next_state_of_piece = safe_state

        else:
            state_determined = 0

            for index in range(len(player.LIST_ENEMY_GLOB_INDEX)):  # check if the globs player is in play
                if new_piece_pos == player.LIST_ENEMY_GLOB_INDEX[index]:
                    if player.HOME_INDEX in enemy_pieces[index]:
                        if not (index in game.ghost_players):
                            next_state_of_piece = danger_state
                        else:
                            next_state_of_piece = safe_state
                        state_determined = 1
                        break

            if state_determined == 0:
                if next_state_of_piece in player.STAR_INDEXS:
                    if next_state_of_piece in player.STAR_INDEXS[1::2]:
                        range_to_look_for_enemies = list(range(1, 7))
                        range_to_look_for_enemies.extend(list(range(8, 14)))
                    else:
                        range_to_look_for_enemies = list(range(1, 13))
                else:
                    range_to_look_for_enemies = list(range(1, 7))
                for index in range_to_look_for_enemies:
                    piece_pos = new_piece_pos - index
                    if piece_pos < 1:
                        piece_pos = 52 + piece_pos
                    enemy_at_pos, _ = player.get_enemy_at_pos(piece_pos, enemy_pieces)
                    if not (enemy_at_pos == player.NO_ENEMY):
                        next_state_of_piece = danger_state
                        state_determined = 1
                        break

            if state_determined == 0:
                next_state_of_piece = normal_state

        return next_state_of_piece