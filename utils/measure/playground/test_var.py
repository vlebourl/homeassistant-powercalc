def get_ct_variations():
    i = 0
    for _ in inclusive_range(1, 255, 15):
        for _ in inclusive_range(150, 500, 50):
            i = i + 1
    print(f"ct: {str(i)}")

def get_hs_variations():
    i = 0
    for _ in inclusive_range(1, 255, 10):
        for _ in inclusive_range(1, 254, 10):
            for _ in inclusive_range(1, 65535, 2000):
                i = i + 1
    print(f"hs: {str(i)}")

def get_brightness_variations():
    i = 0
    for _ in inclusive_range(1, 255, 3):
        i = i + 1
    print(f"bri: {str(i)}")

def inclusive_range(start: int, end: int, step: int):
    i = start
    while i < end:
        yield i
        i += step
    yield end

get_ct_variations()
get_hs_variations()
get_brightness_variations()