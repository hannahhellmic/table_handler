import csv
import pickle

class InvalidFileFormatError(Exception):
    pass

class Table:
    def __init__(self, filename):
        self.filename = filename
        self.column_labels = None
        self.values = []
        self.max_length = None
        self.column_types_by_labels = {}
        self.column_types_by_numbers = {}
        self.file_format = None

    def open_csvfile(self, my_file):
        self.file_format = '.csv'

        with open(my_file, mode='r', encoding='utf-8') as file:
            reader = list(csv.reader(file))

            if self.column_labels is None:
                self.column_labels = reader[0]
            elif self.column_labels != reader[0]:
                raise AttributeError('Mismatching labels')

            for row in reader[1:]:
                self.values.append(dict(zip(self.column_labels, row)))

    def open_pklfile(self, my_file):
        self.file_format = '.pkl'

        with open(my_file, "rb") as file:
            reader = pickle.load(file)

        if self.column_labels is None:
            self.column_labels = list(reader[0].keys())
        elif self.column_labels != list(reader[0].keys()):
            raise AttributeError('Mismatching labels')

        self.values = reader

    def load_table(self, *files):
        for f in files:
            if f[-4:] == '.csv':
                self.open_csvfile(f)
            elif f[-4:] == '.pkl':
                self.open_pklfile(f)
            else:
                raise InvalidFileFormatError("Unsupported file format. Only .csv and .pkl files are allowed.")

        self.max_length = [
            max(len(str(row[col])) for row in self.values) for col in self.column_labels
        ]

        self.get_column_types()

    def print_table(self):
        s = "{:<10}"
        for i in range(len(self.column_labels)):
            t = "{:<" + str(self.max_length[i] + 5) + "} "
            s += t
        print(s.format('', *self.column_labels))
        print()
        for row in range(len(self.values)):
            formatted_values = ['None' if v is None else v for v in self.values[row].values()]
            print(s.format(row + 1, *formatted_values))

    def save_csvfile(self, write_down_name=None, max_rows=None):

        if max_rows is None:
            if write_down_name is None:
                write_down_name = f"{self.filename}.csv"

            if write_down_name[-4:] != '.csv':
                write_down_name += '.csv'

            with open(write_down_name, mode='w', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.column_labels)
                for row in self.values:
                    writer.writerow(row.values())
        else:
            cnt = 0
            while cnt * max_rows < len(self.values):
                if write_down_name is None:
                    wd_name = f"{self.filename}{cnt + 1}.csv"
                else:
                    wd_name = f"{write_down_name}{cnt + 1}.csv"

                with open(wd_name, mode='w', encoding='utf-8', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(self.column_labels)
                    for row in self.values[cnt * max_rows:(cnt + 1) * max_rows]:
                        writer.writerow(row.values())
                    cnt += 1

    def save_pklfile(self, write_down_name=None, max_rows=None):

        if max_rows is None:
            if write_down_name is None:
                write_down_name = f"{self.filename}.csv"

            if write_down_name[-4:] != '.pkl':
                write_down_name += '.pkl'

            with open(write_down_name, "wb") as file:
                pickle.dump(self.values, file)
        else:
            cnt = 0
            while cnt * max_rows < len(self.values):
                if write_down_name is None:
                    wd_name = f"{self.filename}{cnt + 1}.csv"
                else:
                    wd_name = f"{write_down_name}{cnt + 1}.csv"

                with open(wd_name, "wb") as file:
                    data = dict(zip(self.column_labels,
                                    [list(map(lambda x: x[label], self.values[cnt * max_rows:(cnt + 1) * max_rows])) for label in self.column_labels]))
                    pickle.dump(data, file)
                    cnt += 1

    def save_txtfile(self, write_down_name=None, max_rows=None):
        if max_rows is None:
            if write_down_name is None:
                write_down_name = f"{write_down_name}.txt"

            if write_down_name[-4:] != '.txt':
                write_down_name += '.txt'

            text_file = open(write_down_name, "w")
            s = "{:<10}"
            for i in range(len(self.column_labels)):
                t = "{:<" + str(self.max_length[i] + 5) + "} "
                s += t
            text_file.write(s.format('', *self.column_labels))
            text_file.write('\n')
            for row in range(len(self.values)):
                formatted_values = ['None' if v is None else v for v in self.values[row].values()]
                text_file.write(s.format(row + 1, *formatted_values))
                text_file.write('\n')
        else:
            cnt = 0
            while cnt * max_rows < len(self.values):
                if write_down_name is None:
                    wd_name = f"{self.filename}{cnt + 1}.txt"
                else:
                    wd_name = f"{write_down_name}{cnt + 1}.txt"

                text_file = open(wd_name, "w")
                s = "{:<10}"
                for i in range(len(self.column_labels)):
                    t = "{:<" + str(self.max_length[i] + 5) + "} "
                    s += t
                text_file.write(s.format('', *self.column_labels))
                text_file.write('\n')
                for row in range(max_rows * cnt, min(max_rows * (cnt + 1), len(self.values))):
                    formatted_values = ['None' if v is None else v for v in self.values[row].values()]
                    text_file.write(s.format(row + 1, *formatted_values))
                    text_file.write('\n')
                cnt += 1

    def save_table(self, write_down_name=None, max_rows=None, preferred_format=None):

        if (preferred_format is None and self.file_format == '.csv') or (preferred_format == 'csv'):
            self.save_csvfile(write_down_name, max_rows)
        elif (preferred_format is None and self.file_format == '.pkl') or (preferred_format == 'pkl'):
            self.save_pklfile(write_down_name, max_rows)
        elif preferred_format == '.txt':
            self.save_txtfile(write_down_name, max_rows)
        else:
            raise InvalidFileFormatError("The file format is not supported.")


    def get_rows_by_number(self, start, stop=None, copy_table=False):
        if stop is None:
            stop = start + 1

        rows = self.values[start - 1:stop]

        if copy_table:
            new_table = Table(filename=self.filename)
            new_table.column_labels = self.column_labels
            new_table.values = rows
            new_table.max_length = self.max_length
            return new_table
        else:
            return rows

    def get_rows_by_index(self, *vals, copy_table=False):

        rows = [row for row in self.values if row[self.column_labels[0]] in vals]

        if copy_table:
            new_table = Table(filename=self.filename)
            new_table.column_labels = self.column_labels
            new_table.values = rows
            new_table.max_length = self.max_length
            return new_table
        else:
            return rows

    def get_column_types(self, by_number=True):

        def get_info(element):
            if element == 'True' or element == 'False':
                return 'str'

            try:
                int(element)
                return 'int'
            except (TypeError, ValueError):
                try:
                    float(element)
                    return 'float'
                except (TypeError, ValueError):
                    return 'str'

        for col in range(len(self.column_labels)):
            cur_type = set()
            for row in self.values:
                el = row[self.column_labels[col]]
                cur_type.add(get_info(el))
                if len(cur_type) > 1:
                    break

            if len(cur_type) == 1:
                self.column_types_by_numbers[col] = list(cur_type)[0]
                self.column_types_by_labels[self.column_labels[col]] = list(cur_type)[0]
            else:
                self.column_types_by_numbers[col] = 'str'
                self.column_types_by_labels[self.column_labels[col]] = 'str'

        if by_number:
            return self.column_types_by_numbers
        else:
            return self.column_types_by_labels

    def set_column_types(self, types_dict, by_number=True):

        def change_to_int(col_value):
            if by_number:
                col_value = self.column_labels[col_value]
            for row in self.values:
                row[col_value] = int(row[col_value])

        def change_to_float(col_value):
            if by_number:
                col_value = self.column_labels[col_value]
            for row in self.values:
                row[col_value] = float(row[col_value])

        def change_to_bool(col_value):
            if by_number:
                col_value = self.column_labels[col_value]
            for row in self.values:
                row[col_value] = bool(row[col_value])

        def change_to_str(col_value):
            if by_number:
                col_value = self.column_labels[col_value]
            for row in self.values:
                row[col_value] = str(row[col_value])

        for cur_col in types_dict:
            try:
                if types_dict[cur_col] == 'str':
                    change_to_str(cur_col)
                elif types_dict[cur_col] == 'int':
                    change_to_int(cur_col)
                elif types_dict[cur_col] == 'float':
                    change_to_float(cur_col)
                elif types_dict[cur_col] == 'bool':
                    change_to_bool(cur_col)
            except ValueError:
                print('unsupported type')
            except TypeError:
                print('unsupported type')

    def get_values(self, column=0):
        if type(column) is int:
            column = self.column_labels[column]
        items = [row[column] for row in self.values]
        return items

    def get_value(self, column=0):
        if type(column) is int:
            column = self.column_labels[column]
        return self.values[0][column]

    def set_values(self, values, column=0):
        if len(values) != len(self.values):
            raise IndexError('number of rows doesnt match')
        else:
            cur_col_types = self.get_column_types(by_number=False)
            if type(column) is int:
                column = self.column_labels[column]
            required_type = cur_col_types[column]
            for row in range(len(self.values)):
                try:
                    if required_type == 'int':
                        self.values[row][column] = int(values[row])
                    elif required_type == 'float':
                        self.values[row][column] = float(values[row])
                    elif required_type == 'bool':
                        self.values[row][column] = bool(values[row])
                    elif required_type == 'str':
                        self.values[row][column] = str(values[row])
                except ValueError:
                    print('unsupported type')
                except TypeError:
                    print('unsupported type')

    def set_value(self, value, column=0, row=0):
        cur_col_types = self.get_column_types(by_number=False)
        if type(column) is int:
            column = self.column_labels[column]
        required_type = cur_col_types[column]
        try:
            if required_type == 'int':
                self.values[row][column] = int(value)
            elif required_type == 'float':
                self.values[row][column] = float(value)
            elif required_type == 'bool':
                self.values[row][column] = bool(value)
            elif required_type == 'str':
                self.values[row][column] = str(value)
        except ValueError:
            print('unsupported type')
        except TypeError:
            print('unsupported type')
        except IndexError:
            print('index is out of range of the table')

    def contact_tables(self, other_table):
        if self.column_labels != other_table.column_labels:
            raise AttributeError('mismatching labels')
        else:
            nt = Table(self.filename)
            nt.column_labels = self.column_labels
            nt.values = self.values + other_table.values
            nt.max_length = [max(self.max_length[col], other_table.max_length[col]) for col in range(len(nt.column_labels))]
            return nt

    def split_tables(self, row_number):
        if row_number <= len(self.values):
            nt1 = Table(self.filename)
            nt1.column_labels = self.column_labels
            nt1.values = self.values[:row_number]
            nt1.max_length = self.max_length
            nt2 = Table(self.filename)
            nt2.column_labels = self.column_labels
            nt2.values = self.values[row_number:]
            nt2.max_length = self.max_length
            return nt1, nt2
        else:
            raise IndexError('row number is out of range')

    def calculations(self, operation, column, row1, row2, new_row):
        if isinstance(column, int):
            column = self.column_labels[column-1]

        self.get_column_types()

        if self.column_types_by_labels[column] in {'int', 'float'}:
            try:
                if new_row:
                    row = self.values[row1-1].copy()
                    if operation == '+':
                        row[column] += self.values[row2-1][column]
                    elif operation == '-':
                        row[column] -= self.values[row2 - 1][column]
                    elif operation == '*':
                        row[column] *= self.values[row2 - 1][column]
                    elif operation == '/':
                        try:
                            row[column] /= self.values[row2 - 1][column]
                        except ZeroDivisionError:
                            raise ZeroDivisionError(f'value in row № {row2} is 0. Division by zero encountered.')
                    elif operation == '//':
                        try:
                            row[column] //= self.values[row2 - 1][column]
                        except ZeroDivisionError:
                            raise ZeroDivisionError(f'value in row № {row2} is 0. Division by zero encountered.')
                    self.values.append(row)
                else:
                    if operation == '+':
                        self.values[row1-1][column] += self.values[row2-1][column]
                    if operation == '-':
                        self.values[row1-1][column] -= self.values[row2-1][column]
                    if operation == '*':
                        self.values[row1-1][column] *= self.values[row2-1][column]
                    if operation == '/':
                        try:
                            self.values[row1-1][column] /= self.values[row2-1][column]
                        except ZeroDivisionError:
                            raise ZeroDivisionError(f'value in row № {row2} is 0. Division by zero encountered.')
                    if operation == '//':
                        try:
                            self.values[row1 - 1][column] //= self.values[row2 - 1][column]
                        except ZeroDivisionError:
                            raise ZeroDivisionError(f'Value in row № {row2} is 0. Division by zero encountered.')
            except IndexError:
                raise IndexError("Specified row number is out of range.")
            except KeyError:
                raise KeyError(f"Column '{column}' not found in the table.")
        else:
            TypeError(f"Column '{column}' has an unsupported type for calculations.")

    def add(self, column, row1, row2, new_row=False):
        self.calculations('+', column, row1, row2, new_row)

    def sub(self, column, row1, row2, new_row=False):
        self.calculations('-', column, row1, row2, new_row)

    def mul(self, column, row1, row2, new_row=False):
        self.calculations('*', column, row1, row2, new_row)

    def div_float(self, column, row1, row2, new_row=False):
        self.calculations('/', column, row1, row2, new_row)

    def div_int(self, column, row1, row2, new_row=False):
        self.calculations('//', column, row1, row2, new_row)