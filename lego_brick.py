class LegoBrick:
    color = ""
    correct_color = False
    correct_size = True
    #wrong_size = False
    correct_position = True
    y = 0
    x = 0 
    h = 0
    w = 0
    brick_height = 0
    rotation = 0
    min_area = 0
    max_area = 0

brick1 = LegoBrick()
brick1.x = 450
brick1.y = 236
brick1.h = 283
brick1.w = 536
brick1.min_area = 3800
brick1.max_area = 3950
brick1.color = "Red"

brick2 = LegoBrick()
brick2.x = 449
brick2.y = 320
brick2.h = 367
brick2.w = 537
brick2.min_area = 3800
brick2.max_area = 3950
brick2.color = "Red"

brick3 = LegoBrick()
brick3.x = 494
brick3.y = 260
brick3.h = 347
brick3.w = 539
brick3.min_area = 3200
brick3.max_area = 3650
brick3.color = "Blue"

brick4 = LegoBrick()
brick4.x = 496
brick4.y = 282
brick4.h = 327
brick4.w = 541
brick4.min_area = 1900
brick4.max_area = 2150
brick4.color = "Red"

brick5 = LegoBrick()
brick5.x = 498
brick5.y = 263
brick5.h = 348
brick5.w = 542
brick5.min_area = 3400
brick5.max_area = 3600
brick5.color = "Green"

brick6 = LegoBrick()
brick6.x = 498
brick6.y = 248
brick6.h = 330
brick6.w = 544
brick6.min_area = 2200
brick6.max_area = 2350
brick6.color = "Red"

brick7 = LegoBrick()
brick7.x = 456
brick7.y = 329
brick7.h = 373
brick7.w = 543
brick7.min_area = 3850
brick7.max_area = 3950
brick7.color = "Blue"

brick8 = LegoBrick()
brick8.x = 458
brick8.y = 241
brick8.h = 283
brick8.w = 544
brick8.min_area = 3850
brick8.max_area = 3950
brick8.color = "Blue"

brick9 = LegoBrick()
brick9.x = 503
brick9.y = 265
brick9.h = 352
brick9.w = 546
brick9.min_area = 3650
brick9.max_area = 3750
brick9.color = "Green"

brick10 = LegoBrick()
brick10.x = 503
brick10.y = 289
brick10.h = 334
brick10.w = 549
brick10.min_area = 2350
brick10.max_area = 2450
brick10.color = "Red"

lego_model = [brick1, brick2, brick3, brick4, brick5, brick6, brick7, brick8, brick9, brick10]