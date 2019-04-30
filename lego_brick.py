class LegoBrick:
    color = ""
    correct_color = False
    correct_size = True
    #wrong_size = False
    correct_position = True
    position_x = 0
    position_y = 0 
    brick_height = 0
    rotation = 0
    min_area = 0
    max_area = 0

brick1 = LegoBrick()
brick1.position_x = 463
brick1.position_y = 253
brick1.min_area = 3800
brick1.max_area = 3950
brick1.color = "Red"

brick2 = LegoBrick()
brick2.position_x = 461
brick2.position_y = 336
brick2.min_area = 3800
brick2.max_area = 3950
brick2.color = "Red"

brick3 = LegoBrick()
brick3.position_x = 482
brick3.position_y = 292
brick3.min_area = 3200
brick3.max_area = 3600
brick3.color = "Blue"

brick4 = LegoBrick()
brick4.position_x = 483
brick4.position_y = 292
brick4.min_area = 1800
brick4.max_area = 2150
brick4.color = "Red"

brick5 = LegoBrick()
brick5.position_x = 483
brick5.position_y = 292
brick5.min_area = 3450
brick5.max_area = 3550
brick5.color = "Green"

brick6 = LegoBrick()
brick6.position_x = 483
brick6.position_y = 292
brick6.min_area = 2200
brick6.max_area = 2350
brick6.color = "Red"

brick7 = LegoBrick()
brick7.position_x = 461
brick7.position_y = 335
brick7.min_area = 3850
brick7.max_area = 3950
brick7.color = "Blue"

brick8 = LegoBrick()
brick8.position_x = 463
brick8.position_y = 253
brick8.min_area = 3850
brick8.max_area = 3950
brick8.color = "Blue"

brick9 = LegoBrick()
brick9.position_x = 483
brick9.position_y = 292
brick9.min_area = 3650
brick9.max_area = 3750
brick9.color = "Green"

brick10 = LegoBrick()
brick10.position_x = 483
brick10.position_y = 292
brick10.min_area = 2350
brick10.max_area = 2450
brick10.color = "Red"

lego_model = [brick1, brick2, brick3, brick4, brick5, brick6, brick7, brick8, brick9, brick10]