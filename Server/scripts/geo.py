def is_point_in_polygon(lon, lat):
    polygon = [
        (-66.29267798176957, -17.41047981158394),
        (-66.27317424368415, -17.408693224961368),
        (-66.27294019882764, -17.39894113180513),
        (-66.23826774043988, -17.396720279198477),
        (-66.23879483880194, -17.37547885632445),
        (-66.29549818091319, -17.38268571477103)
    ]
    num = len(polygon)
    j = num - 1
    c = False

    for i in range(num):
        if ((polygon[i][1] > lat) != (polygon[j][1] > lat)) and \
                (lon < (polygon[j][0] - polygon[i][0]) * (lat - polygon[i][1]) / (polygon[j][1] - polygon[i][1]) + polygon[i][0]):
            c = not c
        j = i

    return c
