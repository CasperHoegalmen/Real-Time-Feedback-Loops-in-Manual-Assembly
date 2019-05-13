class LegoBrick:
    color = ""
    correct_color = False
    correct_size = True
    #wrong_size = False
    correct_position = True
    correct_height = False
    is_flat = True
    y = 0
    x = 0 
    h = 0
    w = 0
    brick_height = 0
    rotation = 0
    min_area = 0
    max_area = 0
    area_range = 400
    position_offset = 12

brick1 = LegoBrick()
brick1.x = 658 - LegoBrick.position_offset
brick1.y = 324 - LegoBrick.position_offset
brick1.h = 409 + LegoBrick.position_offset
brick1.w = 828 + LegoBrick.position_offset
brick1.min_area = 13970 - LegoBrick.area_range
brick1.max_area = 13970 + LegoBrick.area_range
brick1.color = "Red"

brick2 = LegoBrick()
brick2.x = 309 - LegoBrick.position_offset
brick2.y = 202 - LegoBrick.position_offset
brick2.h = 247 + LegoBrick.position_offset
brick2.w = 396 + LegoBrick.position_offset
brick2.min_area = 3610 - LegoBrick.area_range
brick2.max_area = 3610 + LegoBrick.area_range
brick2.color = "Red"

brick3 = LegoBrick()
brick3.x = 351 - LegoBrick.position_offset
brick3.y = 224 - LegoBrick.position_offset
brick3.h = 310 + LegoBrick.position_offset
brick3.w = 395 + LegoBrick.position_offset
brick3.min_area = 3520 - LegoBrick.area_range
brick3.max_area = 3520 + LegoBrick.area_range
brick3.color = "Blue"

brick4 = LegoBrick()
brick4.x = 350 - LegoBrick.position_offset
brick4.y = 243 - LegoBrick.position_offset
brick4.h = 289 + LegoBrick.position_offset
brick4.w = 395 + LegoBrick.position_offset
brick4.min_area = 1915 - LegoBrick.area_range
brick4.max_area = 1915 + LegoBrick.area_range
brick4.color = "Red"

brick5 = LegoBrick()
brick5.x = 350 - LegoBrick.position_offset
brick5.y = 223 - LegoBrick.position_offset
brick5.h = 309 + LegoBrick.position_offset
brick5.w = 394 + LegoBrick.position_offset
brick5.min_area = 3675 - LegoBrick.area_range
brick5.max_area = 3675 + LegoBrick.area_range
brick5.color = "Green"

brick6 = LegoBrick()
brick6.x = 350 - LegoBrick.position_offset
brick6.y = 243 - LegoBrick.position_offset
brick6.h = 287 + LegoBrick.position_offset
brick6.w = 394 + LegoBrick.position_offset
brick6.min_area = 1905 - LegoBrick.area_range
brick6.max_area = 1905 + LegoBrick.area_range
brick6.color = "Red"

brick7 = LegoBrick()
brick7.x = 307 - LegoBrick.position_offset
brick7.y = 288 - LegoBrick.position_offset
brick7.h = 330 + LegoBrick.position_offset
brick7.w = 393 + LegoBrick.position_offset
brick7.min_area = 3570 - LegoBrick.area_range
brick7.max_area = 3570 + LegoBrick.area_range
brick7.color = "Blue"

brick8 = LegoBrick()
brick8.x = 308 - LegoBrick.position_offset
brick8.y = 199 - LegoBrick.position_offset
brick8.h = 243 + LegoBrick.position_offset
brick8.w = 394 + LegoBrick.position_offset
brick8.min_area = 3600 - LegoBrick.area_range
brick8.max_area = 3600 + LegoBrick.area_range
brick8.color = "Blue"

brick9 = LegoBrick()
brick9.x = 348 - LegoBrick.position_offset
brick9.y = 220 - LegoBrick.position_offset
brick9.h = 309 + LegoBrick.position_offset
brick9.w = 394 + LegoBrick.position_offset
brick9.min_area = 3790 - LegoBrick.area_range
brick9.max_area = 3790 + LegoBrick.area_range
brick9.color = "Green"

brick10 = LegoBrick()
brick10.x = 348 - LegoBrick.position_offset
brick10.y = 242 - LegoBrick.position_offset
brick10.h = 287 + LegoBrick.position_offset
brick10.w = 393 + LegoBrick.position_offset
brick10.min_area = 1920 - LegoBrick.area_range
brick10.max_area = 1920 + LegoBrick.area_range
brick10.color = "Red"

brick11 = LegoBrick()
brick11.x = 658 - LegoBrick.position_offset
brick11.y = 324 - LegoBrick.position_offset
brick11.h = 409 + LegoBrick.position_offset
brick11.w = 828 + LegoBrick.position_offset
brick11.min_area = 13950 - LegoBrick.area_range
brick11.max_area = 13950 + LegoBrick.area_range
brick11.is_flat = False
brick11.color = "Red"

brick12 = LegoBrick()
brick12.x = 827 - LegoBrick.position_offset
brick12.y = 367 - LegoBrick.position_offset
brick12.h = 453 + LegoBrick.position_offset
brick12.w = 997 + LegoBrick.position_offset
brick12.min_area = 14000 - LegoBrick.area_range
brick12.max_area = 14000 + LegoBrick.area_range
brick12.is_flat = False
brick12.color = "Yellow"

