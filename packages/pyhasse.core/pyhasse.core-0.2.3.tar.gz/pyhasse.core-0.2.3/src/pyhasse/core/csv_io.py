""" Module reading data from CSV or form

Formvalues must have a csv structure.
- if objects or attributes have the same name,
  an explicit name is generated
- lines not following the structure of the first line
  are automatically ignored
- in demo-mode you can set the max rows to a given number

"""


class CSVReader(object):
    """ Read Data from csv files and convert the data to a matrix

    :param  fn: Filename (incl. path)
    :var obj: list of object names
    :var a: field of the csv-File (inclus. att and obj names)
    :var la: all rows (inclus. names of attributes)
    :var ls: all columns (inclus. names of objects)
    :var dm: interim field of entries of csv-file
    :var formval: values taken from a formular (string)
    :var ndec: number of decimals (precision)
    :var skipped_rows: list of ignored rows
    """

    def __init__(self, fn=None, formval=None, ndec=3, demo=None):

        self.DEMO = demo
        self.fn = fn
        self.formval = formval
        self.max = 0
        self.ndec = ndec
        self.eqm = []
        self.prop = []
        self.obj = []
        self.cols = 0
        self.rows = 0
        self.data = []
        self.skiped_rows = []
        self.redrows = 0
        self.missing_data = False
        self.missing_attr = False
        self.delimiter = None
        self.dmdim()

    def read_string(self):
        """Load csv data from string

        :var max: filter lines, not as long as the header"""

        formval = self.formval.split("\n")
        if len(formval) < 2:
            self.missing_data = True
            return
        # firstline for delimiter
        for j in [",", "\t", ";", " "]:
            firstline = formval[0].strip().split(j)
            firstlinevalues = [i for i in firstline if i != ""]
            secondline = formval[1].strip().split(j)
            secondlinevalues = [i for i in secondline if i != ""]

            # if the upper left corner is not filled
            if len(secondlinevalues) == len(firstlinevalues) + 1:
                values = [""] + firstlinevalues
            else:
                values = firstlinevalues
            if len(values) > 1:
                counter = 1
                for i in values:
                    counter += 1
                self.max = len(values)
                self.delimiter = j
                break
        self.prop, renamed_attributes = self._rename_double(values[1:])
        obj_names = []
        for i in range(1, len(formval)):
            line = formval[i].strip().split(self.delimiter)
            if line[0] == "":
                line[0] = "dummy" + str(i)
            values = [j for j in line if j.strip() != ""]
            if len(values) != self.max:
                self.skiped_rows.append([i, len(values), formval[i]])
            else:
                try:
                    floats = [float(k.replace(",", ".")) for k in values[1:]]
                    self.data.append(floats)
                    obj_names.append(values[0])
                except Exception:
                    pass

        self.obj, renamed_objects = self._rename_double(obj_names)
        self._demomode()
        self.rows = len(self.obj)
        self.cols = len(self.prop)
        # check minimum of data
        if self.rows > 1:
            self.missing_data = False
        else:
            self.missing_data = True
            msg = ["", "", "<p><em>Not enough rows</em>, check your data</p>"]
            self.skiped_rows.append(msg)

        if self.cols > 0:
            self.missing_attr = False
        else:
            self.missing_attr = True
            msg = ["", "", "<p><em>Attributes missing </em>, check your data"]
            self.skiped_rows.append((msg))
        if renamed_objects or renamed_attributes:
            msg = ["", "", "<p>Some names are identical and renamed</p>"]
            self.skiped_rows.append((msg))

    def _demomode(self):
        """Cut the number of rows and colums to a given value"""
        if self.DEMO:
            demodata = []
            if self.DEMO > len(self.data):
                maxrows = len(self.data)
            else:
                maxrows = self.DEMO
            for i in range(maxrows):
                demodata.append(self.data[i][:maxrows])
            if self.DEMO > len(self.prop):
                maxcols = len(self.prop)
            else:
                maxcols = self.DEMO

            self.data = demodata
            self.prop = self.prop[:maxcols]
            self.obj = self.obj[:maxrows]

    def dmdim(self):
        """Dimension of the read-in datamatrix"""

        if self.fn:
            fhd = open(self.fn, "r")
            with fhd:
                self.formval = fhd.read()
            fhd.close()
        self.read_string()

    def _rename_double(self, names=[]):
        """rename if two names are identical

        :param list names: list of names
        :rtype: tuple
        :returns: unique_names - list inclusive renamed values
                  renamed - list of old names, renamed
        """
        seen = set()
        unique_names = []
        counters = {}
        renamed = []
        for x in names:
            x = x.strip().replace(" ", "-")
            if x not in seen:
                seen.add(x)
                counters[x] = 0
                unique_names.append(x)
            else:
                counters[x] += 1
                renamed.append(x)
                unique_names.append("{}_{}".format(x, counters[x]))
        return unique_names, renamed
