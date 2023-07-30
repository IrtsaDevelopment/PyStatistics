# PyStatistics | Number Types






#Imports
from Factoring import *






#Classes
class WeightedNumber:
    @staticmethod
    def __checkIfValid(value):
        if type(value) == float: 
            if value > 1: return value <= 100
            return value >= 0 
        
        if type(value) == int: return value >= 0 and value <= 100
        
        return False
    

    @staticmethod
    def __checkWeightType(weight):
        if type(weight) == float:
            if weight > 1: return 'whole'
            return 'decimal'
        return 'whole'
    


    def __init__(self, number: int | float, weight: int | float):
        if self.__checkIfValid(weight):
            self.number = number
            self.weight = weight

            self.weightType = self.__checkWeightType(weight)

            self.__valid = True
        
        else: self.__valid = False


    @property
    def floatForm(self) -> float:
        if not self.__valid: return None

        if self.weightType == 'whole': weight = self.weight / 100.0
        else: weight = self.weight

        return round((self.number * weight), 2)
    

    @property
    def percentForm(self) -> str:
        if not self.__valid: return None

        if self.weightType == 'decimal': weight = self.weight * 100.0
        else: weight = float(self.weight)

        return str(round(weight, 2)) + '%'
    

    @property
    def stringForm(self) -> str:
        return self.__repr__()
    


    def __convertToFloat(self, other):
        if type(other) in [WeightedNumber, Decimal, Fraction]: return other.floatForm
        if type(other) in [float, int]: return float(other)
    


    def __add__(self, other):
        return self.floatForm + self.__convertToFloat(other)
    


    def __sub__(self, other):
        return self.floatForm - self.__convertToFloat(other)



    def __mul__(self, other):
        return self.floatForm * self.__convertToFloat(other)
    


    def __truediv__(self, other):
        return self.floatForm / self.__convertToFloat(other)
    


    def __radd__(self, other): return self.__add__(other)

    def __iadd__(self, other): return self.__add__(other)

    def __rsub__(self, other): return self.__sub__(other)
    
    def __isub__(self, other): return self.__sub__(other)
    
    def __rmul__(self, other): return self.__mul__(other)
      
    def __imul__(self, other): return self.__mul__(other)
    
    def __itruediv__(self, other): return self.__truediv__(other)

    def __rtruediv__(self, other): return self.__truediv__(other)

    def __repr__(self): return str(self.number) + ' - ' + self.percentForm




