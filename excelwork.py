from geopy import distance
from geopy.distance import lonlat, distance, geodesic, vincenty
import xlrd


class Excel:
    def __init__(self):
        workbook = xlrd.open_workbook("tablinfolocal.xlsx", on_demand=True)
        sheet = workbook.sheet_by_index(0)
        self.array_lon = []
        self.array_lat = []
        self.common_name = []
        self.category = []
        self.street_name = []
        self.way = []
        row_number = sheet.nrows

        for row in range(1, row_number):
            self.common_name.append(str(sheet.row(row)[1]).replace("text:", "").replace(":", " ").replace("'", " "))
            self.category.append(str(sheet.row(row)[2]).replace("text:", "").replace(":", " ").replace("'", " "))
            self.street_name.append(str(sheet.row(row)[5]).replace("text:", "").replace(":", " ").replace("'", " "))
            self.array_lon.append(str(sheet.row(row)[6]).replace("text:", "").replace(":", " ").replace("'", " "))
            self.array_lat.append(str(sheet.row(row)[7]).replace("text:", "").replace(":", " ").replace("'", " "))

    def distance_calculation(self, user_local):
        i = 0
        while i != 1837:
            placeclocal = (float(self.array_lat[i]), float(self.array_lon[i]))
            resultt = geodesic(user_local, placeclocal).meters
            self.way.append(resultt)
            i += 1
        index = self.way.index(min(self.way))
        return index
