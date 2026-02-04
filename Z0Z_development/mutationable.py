# ruff: noqa
qq = [3, 5, 7]
ww = qq
ee = qq.copy()
(rr := qq)
tt = id(qq)
yy = [qq][0]
qq.append(11)

print(f"{qq = }\n{ww = }\n{ee = }\n{rr = }\n{tt = }\n{yy = }")