class Fraction:
    @staticmethod
    def __checkIfValidNumerator(value):
        return type(value) == int
    

    @staticmethod
    def __checkIfValidDenominator(value):
        return type(value) == int and value > 0
    

    @staticmethod
    def __numberToFraction(number: str | float | int):
        if type(number) == int: number = str(float(number))
        if type(number) == float: number = str(number)
        splitter = number.index('.')

        leftNumber = number[:splitter]
        rightNumber = number[splitter + 1:]

        denominator = 10 ** len(rightNumber)
        numerator = denominator * int(leftNumber) + int(rightNumber)

        return Fraction(numerator, denominator)
    

    @staticmethod
    def __newFractions(numeratorA, numeratorB, denominatorA, denominatorB):
        denominator = denominatorA * denominatorB
        numeratorA = numeratorA * denominatorB
        numeratorB = numeratorB * denominatorA

        return (numeratorA, numeratorB, denominator)
    

    @staticmethod
    def __simplify(fraction):
        numerator = fraction.numerator
        denominator = fraction.denominator
        neg = 1

        if numerator < 0 or denominator < 0:
            numerator = abs(numerator)
            denominator = abs(denominator)
            neg = -1

        if numerator == 0: return Fraction(0, denominator)
        
        gcf = GreatestCommonFactor([numerator, denominator])

        numerator /= gcf
        denominator /= gcf
        
        return Fraction(neg * int(numerator), int(denominator))


    
    def __init__(self, numerator: int, denominator: int):
        if self.__checkIfValidNumerator(numerator) and self.__checkIfValidDenominator(denominator):
            self.numerator = numerator
            self.denominator = denominator

            self.__valid = True
        
        else: self.__valid = False
    

    @property
    def floatForm(self) -> float:
        if not self.__valid: return None
        return round((float(self.numerator) / self.denominator), 2)
    

    @property
    def stringForm(self) -> str:
        return self.__repr__()
    

    
    def simplify(self):
        return self.__simplify(self)
    


    def __convertToFraction(self, other):
        if type(other) in [int, float]: other = self.__numberToFraction(other)
        if type(other) == Decimal: other = self.__numberToFraction(other.stringForm)
        if type(other) == WeightedNumber: other = self.__numberToFraction(other.floatForm)
        if type(other) == Fraction: return other
    


    def __add__(self, other):
        other = self.__convertToFraction(other)
        Fracs = self.__newFractions(self.numerator, other.numerator, self.denominator, other.denominator)
        return self.__simplify(Fraction((Fracs[0] + Fracs[1]), Fracs[2]))
    


    def __radd__(self, other):
        other = self.__convertToFraction(other)
        Fracs = self.__newFractions(self.numerator, other.numerator, self.denominator, other.denominator)
        return self.__simplify(Fraction((Fracs[1] + Fracs[0]), Fracs[2]))
    


    def __sub__(self, other):
        other = self.__convertToFraction(other)
        Fracs = self.__newFractions(self.numerator, other.numerator, self.denominator, other.denominator)
        return self.__simplify(Fraction((Fracs[0] - Fracs[1]), Fracs[2]))
    


    def __subr__(self, other):
        other = self.__convertToFraction(other)
        Fracs = self.__newFractions(self.numerator, other.numerator, self.denominator, other.denominator)
        return self.__simplify(Fraction((Fracs[1] - Fracs[0]), Fracs[2]))
    


    def __mul__(self, other):
        other = self.__convertToFraction(other)
        return self.__simplify(Fraction((self.numerator * other.numerator), (self.denominator * other.denominator)))
    


    def __truediv__(self, other):
        other = self.__convertToFraction(other)
        return self.__mul__(Fraction(other.denominator, other.numerator))
    


    def __iadd__(self, other): return self.__add__(other)
    
    def __isub__(self, other): return self.__sub__(other)
    
    def __rmul__(self, other): return self.__mul__(other)
      
    def __imul__(self, other): return self.__mul__(other)
    
    def __itruediv__(self, other): return self.__truediv__(other)

    def __rtruediv__(self, other): return self.__truediv__(other)

    def __repr__(self): return str(self.simplify().numerator) + '/' + str(self.simplify().denominator)




