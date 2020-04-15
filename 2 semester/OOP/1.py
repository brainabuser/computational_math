class Person:
    def __init__(self):
        print('Пустой объект класса ' + self.__class__.__name__ + ' создан.')

    def SetName(self, name):
        self._name = name

    def SetSurname(self, surname):
        self._surname = surname

    def SetAge(self, age):
        self._age = age

    def SetNationality(self, nationality):
        self._nationality = nationality

    def SetAddress(self, address):
        self._address = address

    def GetName(self):
        return self._name

    def GetSurname(self):
        return self._surname

    def GetAge(self):
        return self._age

    def GetNationality(self):
        return self._nationality

    def GetAddress(self):
        return self._address


class Worker(Person):
    def SetAge(self, age):
        self._age = age
        if self._age >= 18:
            print('Я - совершеннолетний рабочий.')

    def SetCompanyName(self, companyName):
        self._companyName = companyName

    def SetCompanyAddress(self, companyAddress):
        self._companyAddress = companyAddress

    def SetWorkPhone(self, workPhone):
        self._workPhone = workPhone

    def GetCompanyName(self):
        return self._companyName

    def GetCompanyAddress(self):
        return self._companyAddress

    def GetWorkPhone(self):
        return self._workPhone


class Scientist(Worker):
    def SetScientificalField(self, scientificalField):
        self._scientificalField = scientificalField

    def SetTypeOfScientist(self, typeOfScientist):
        self._typeOfScientist = typeOfScientist

    def SetNumberOfPublications(self, numberOfPublications):
        raise NotImplementedError

    def GetScientificalField(self):
        return self._scientificalField

    def GetTypeOfScientist(self):
        return self._typeOfScientist

    def GetNumberOfPublications(self):
        raise NotImplementedError


class Master(Scientist):
    def SetNumberOfPublications(self, numberOfPublications):
        self._numberOfPublications = 10 * numberOfPublications

    def GetNumberOfPublications(self):
        return self._numberOfPublications


class CandidateOfSciences(Scientist):
    def SetNumberOfPublications(self, numberOfPublications):
        self._numberOfPublications = 20 * numberOfPublications

    def GetNumberOfPublications(self):
        return self._numberOfPublications


class DoctorOfSciences(Scientist):
    def SetNumberOfPublications(self, numberOfPublications):
        self._numberOfPublications = 30 * numberOfPublications

    def GetNumberOfPublications(self):
        return self._numberOfPublications


master = Master()
master.SetName("Elon")
print(master.GetName())
master.SetSurname('Musk')
print(master.GetSurname())
master.SetNumberOfPublications(10)
print('Number of publications:', master.GetNumberOfPublications())

candidate = CandidateOfSciences()
candidate.SetName("Niels")
print(candidate.GetName())
candidate.SetSurname('Bohr')
print(candidate.GetSurname())
candidate.SetNumberOfPublications(10)
print('Number of publications:', candidate.GetNumberOfPublications())

doctor = DoctorOfSciences()
doctor.SetName("Isaac")
print(doctor.GetName())
doctor.SetSurname('Newton')
print(doctor.GetSurname())
doctor.SetNumberOfPublications(10)
print('Number of publications:', doctor.GetNumberOfPublications())
