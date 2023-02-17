import json


class Exam:
    def __init__(self, code, student_list):
        self.code = code
        self.student_list = student_list
        self.no_student = len(student_list)
        self.adjacency_list = []
        self.halls = {}
        self.color = None
        self.day = None

    def color_node(self, color, day):
        self.color = color
        self.day = day


class Room:
    def __init__(self, code, capacity):
        self.code = code
        self.capacity = capacity
        self.available = capacity


def ratio(exam1, exam2):
    common = len(list(set(exam1.student_list).intersection(exam2.student_list)))
    return common / max(exam1.no_student, exam2.no_student)


def create_nodes(file):
    with open('data/' + file) as data_file:
        course_data = json.load(data_file)
    exams = []
    for course in course_data.keys():
        if len(course_data[course]) > 0:
            exam = Exam(code=course, student_list=course_data[course])
            exams.append(exam)
    return exams


def create_map(exams):
    size = len(exams)
    exams.sort(key=lambda x: x.no_student, reverse=True)
    for i in range(size):
        exam = exams[i]
        for j in range(size):
            if j != i:
                rat = ratio(exam, exams[j])
                if rat > 0:
                    exam.adjacency_list.append([j, rat])
    return exams


def color_map(exams, num_of_day, num_of_period, max_ratio, max_of_exam):
    exams.sort(key=lambda x: x.no_student, reverse=True)
    for day in range(num_of_day):
        for exam in exams:
            if exam.color != None:
                continue
            colors = [i for i in range(num_of_period)]
            in_day_rat = 0
            for a in exam.adjacency_list:
                ex = exams[a[0]]
                if (ex.color != None) and (ex.day == day):
                    try:
                        colors.remove(ex.color)
                    except:
                        print(color, colors)
                    finally:
                        if a[1] > in_day_rat:
                            in_day_rat = a[1]

            if in_day_rat < max_ratio:
                for color in colors:
                    count = sum(map(lambda x: x.color == color and x.day == day, exams))
                    if count < max_of_exam:
                        exam.color_node(color=color, day=day)
                        break
    return exams


def create_halls(file):
    with open('data/' + file) as data_file:
        hall_data = json.load(data_file)
    halls = []
    for key in hall_data.keys():
        room = Room(code=key, capacity=hall_data[key])
        halls.append(room)
    return halls


def finding_hall(exams, no_day, no_period, halls):
    for i in range(no_day):
        for j in range(no_period):
            for hall in halls:
                hall.available = hall.capacity

            in_slot_exams = list(filter(lambda e: e.day == i and e.color == j, exams))
            in_slot_exams.sort(key=lambda x: x.no_student)
            halls.sort(key=lambda x: x.capacity)

            for exam in in_slot_exams:
                exam_remain = exam.no_student
                # có phòng lớn hơn hoặc băng số thí sinh
                for hall in halls:
                    if hall.available >= exam_remain:
                        hall.available = hall.available - exam_remain
                        exam.halls[hall.code] = exam_remain
                        exam_remain = 0
                        break
                # không có phòng nào lớn hơn số thí sinh
                while exam_remain > 0:
                    count = 0
                    for hall in halls:
                        if hall.available == 0:
                            count += 1
                            if count == len(halls) and exam_remain > 0:
                                print(f"Số lượng phòng ko đủ tổ cho buoi thi {j+1} ngay {i+1}")
                                exam_remain = 0
                            else:
                                continue
                        elif exam_remain > hall.available:
                            exam.halls[hall.code] = hall.available
                            exam_remain -= hall.available
                            hall.available = 0
                        else:
                            hall.available = hall.available - exam_remain
                            exam.halls[hall.code] = exam_remain
                            exam_remain = 0


    return exams


if __name__ == "__main__":
    num_of_day = 3
    max_of_exam = 2
    num_of_period = 2
    max_ratio = 0.34
    file = 'test_data.json'
    exams = create_nodes(file)
    exams = create_map(exams)
    exams = color_map(exams, num_of_day, num_of_period, max_ratio, max_of_exam)
    halls = create_halls('test_halls.json')
    exams = finding_hall(exams, num_of_day, num_of_period, halls)
    exams.sort(key=lambda x: (x.day, x.color))
    for exam in exams:
        print(exam.code, f"ngay:{exam.day + 1}", f"slot: {exam.color + 1}", f"{exam.halls}")