class Decimal:
    @staticmethod
    def __checkIfValid(value):
        try: value = int(value)
        except: return False
        
        if type(value) == int: return True
        return value.isdigit() and '.' not in value
    


    def __init__(self, integeral: str | int, fractional: str | int):
        if self.__checkIfValid(integeral) and self.__checkIfValid(fractional):
            self.integeral = str(integeral)
            self.fractional = str(fractional)
            
            self.__valid = True
        
        else: self.__valid = False
    

    @property
    def floatForm(self) -> float:
        if not self.__valid: return None
        return float(self.integeral + '.' + self.fractional)
        
    
    @property
    def stringForm(self) -> str: 
        return self.__repr__()
    


    def __convertToDecimal(self, other):
        if type(other) in [Fraction, WeightedNumber]: return Decimal(str(other.floatForm).split('.')[0], str(other.floatForm).split('.')[1])
        if type(other) == float: return Decimal(str(other).split('.')[0], str(other).split('.')[1])
        if type(other) == int: return Decimal(str(int(self.integeral) + int(other)), self.fractional)
        if type(other) == Decimal: return other
    


    def __add(self, other):
        integeral = str(int(self.integeral) + int(other.integeral))

        difference = abs(len(other.fractional) - len(self.fractional))
        if len(self.fractional) < len(other.fractional): fractional = str(eval(str(int(other.fractional)) + '+' + str(int(self.fractional + ('0' * difference)))))
        else: fractional = str(eval(str(int(self.fractional)) + '+' + str(int(other.fractional + '0' * difference))))

        maxLength = max(len(self.fractional), len(other.fractional))
        if len(fractional) > maxLength:
            integeral = str(int(integeral) + int(str(fractional)[:len(str(fractional)) - maxLength]))
            fractional = fractional[len(str(fractional)) - maxLength:]
        
        if len(fractional) < maxLength: fractional = ('0' * (maxLength - len(fractional))) + fractional

        return Decimal(integeral, fractional)
    


    def __addR(self, other):
        integeral = str(int(self.integeral) + int(other.integeral))

        difference = abs(len(other.fractional) - len(self.fractional))
        if len(other.fractional) < len(self.fractional): fractional = str(eval(str(int(self.fractional)) + '+' + str(int(other.fractional + ('0' * difference)))))
        else: fractional = str(eval(str(int(other.fractional)) + '+' + str(int(self.fractional + '0' * difference))))

        maxLength = max(len(self.fractional), len(other.fractional))
        if len(fractional) > maxLength:
            integeral = str(int(integeral) + int(str(fractional)[:len(str(fractional)) - maxLength]))
            fractional = fractional[len(str(fractional)) - maxLength:]
        
        if len(fractional) < maxLength: fractional = ('0' * (maxLength - len(fractional))) + fractional

        return Decimal(integeral, fractional)
    


    def __sub(self, other):
        integeral = str(int(self.integeral) - int(other.integeral))
        difference = abs(len(other.fractional) - len(self.fractional))
        
        if len(self.fractional) < len(other.fractional): fractional = str(eval(str(int(self.fractional + ('0' * difference))) + '-' + str(int(other.fractional))))
        else: fractional = str(eval(str(int(self.fractional)) + '-' + str(int(other.fractional + ('0' * difference)))))

        maxLength = max(len(self.fractional), len(other.fractional))

        if int(fractional) < 0 and int(integeral) > 0: integeral = str(int(integeral) - 1)
        fractional = str(10**maxLength - abs(int(fractional)))

        if len(fractional) < maxLength: fractional = ('0' * (maxLength - len(fractional))) + fractional
        return Decimal(integeral, fractional)
    


    def __subR(self, other):
        integeral = str(int(other.integeral) - int(self.integeral))
        difference = abs(len(other.fractional) - len(self.fractional))
        
        if len(other.fractional) < len(self.fractional): fractional = str(eval(str(int(other.fractional + ('0' * difference))) + '-' + str(int(self.fractional))))
        else: fractional = str(eval(str(int(other.fractional)) + '-' + str(int(self.fractional + ('0' * difference)))))

        maxLength = max(len(self.fractional), len(other.fractional))

        if int(fractional) < 0 and int(integeral) > 0: integeral = str(int(integeral) - 1)
        fractional = str(10**maxLength - abs(int(fractional)))

        if len(fractional) < maxLength: fractional = ('0' * (maxLength - len(fractional))) + fractional
        return Decimal(integeral, fractional)



    def __add__(self, other):
        other = self.__convertToDecimal(other)
        if int(other.integeral) < 0:
            other.integeral = str(-1 * int(other.integeral))
            decimal = self.__sub(other)
            other.integeral = str(-1 * int(other.integeral))
        else: decimal = self.__add(other)

        return decimal
    


    def __radd__(self, other):
        other = self.__convertToDecimal(other)
        if int(other.integeral) < 0:
            other.integeral = str(-1 * int(other.integeral))
            decimal = self.__subR(other)
            other.integeral = str(-1 * int(other.integeral))
        else: decimal = self.__addR(other)

        return decimal
            


    def __sub__(self, other):
        other = self.__convertToDecimal(other)
        if int(self.integeral) < 0:
            self.integeral = str(-1 * int(self.integeral))
            decimal = self.__add(other)
            self.integeral = str(-1 * int(self.integeral))
        else: decimal = self.__sub(other)

        return decimal
    


    def __rsub__(self, other): 
        other = self.__convertToDecimal(other)
        if int(self.integeral) < 0:
            self.integeral = str(-1 * int(self.integeral))
            decimal = self.__addR(other)
            self.integeral = str(-1 * int(self.integeral))
        else: decimal = self.__subR(other)

        return decimal


    def __mul__(self, other):
        other = self.__convertToDecimal(other)
        fracA = self.fractional
        fracB = other.fractional
        diff = abs(len(fracA) - len(fracB))

        if diff > 0:
            if len(fracA) < len(fracB): fracA += '0' * diff
            else: fracB += '0' * diff

        numberA = int(self.integeral) * 10**len(fracA)
        if numberA > 0:  numberA += int(fracA)
        else: numberA -= int(fracA)

        numberB = int(other.integeral) * 10**len(fracB)
        if numberB > 0: numberB += int(fracB)
        else: numberB -= int(fracB)

        result = str(numberA * numberB)
        split = len(result) - (len(fracA) * 2)
        
        return Decimal(result[:split], result[split:]) 
    


    def __truediv__(self, other):
        other = self.__convertToDecimal(other)
        fracA = self.fractional
        fracB = other.fractional
        diff = abs(len(fracA) - len(fracB))

        if diff > 0:
            if len(fracA) < len(fracB): fracA += '0' * diff
            else: fracB += '0' * diff

        numberA = int(self.integeral) * 10**len(fracA)
        if numberA > 0:  numberA += int(fracA)
        else: numberA -= int(fracA)

        numberB = int(other.integeral) * 10**len(fracB)
        if numberB > 0: numberB += int(fracB)
        else: numberB -= int(fracB)

        result = str(numberA / numberB)
        return Decimal(result.split('.')[0], result.split('.')[1])



    def __iadd__(self, other): return self.__add__(other)
    
    def __isub__(self, other): return self.__sub__(other)
    
    def __rmul__(self, other): return self.__mul__(other)
      
    def __imul__(self, other): return self.__mul__(other)
    
    def __itruediv__(self, other): return self.__truediv__(other)

    def __rtruediv__(self, other): return self.__truediv__(other)

    def __repr__(self): return str(self.integeral) + '.' + str(self.fractional)




