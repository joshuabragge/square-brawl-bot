baseaddr = {
           'p1_health': 0x101F3648,
           'p2_health': 0x101F3648,
           #'p3_health': 0x100731FC,
           'p3_health': ["Square Brawl.exe", 0x100ECCBE0],
           'p4_health': ["Square Brawl.exe", 0x100E5C338],
           # 'p1_x': ["Square Brawl.exe", 0x100E04914],
           # 'p1_y': ["Square Brawl.exe", 0x100E04914],
           'p1_x': ["mono.dll", 0x1001F3648],
           'p1_y': ["mono.dll", 0x1001F3648],

           'p2_x': ["mono.dll", 0x1001F3648],
           'p2_y': ["mono.dll", 0x1001F3648],

           'p3_x': ["Square Brawl.exe", 0x100E9E108],
           'p3_y': ["Square Brawl.exe", 0x100E9E108],
           'p4_x': ["Square Brawl.exe", 0x100E9E108],
           'p4_y': ["Square Brawl.exe", 0x100E9E108],

           }

offsets = {
          'p1_health': [0x2A8, 0x55C, 0x58, 0x14, 0x3FC],
          'p2_health': [0x2A8, 0x55C, 0x7C, 0x14, 0x154],

          'p3_health': [0x11C, 0x18, 0x4C4, 0x234, 0x3FC],
          'p4_health': [0x35C, 0x46C, 0xE8, 0x140, 0x154],

          'p1_x': [0x2A8, 0x80C, 0xC, 0x48, 0xC],
          'p1_y': [0x2A8, 0x80C, 0xC, 0x48, 0x10],

          'p2_x': [0x2A8, 0x564, 0xC, 0x48, 0x2C],
          'p2_y': [0x2A8, 0x564, 0xC, 0x48, 0x30],

          'p3_x': [0x38, 0x5AC, 0x2C],
          'p3_y': [0x38, 0x5AC, 0x30],
          'p4_x': [0x36, 0x5AC, 0x2C],
          'p4_y': [0x36, 0x5AC, 0x30],

          }
# 'p3_health':[0x1A4,0xAC,0x80,0x4F8,0x6A4]}
# 'p3_health':[0xC,0xB4,0xF0,0x4F8,0x6A4]}
'''-0.6426766515
-13.28003788
'''
# 'p2_health': 0x101F30AC,
# 'p2_health': [0x1258, 0x400, 0xB3C],
