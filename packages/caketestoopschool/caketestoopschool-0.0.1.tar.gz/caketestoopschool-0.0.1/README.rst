(OOP School) ใช้สำหรับใช้เรียน Python OOP CKDEV
===============================================

Python OOP+ วิธีสร้าง Library เป็นของตัวเอง+ อัพโหลด Package ไปยัง
PyPI.org

โปรแกรมนี้ลุงใช้สำหรับสอน OOP Programming โดยสามารถดูตัวอย่างคลิปได้ใน:
https://www.youtube.com/watch?v=1egtTXUJ3-4&t=11609s

วิธีติดตั้ง
~~~~~~~~~~~

เปิด CMD / Terminal

.. code:: python

    pip install caketestoopschool

วิธีใช้งาน package นี้
~~~~~~~~~~~~~~~~~~~~~~

[STEP 1] - เปิด IDLE ขึ้นมาแล้วพิมพ์...

.. code:: python

    from caketestoopschool import Student,Tesla,SpicialStudent,Teacher
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

พัฒนาโดย: ลุงวิศวกร สอนคำนวณ FB: https://www.facebook.com/UncleEngineer
YouTube: https://www.youtube.com/UncleEngineer
