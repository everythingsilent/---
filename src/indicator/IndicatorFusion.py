# 将各级疲劳程度依次用数值表示：
# 清醒0        轻度1      中度2      重度3
# 0.1       0.3     0.7         1


def perclos_level(n):
    if n < 0.1:
        return 0.1
    elif n > 0.1 and n <= 0.3:
        return 0.3
    elif n > 0.3 and n <= 0.5:
        return 0.7
    else:
        return 1


def avg_close_eye_level(n):
    if n < 0.2:
        return 0.1
    elif n > 0.2 and n <= 0.25:
        return 0.3
    elif n > 0.25 and n <= 0.3:
        return 0.7
    else:
        return 1


def yawn_level(n):
    if n < 1:
        return 0.1
    elif n > 1 and n <= 2:
        return 0.3
    elif n > 2 and n <= 3:
        return 0.7
    else:
        return 1


def fusion_algorithm(perclos, eye, yawn):
    total = round((perclos * 1) + (eye * 0.8) + (yawn * 0.5), 2)

    if total <= 0.23:
        # 清醒
        return 0
    elif total > 0.23 and total <= 0.69:
        # 轻度疲劳
        return 1
    elif total > 0.69 and total <= 1.61:
        # 中度疲劳
        return 2
    else:
        # 重度疲劳
        return 3