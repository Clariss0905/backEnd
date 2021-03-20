from turtle import pd

from flask import Flask
import pymysql
import threading

app = Flask(__name__)

db = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',  # 用户名
    password='WL3624320019',  # 密码
    database='bishe',  # 数据库的名字
    charset='utf8'
)
lock = threading.Lock()


# 插入id
def insert(data):
    cursor = db.cursor()
    sql = "insert into user values(" + data + ")"
    cursor.execute(sql)
    db.commit()
    return


# 数据库返回登录参数
def login(uid):
    cursor = db.cursor()
    sql = "SELECT *FROM user WHERE (id='" + str(uid) + "')"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


# 数据库查询学院信息
def college():
    cursor = db.cursor()
    sql = "SELECT *FROM college"
    lock.acquire()
    cursor.execute(sql)
    lock.release()
    result = cursor.fetchall()
    return result


# 数据库查询专业信息
def major(college_id):
    cursor = db.cursor()
    sql = "SELECT *FROM major WHERE (college_id=" + str(college_id) + ")"
    lock.acquire()
    cursor.execute(sql)
    lock.release()
    result = cursor.fetchall()
    return result


# 数据库查询专业信息
def class1(major_id):
    cursor = db.cursor()
    sql = "SELECT *FROM class WHERE (major_id=" + str(major_id) + ")"
    lock.acquire()
    cursor.execute(sql)
    lock.release()
    result = cursor.fetchall()
    return result


# 注册用户
def registe(uid, password, age, sex, telephone, class_id, enter_time, root):
    cursor = db.cursor()
    sql = "insert user values(" + str(uid) + "," + str(password) + "," + str(age) + "," + str(sex) + "," + str(
        telephone) + "," + str(class_id) + "," + str(enter_time) + "," + str(root) + ")"
    lock.acquire()
    cursor.execute(sql)
    lock.release()
    db.commit()
    return


# 查询专业
def userInfo(class_id):
    cursor = db.cursor()
    sql = "SELECT class_name,major_name,college_name from class,major,college WHERE class.major_id = major.major_id and major.college_id = college.college_id and class_id =" + str(
        class_id)
    lock.acquire()
    cursor.execute(sql)
    lock.release()
    result = cursor.fetchall()
    return result


# 修改个人信息
def changeInfo(telephone, uid):
    cursor = db.cursor()
    sql = "UPDATE user SET telephone = " + str(telephone) + " WHERE id = " + str(uid)
    lock.acquire()
    cursor.execute(sql)
    lock.release()
    db.commit()
    return


# 查看学生学年成绩
def searchCourse(year, uid):
    cursor = db.cursor()
    sql = "SELECT student_course.course_date, student_course.course_mark, course.course_name, course.course_credit FROM student_course, course WHERE student_course.course_id = course.course_id AND course_date = " + str(
        year) + "  AND student_course.student_id = " + str(uid)
    lock.acquire()
    cursor.execute(sql)
    lock.release()
    result = cursor.fetchall()
    return result


# 奖惩事件查询
def award(year, uid):
    cursor = db.cursor()
    sql = "SELECT student_award.award_time,	awrad.award_name, award_kind, awrad.mark FROM awrad, student_award WHERE awrad.award_id = student_award.award_id AND student_award.student_id = " + str(
        uid) + " AND student_award.`year` = " + str(year)
    lock.acquire()
    cursor.execute(sql)
    lock.release()
    result = cursor.fetchall()
    return result


# 奖惩申请
def apply(student_id, award_id, apply_id, state, info, apply_time, year):
    cursor = db.cursor()
    sql = "INSERT INTO apply_award(student_id,award_id,apply_id,state,info,apply_time,apply_award.`year`) VALUES (" + str(
        student_id) + "," + str(award_id) + "," + str(apply_id) + "," + str(state) + "," + "'" + str(
        info) + "'" + "," + "'" + apply_time + "'" + "," + str(year) + ")"
    lock.acquire()
    cursor.execute(sql)
    lock.release()
    db.commit()
    return


# 查询奖惩申请情况
def searchApply(uid):
    cursor = db.cursor()
    sql = "SELECT apply_award.apply_time,awrad.award_name,apply_award.info,apply_award.state FROM apply_award, awrad WHERE awrad.award_id = apply_award.award_id AND student_id=" + str(
        uid)
    lock.acquire()
    cursor.execute(sql)
    lock.release()
    result = cursor.fetchall()
    cursor.close()
    return result


# 查询奖惩申请情况
def searchApplyAll():
    cursor = db.cursor()
    sql = "SELECT apply_award.apply_time,awrad.award_name,apply_award.info,apply_award.state, apply_award.apply_id, apply_award.id FROM apply_award, awrad WHERE awrad.award_id = apply_award.award_id"
    lock.acquire()
    cursor.execute(sql)
    lock.release()
    result = cursor.fetchall()
    cursor.close()
    return result


# 奖惩详细类型查询
def searchApplyKind():
    cursor = db.cursor()
    sql = "SELECT award_id,award_name FROM awrad"
    lock.acquire()
    cursor.execute(sql)
    lock.release()
    result = cursor.fetchall()
    cursor.close()
    return result


# 教师所教的班
def teacherClass(teacher_id):
    cursor = db.cursor()
    sql = "SELECT DISTINCT 	class.class_name, class.class_id FROM class, course, class_course WHERE course.course_id = class_course.course_id AND class_course.class_id = class.class_id AND course.course_teacher = " + str(
        teacher_id)
    lock.acquire()
    cursor.execute(sql)
    lock.release()
    result = cursor.fetchall()
    return result


# 教师所教的课程
def teacherCourse(teacher_id, class_id):
    cursor = db.cursor()
    sql = "SELECT course.course_name, course.course_id FROM course, class_course WHERE course.course_id = class_course.course_id AND course.course_teacher = " + str(
        teacher_id) + " AND class_course.class_id = " + str(class_id)
    lock.acquire()
    cursor.execute(sql)
    lock.release()
    result = cursor.fetchall()
    return result


# 教师选择班级课程后返回对应表格
def teacherCourseMark(year, class_id, course_id, teacher_id):
    cursor = db.cursor()
    sql = "SELECT `user`.entry_date, class.class_name, course.course_name, `user`.id, student_course.course_mark FROM `user`, student_course, course, class WHERE `user`.class_id = class.class_id AND student_course.course_id = course.course_id AND `user`.entry_date = " + str(
        year) + " AND `user`.class_id = " + str(class_id) + " AND course.course_teacher = " + str(
        teacher_id) + " AND student_course.course_id = " + str(course_id)
    lock.acquire()
    cursor.execute(sql)
    lock.release()
    result = cursor.fetchall()
    return result


# 教师录入学生成绩
def updateMark(student_id, course_mark, course_id):
    cursor = db.cursor()
    sql = "UPDATE student_course SET course_mark = " + str(course_mark) + " WHERE student_id = " + str(
        student_id) + " AND course_id = " + str(course_id)
    lock.acquire()
    cursor.execute(sql)
    lock.release()
    db.commit()
    return


# 修改申请奖惩状态
def updateState(id, state):
    cursor = db.cursor()
    sql = "UPDATE apply_award SET state = " + str(state) + " WHERE id = " + str(
        id)
    lock.acquire()
    cursor.execute(sql)
    lock.release()
    db.commit()
    return
