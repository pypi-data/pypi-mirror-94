class Calculator:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def calculate(self):
        return self.a + self.b


if __name__ == '__main__':
    cal = Calculator(1 ,2)
    print(cal.calculate())