class Matrix:
    @staticmethod
    def __convertData(Data):
        return [i.floatForm if type(i) in [WeightedNumber, Fraction] else i for i in Data]
    

    @staticmethod
    def __checkIfValid(value):
        valueLengths = [len(i) for i in value]
        return all([type(str) not in i for i in value]) and len(list({a : valueLengths.count(a) for a in valueLengths}.keys())) == 1
    

    @staticmethod
    def __multiplyLists(valueA, valueB):
        return sum([(valueA[i] * valueB[i]) for i in range(len(valueA))])
    

    @staticmethod
    def __invertList(value):
        return [[item[i] for item in value] for i in range(len(value[0]))]
    

    #setup for later
    #@staticmethod
    #def __findInverse(matrix): pass

    
    
    def __init__(self, *args: list):
        matrix = [self.__convertData(i) for i in args]

        if self.__checkIfValid(matrix):
            self.matrix = matrix
            self.rowAmount = len(matrix)
            self.columnAmount = len(matrix[0])

            self.__valid = True
        
        else: self.__valid = False
    

    @property
    def stringForm(self) -> str:
        return '\n'.join([' '.join([str(a) for a in i]) for i in self.matrix])
    


    def __ConvertToMatrix(self, other):
        if type(other) in [WeightedNumber, Fraction, Decimal]: other = other.floatForm
        if type(other) in [int, float]: return Matrix(*[[other for a in range(self.columnAmount)] for b in range(self.rowAmount)])
    


    def __add(self, other):
        return Matrix(*[[self.matrix[b][a] + other.matrix[b][a] for a in range(len(self.matrix[b]))] for b in range(len(self.matrix))])
    


    def __sub(self, other):
        return Matrix(*[[self.matrix[b][a] - other.matrix[b][a] for a in range(len(self.matrix[b]))] for b in range(len(self.matrix))])
    


    def __add__(self, other):
        if type(other) in [int, float, Fraction, WeightedNumber, Decimal]:
            other = self.__ConvertToMatrix(other)
            return self.__add(other)

        elif type(other) == Matrix:
            if self.rowAmount != other.rowAmount or self.columnAmount != other.columnAmount: return None
            return self.__add(other)
    


    def __sub__(self, other):
        if type(other) in [int, float, Fraction, WeightedNumber, Decimal]:
            other = self.__ConvertToMatrix(other)
            return self.__sub(other)

        elif type(other) == Matrix:
            if self.rowAmount != other.rowAmount or self.columnAmount != other.columnAmount: return None
            return self.__sub(other)
    


    def __mul__(self, other):
        if type(other) in [int, float, Fraction, WeightedNumber, Decimal]:
            other = self.__ConvertToMatrix(other)
            return Matrix(*[[self.matrix[b][a] * other.matrix[b][a] for a in range(len(self.matrix[b]))] for b in range(len(self.matrix))])

        elif type(other) == Matrix:
            if self.rowAmount != other.columnAmount: return None
            other = Matrix(*self.__invertList(other.matrix))

            NewMatrix = [[sum([(self.matrix[a][b] * other.matrix[c][b]) for b in range(len(self.matrix[a]))]) for a in range(len(self.matrix))] for c in range(len(other.matrix))]
            return Matrix(*self.__invertList(NewMatrix))
    


    def __iadd__(self, other): return self.__add__(other)
    
    def __isub__(self, other): return self.__sub__(other)
    
    def __rmul__(self, other): return self.__mul__(other)
      
    def __imul__(self, other): return self.__mul__(other)
    
    def __itruediv__(self, other): return self.__truediv__(other)

    def __rtruediv__(self, other): return self.__truediv__(other)

    def __repr__(self): return self.stringForm
            


    def __repr__(self):
        return self.stringForm