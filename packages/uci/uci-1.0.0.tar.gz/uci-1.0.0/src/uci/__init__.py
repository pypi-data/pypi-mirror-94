from stop_words import stop_words


class UCI:
    """Unique Content Identifier 

    Attributes
    ----------
    number: int
        Number must be greater than 46654 or where it end
    """

    def __init__(self, number):
        if not isinstance(number, (int, long)):
            raise TypeError('number must be an integer')
        if number <= 46654:
            raise ValueError('number must be greater than 46654')

        self.number = number

    @property
    def next(self):
        """Next uci number"""

        while True:
            self.number += 1
            sign = self.base36encode()
            if sign not in stop_words:
                break
        return sign

    @property
    def end_on(self):
        """Where the number end"""

        return self.number

    def base36encode(self):
        number = self.number

        alphabet, base36 = ['0123456789abcdefghijklmnopqrstuvwxyz', '']

        while number:
            number, i = divmod(number, 36)
            base36 = alphabet[i] + base36

        return base36 or alphabet[0]

    def base36decode(self, base36_number):
        return int(base36_number, 36)
