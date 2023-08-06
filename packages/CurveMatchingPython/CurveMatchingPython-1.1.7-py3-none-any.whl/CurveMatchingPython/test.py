from CurveMatchingPython import CurveMatching as CM






x = [1, 2, 3, 4, 5]
y = [1, 2, 3, 4, 5]

x1 = [1, 2, 3, 4, 5]
y1 = [1, 2.5, 3, 4, 5]


# error = [0.2, 0.1, 0.2, 0.1, 0.2, 0.1]
# 9507728619896124

# CM.execute(x_sim=x, y_sim=x, x_exp=x, y_exp=x, numberOfBootstrapVariations=1, verbose=True)
# CM.execute(x_sim=x, y_sim=x, x_exp=x, y_exp=x, numberOfBootstrapVariations=20, verbose=True)
CM.execute(x_sim=x, y_sim=x, x_exp=x1, y_exp=y1,
           numberOfBootstrapVariations=1,
           verbose=True)
# print(CM.get_parameter().__dict__)
