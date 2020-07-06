class Cell:
    def __init__(self, row, column, number=None):
        self._row = self._validate_row_column_input(row)
        self._column = self._validate_row_column_input(column)
        self._number = self._validate_number_input(number)
        self._possibilities = set([number]) if number else set(range(1,10))
        self._attempted = set()

    @property
    def row(self):
        """
        Access private variable value for cell row
        
        Returns:
            int -- value between 0 and 8
        """
        return self._row

    @property
    def column(self):
        """
        Access private variable value for cell column
        
        Returns:
            int -- value between 0 and 8
        """
        return self._column

    @property
    def solved(self):
        """
        Determine if cell is in a solved state by being assigned a number.
        
        Returns:
            bool -- True/False if the cell should be considered solved
        """
        return True if self._number else False

    @property
    def number(self):
        """
        Access number value assigned to cell
        
        Returns:
            int -- value assigned to the cell instance, 1-9 or None if not value is currently assigned
        """
        return self._number

    @number.setter
    def number(self, value):
        """
        Sets a value to the private variable _number. Setting a value of 1-9 will put the cell
        into a solved state or None will put the cell into an unsolved state.
        
        Arguments:
            value {int/None} -- the value the cell should be assigned
        """
        self._number = self._validate_number_input(value)

    @property
    def possibilities(self):
        """
        Access private variable possibilities which is a set of candidate values for the given cell
        
        Returns:
            set -- values of potential candidates for the cell
        """
        return self._possibilities

    def add_possibilities(self, values):
        """
        Add values to the possibilities variable
        
        Arguments:
            values {int} -- values that should be added to possibility list
        """
        for number in values:
            self._validate_number_input(number)
        self._possibilities.update(values)

    def remove_possibilities(self, values):
        """
        Remove values from the possibilities variable
        
        Arguments:
            values {int} -- values that should be removed from the possibility list
        """
        for number in values:
            self._validate_number_input(number)
        self._possibilities.difference_update(values)

    def _validate_number_input(self, number):
        """
        validates type and value for cell _number attribute
        
        Arguments:
            number {int} -- the value intended to be saved to the cell
        
        Raises:
            TypeError: raised if number is not an integer
            ValueError: raised if number is not between 1 and 9 inclusive
        
        Returns:
            int -- the validated number
        """
        if number is not None and type(number) is not int:
            raise TypeError("number must be of type int")
        if number is not None and number not in range(1,10):
            raise ValueError("number must be an integer between 1 and 9 inclusive")

        return number

    def _validate_row_column_input(self, value):
        """
        validates type and value for cell _row and _column attribute
        
        Arguments:
            value {int} -- the value stored in the cells _row or _column attribute
        
        Raises:
            TypeError: raised if value is not an int
            ValueError: raised if value is not between 0 and 8 inclusive
        
        Returns:
            int -- the validated value
        """
        if type(value) is not int:
            raise TypeError("row/column value must be of type int")
        if value not in range(0,9):
            raise ValueError("row/column value must be an integer between 0 and 8 inclusive")

        return value

    @property
    def attempted(self):
        """
        Access private varaible _attempted which is a set of all values previously attempted in this cell
        
        Returns:
            set -- all previously attempted values for the cell
        """
        return self._attempted

    def reset_attempted(self):
        """
        Reset the _attempted attribute to the empty set.
        """
        self._attempted.clear()

    def update_attempted(self, value):
        """
        Update the _attempted attribute with a chosen value. Used when a "guess" is made
        
        Arguments:
            value {int} -- a number that was placed into the cells _number attribute
        """
        self._attempted.add(self._validate_number_input(value))

    def choices_left(self):
        """
        Determine if the cell has a potential guess remaining to be tested
        
        Returns:
            bool -- True if there is a guess left to be tested, False otherwise
        """
        if len(self.possibilities-self.attempted) < 1:
            return False

        return True

    def __str__(self):
        return f"row: {self._row}, column: {self._column}, number: {self.number}, possibilities: {self.possibilities}, attempted: {self.attempted}"
