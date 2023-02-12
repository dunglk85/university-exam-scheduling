import json


class Exam:
    def __init__(self, code, student_list):
        self.code = code
        self.student_list = student_list
        self.adjacency_list = []
        self.color = None
        self.day = None

    def color_node(self, color, day):
        self.color = color
        self.day = day


class Room:
    def __init__(self, code, capacity):
        self.code = code
        self.exams = []
        self.capacity = capacity


def ratio(exam1, exam2):
    common = len(list(set(exam1.student_list).intersection(exam2.student_list)))
    return common / max(len(exam1.student_list), len(exam2.student_list))


def create_nodes(file):
    with open('data/' + file) as data_file:
        course_data = json.load(data_file)
        # print(type(course_data))
    exams = []
    for course in course_data.keys():
        if len(course_data[course])>0:
            exam = Exam(code=course, student_list=course_data[course])
            exams.append(exam)
    return exams

def create_map(node_list):
    for exam in node_list:
        for i in range(len(node_list)):
            rat = ratio(exam, node_list[i])
            if rat > 0 and rat != 1:
                exam.adjacency_list.append([i, rat])
    return node_list


def color_map(exams, num_of_day, num_of_period, max_ratio, max_of_exam):
    for day in range(num_of_day):
        for exam in exams:
            if exam.color != None:
                continue
            colors = [i for i in range(num_of_period)]
            in_day_rat = 0
            exam.code
            for a in exam.adjacency_list:
                ex = exams[a[0]]
                ex.code
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
            # if is_color:
            #     break
    return exams


if __name__ == "__main__":
    num_of_day = 3
    max_of_exam = 2
    num_of_period = 2
    max_ratio = 0.34
    file = 'test_data.json'
    exams = create_nodes(file)
    exams.sort(key=lambda x: len(x.student_list), reverse=True)
    exams = create_map(exams)
    exams = color_map(exams, num_of_day, num_of_period, max_ratio, max_of_exam)
    exams.sort(key=lambda x: x.day)
    for exam in exams:
        print(exam.code, f"ngay:{exam.day + 1}", f"slot: {exam.color+1}")
