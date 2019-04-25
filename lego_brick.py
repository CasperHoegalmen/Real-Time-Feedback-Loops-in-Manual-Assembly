class LegoBrick:
    color = ""
    correct_size = True
    #wrong_size = False
    correct_position = True
    position_x = 0
    position_y = 0 
    brick_height = 0
    rotation = 0

brick1 = LegoBrick()
brick1.position_x = 325
brick1.position_y = 255
brick1.color = "Red"

brick2 = LegoBrick()
brick2.position_x = 370
brick2.position_y = 255
brick2.color = "Blue"

brick3 = LegoBrick()
brick3.color = "Red"

brick4 = LegoBrick()
brick4.color = "Green"

brick5 = LegoBrick()
brick5.color = "Blue"

brick6 = LegoBrick()
brick6.color = "Blue"

brick7 = LegoBrick()
brick7.color = "Green"

brick8 = LegoBrick()
brick8.color = "Red"

lego_model = [brick1, brick2, brick3, brick4, brick5, brick6, brick7, brick8]