brick13 = LegoBrick()
brick13.x = 828 - LegoBrick.position_offset
brick13.y = 283 - LegoBrick.position_offset
brick13.h = 368 + LegoBrick.position_offset
brick13.w = 996 + LegoBrick.position_offset
brick13.min_area = 13000 - LegoBrick.area_range
brick13.max_area = 13000 + LegoBrick.area_range
brick13.is_flat = False
brick13.color = "Purple"

brick14 = LegoBrick()
brick14.x = 913 - LegoBrick.position_offset
brick14.y = 326 - LegoBrick.position_offset
brick14.h = 410 + LegoBrick.position_offset
brick14.w = 998 + LegoBrick.position_offset
brick14.min_area = 6840 - LegoBrick.area_range
brick14.max_area = 6840 + LegoBrick.area_range
brick14.is_flat = True
brick14.color = "Red"

brick15 = LegoBrick()
brick15.x = 744 - LegoBrick.position_offset
brick15.y = 323 - LegoBrick.position_offset
brick15.h = 410 + LegoBrick.position_offset
brick15.w = 914 + LegoBrick.position_offset
brick15.min_area = 13560 - LegoBrick.area_range
brick15.max_area = 13560 + LegoBrick.area_range
brick15.is_flat = True
brick15.color = "Green"

brick16 = LegoBrick()
brick16.x = 867 - LegoBrick.position_offset
brick16.y = 409 - LegoBrick.position_offset
brick16.h = 579 + LegoBrick.position_offset
brick16.w = 955 + LegoBrick.position_offset
brick16.min_area = 13200 - LegoBrick.area_range
brick16.max_area = 13200 + LegoBrick.area_range
brick16.is_flat = True
brick16.color = "Blue"

brick17 = LegoBrick()
brick17.x = 870 - LegoBrick.position_offset
brick17.y = 156 - LegoBrick.position_offset
brick17.h = 326 + LegoBrick.position_offset
brick17.w = 958 + LegoBrick.position_offset
brick17.min_area = 13120 - LegoBrick.area_range
brick17.max_area = 13120 + LegoBrick.area_range
brick17.is_flat = True
brick17.color = "Blue"

brick18 = LegoBrick()
brick18.x = 870 - LegoBrick.position_offset
brick18.y = 279 - LegoBrick.position_offset
brick18.h = 451 + LegoBrick.position_offset
brick18.w = 958 + LegoBrick.position_offset
brick18.min_area = 13720 - LegoBrick.area_range
brick18.max_area = 13720 + LegoBrick.area_range
brick18.is_flat = False
brick18.color = "Purple"

brick19 = LegoBrick()
brick19.x = 745 - LegoBrick.position_offset
brick19.y = 319 - LegoBrick.position_offset
brick19.h = 406 + LegoBrick.position_offset
brick19.w = 875 + LegoBrick.position_offset
brick19.min_area = 10588 - LegoBrick.area_range
brick19.max_area = 10588 + LegoBrick.area_range
brick19.is_flat = False
brick19.color = "Yellow"

brick20 = LegoBrick()
brick20.x = 831 - LegoBrick.position_offset
brick20.y = 319 - LegoBrick.position_offset
brick20.h = 406 + LegoBrick.position_offset
brick20.w = 916 + LegoBrick.position_offset
brick20.min_area = 7090 - LegoBrick.area_range
brick20.max_area = 7090 + LegoBrick.area_range
brick20.is_flat = False
brick20.color = "Green"

brick21 = LegoBrick()
brick21.x = 876 - LegoBrick.position_offset
brick21.y = 152 - LegoBrick.position_offset
brick21.h = 194 + LegoBrick.position_offset
brick21.w = 917 + LegoBrick.position_offset
brick21.min_area = 1640 - LegoBrick.area_range
brick21.max_area = 1640 + LegoBrick.area_range
brick21.is_flat = False
brick21.color = "Red"

brick22 = LegoBrick()
brick22.x = 870 - LegoBrick.position_offset
brick22.y = 537 - LegoBrick.position_offset
brick22.h = 578 + LegoBrick.position_offset
brick22.w = 911 + LegoBrick.position_offset
brick22.min_area = 1600 - LegoBrick.area_range
brick22.max_area = 1600 + LegoBrick.area_range
brick22.is_flat = False
brick22.color = "Green"

brick23 = LegoBrick()
brick23.x = 955 - LegoBrick.position_offset
brick23.y = 409 - LegoBrick.position_offset
brick23.h = 454 + LegoBrick.position_offset
brick23.w = 1083 + LegoBrick.position_offset
brick23.min_area = 4900 - LegoBrick.area_range
brick23.max_area = 4900 + LegoBrick.area_range
brick23.is_flat = False
brick23.color = "Green"

brick24 = LegoBrick()
brick24.x = 957 - LegoBrick.position_offset
brick24.y = 280 - LegoBrick.position_offset
brick24.h = 324 + LegoBrick.position_offset
brick24.w = 1085 + LegoBrick.position_offset
brick24.min_area = 4050 - LegoBrick.area_range
brick24.max_area = 5050 + LegoBrick.area_range
brick24.is_flat = False
brick24.color = "Yellow"

# lego_model = [brick1, brick2, brick3, brick4, brick5, brick6, brick7, brick8, brick9, brick10, 
#                 brick11, brick12, brick13, brick14, brick15, brick16, brick17, brick18, brick19, brick20, brick21, brick22, brick23, brick24]

lego_model = [brick11, brick12, brick13, brick14, brick15, brick16, brick17, brick18, brick19, brick20, brick21, brick22, brick23, brick24, brick1, brick1, brick1]