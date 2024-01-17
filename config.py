figure_index = {'1': 0, '2': 1, '3': 2, '4': 3, 'base_toolbox': 4,
                'big_colorbar': 5, 'big_eraser': 6, 'big_indicator': 7,
                'big_left': 8, 'big_line': 9, 'big_painter': 10, 'big_right': 11,
                'big_timebin': 12, 'black_colorbar': 13, 'black_eraser': 14,
                'black_indicator': 15, 'black_left': 16, 'black_line': 17,
                'black_painter': 18, 'black_right': 19, 'black_timebin': 20,
                'boundingbox': 21, 'left_over.jpg': 22, 'right_over': 23,
                'second_bbox': 24, 'slider': 25, 'small_colorbar': 26, 'small_eraser': 27,
                'small_indicator': 28, 'small_left': 29, 'small_line': 30,
                'small_painter': 31, 'small_right': 32, 'small_timebin': 33}

figure_size = {'1': (153, 1280, 3), '2': (153, 1280, 3), '3': (153, 1280, 3), '4': (153, 1280, 3),
               'base_toolbox': (124, 720, 3), 'big_colorbar': (96, 96, 3), 'big_eraser': (96, 96, 3),
               'big_indicator': (96, 96, 3),
               'big_left': (96, 96, 3), 'big_line': (197, 247, 3), 'big_painter': (96, 96, 3), 'big_right': (96, 96, 3),
               'big_timebin': (96, 96, 3), 'black_colorbar': (96, 96, 3), 'black_eraser': (96, 96, 3),
               'black_indicator': (96, 96, 3), 'black_left': (96, 96, 3), 'black_line': (197, 247, 3),
               'black_painter': (96, 96, 3), 'black_right': (96, 96, 3), 'black_timebin': (96, 96, 3),
               'boundingbox': (124, 275, 3), 'left_over.jpg': (76, 76, 3), 'right_over': (75, 76, 3),
               'second_bbox': (150, 900, 3), 'slider': (7, 800, 3), 'small_colorbar': (75, 76, 3),
               'small_eraser': (75, 75, 3),
               'small_indicator': (75, 75, 3), 'small_left': (75, 76, 3), 'small_line': (149, 195, 3),
               'small_painter': (75, 76, 3), 'small_right': (75, 76, 3), 'small_timebin': (75, 76, 3)}

widgets = {'base': ['base_toolbox', 'small_painter', 'small_eraser', 'small_indicator'],
          'hold_painter' : ['base_toolbox', 'small_painter', 'small_eraser', 'small_indicator'],
          'hold_eraser' : ['base_toolbox', 'small_painter', 'small_eraser', 'small_indicator'],
          'hold_indicator' : ['base_toolbox', 'small_painter', 'small_eraser', 'small_indicator'],
          'select_painter' : ['base_toolbox', 'big_painter', 'small_eraser', 'small_indicator'],
          'select_eraser' : ['base_toolbox', 'small_painter', 'big_eraser', 'small_indicator'],
          'select_indicator' : ['base_toolbox', 'small_painter', 'small_eraser', 'big_indicator']}

widget_pos = {'base_toolbox' : [0, 480],
              'small_painter' : [25, 560],
              'small_indicator' : [25, 803],
              'small_eraser' : [25, 1045],
              'big_painter' : [14, 550],
              'big_indicator' : [14, 793],
              'big_eraser': [14, 1035]}

area = {'base_toolbox' : [[0, 124], [480, 1200]],
              'small_painter' : [[25, 100], [560, 636]],
              'small_indicator' : [[25, 100], [803, 878]],
              'small_eraser' : [[25, 100], [1045, 1120]],
              'big_painter' : [[14, 110], [550, 646]],
              'big_indicator' : [[14, 110], [793, 888]],
              'big_eraser': [[14, 110], [1035, 1130]]}
