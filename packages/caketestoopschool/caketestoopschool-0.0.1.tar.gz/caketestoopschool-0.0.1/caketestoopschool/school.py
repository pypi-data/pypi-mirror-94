# -*- coding: utf-8 -*-

# school.py

class Student :
    def __init__(self,name,Lastname):
        self.name = name
        self.Lastname = Lastname
        self.exp = 0 # คะแนนประสบการณ์
        self.lesson = 0 # จำนวนคลาสที่เคยเรียน
        self.vehicle = 'รถเมลล์'
    @property
    def fullname(self):
        return '{} {}'.format(self.name, self.Lastname)

    def coding(self):
        '''นี่คือคลาสเรียนวิชาเขียนโปรแกรม'''
        self.AddEXP()
        
        print('{}กำลังเรียนเขียนโปรแกรม...'.format(self.fullname))
    def ShowEXP(self):
        print('{} ได้คะแนน {} exp (เรียนไป {} ครั้ง)'.format(self.name,self.exp,self.lesson)) 
    
    def AddEXP(self):
        self.exp += 10 # self.exp = self.exp+ 10
        self.lesson += 1# self.lesson = self.lesson+ 1 
    def __str__(self):
        return self.fullname

    def __repr__(self):
        return self.fullname

    def __add__(self,other):
        return self.exp + other.exp         



class Tesla:
    def __init__(self):
        self.model = 'Model S'
    def selfDriving(self,st):
        print('ระบบขับอัตโนมัตืกำลังทำงาน...กำลังพาคุณ{}กลับบ้าน!'.format(st.name))    




    def __str__(self):
        print('ระบบขับอัตโนมัติกำลังทำงาน...')
    def __str__(self):
        return self.model    


class SpicialStudent(Student): 
    def __init__(self,name,Lastname,father):
        super().__init__(name,Lastname)
        self.father = father
        self.vehicle = Tesla()
        print('รู้ไหมฉันลูกใคร?..!พ่อฉันชื่อ {}'.format(self.father))
    def AddEXP(self):
        self.exp += 30
        self.lesson += 2
class Teacher:
    def __init__(self,fullname):
        self.fullname = fullname
        self.students = []

    def CheckStudent(self):
        for i,st in enumerate(self.students):
            print('----นักเรียนของคุณครู{}----'.format(self.fullname))
            print('{}--->{} [{} exp][เรียนไป {} ครั้ง]'.format(i+1, st.fullname,st.exp,st.lesson))
    def AddStudent(self,st):
        self.students.append(st)
#print('FILE:',__name__)
if __name__ == '__main__':
    
    # Day 0
    allstudent = [] 
    teacher1  = Teacher('Ada Lovelace')
    teacher2 = Teacher('Bill Gates')
    print(teacher1.students)




                
    # Day 1
    print('-----Day1----')
    st1 = Student('Albert','Einstein')
    allstudent.append(st1) # สมัครเสร็จกับไว้ในลิสนักเรียนทันที
    teacher2.AddStudent(st1)
    print(st1.fullname)



    # Day 2
    print('-----Day2----')
    st2 = Student('Steve','jobs')
    allstudent.append(st2) # สมัครเสร็จกับไว้ในลิสนักเรียนทันที
    teacher2.AddStudent(st2)
    print(st2.fullname)

    # Day 3
    print('-----Day3----')
    for i in range(3):
        st1.coding()
    st1.coding()
    st2.coding()
    st1.ShowEXP()
    st2.ShowEXP()
    # Day4
    print('-----Day4----')

    stp1 = SpicialStudent('Thomas','Edison','Hitler')
    allstudent.append(stp1) # สมัครเสร็จกับไว้ในลิสนักเรียนทันที
    teacher1.AddStudent(stp1)
    print(stp1.fullname)

    print('คุณครูครับขอคะแนนฟรีสัก 20 คะแนนได้ไหม')
    stp1.exp = 20 # แก้ไขค่าใน class ได้
    stp1.coding()
    stp1.ShowEXP()

    # Day 5
    print('-----Day5----')
    print('นักเรียนกลับบ้านยังไงจ๊ะ?')
    print(allstudent)
    for st in allstudent:
        print('ผม: {} กลับบ้านด้วย {} ครับ'.format(st.name,st.vehicle))
        print(isinstance(st,SpicialStudent))
        if isinstance(st,SpicialStudent):
            st.vehicle.selfDriving(st)

    # Day 6
    print('-----Day6----')

    teacher1.CheckStudent()
    teacher2.CheckStudent()

    print('รวมพลังของนักเรียน 2 คน ',st1 + st2)

        





