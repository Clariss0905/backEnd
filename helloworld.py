from flask import Flask, request
from flask_cors import CORS
from flask import jsonify
import database
from collections import defaultdict

d = defaultdict(list)
app = Flask(__name__)

CORS(app, supports_credentials=True)


@app.route('/')
def helloworld():
    return "hello world!"


@app.route('/hey/<username>')
def hey(username):
    return "hey %s" % username


@app.route('/insert/<number>', methods=["POST"])
def insert(number):
    database.insert(number)
    return jsonify(msg="提交成功")


# 登录
@app.route('/login', methods=["POST"])
def login():
    get_data = request.get_json()
    print(get_data)
    uid = get_data.get("id")
    password = get_data.get("password")
    info = database.login(uid)
    print(info)
    if not all([uid, password]):
        return jsonify(code=0, msg="参数不完整")
    if uid == info[0][0] and password == info[0][1]:
        return jsonify(code=200, msg="登陆成功", root=info[0][7])
    else:
        return jsonify(code=400, msg="登录失败 ")


# 查询学院
@app.route('/college_info', methods=["GET"])
def college_info():
    info = database.college()
    jsonCollege = []
    for row in info:
        result = {}
        result['college_id'] = row[0]
        result['college_name'] = row[1]
        jsonCollege.append(result)
    return jsonify(jsonCollege)


# 查询专业
@app.route('/major_info', methods=["GET"])
def major_info():
    get_data = request.args['college_id']
    info = database.major(get_data)
    jsonCollege = []
    for row in info:
        result = {}
        result['college_id'] = row[0]
        result['major_id'] = row[1]
        result['major_name'] = row[2]
        jsonCollege.append(result)
    return jsonify(jsonCollege)


# 查询课程
@app.route('/class_info', methods=["GET"])
def class_info():
    get_data = request.args['major_id']
    info = database.class1(get_data)
    jsonCollege = []
    for row in info:
        result = {}
        result['major_id'] = row[0]
        result['class_id'] = row[1]
        result['class_name'] = row[2]
        jsonCollege.append(result)
    return jsonify(jsonCollege)


# 注册
@app.route('/register', methods=["POST"])
def register():
    get_data = request.get_json()
    uid = get_data.get("id")
    password = get_data.get("password")
    age = get_data.get("age")
    sex = get_data.get("sex")
    telephone = get_data.get("telephone")
    class_id = get_data.get("class_id")
    root = get_data.get("root")
    enter_time = get_data.get("enter_time")
    info = database.login(uid)
    if not all([uid, password, age, sex, telephone, class_id, enter_time, root]):
        return jsonify(code=0, msg="参数不完整")
    if info:
        return jsonify(code=500, msg="用户已注册")
    else:
        database.registe(uid, password, age, sex, telephone, class_id, enter_time, root)
        return jsonify(code=200, msg="注册成功")


# 个人信息查询
@app.route('/userInfo', methods=["GET"])
def userInfo():
    global a
    get_data = request.args['userid']
    info = database.login(get_data)
    jsonCollege = []
    for row in info:
        result = {}
        result['id'] = row[0]
        result['password'] = row[1]
        result['age'] = row[2]
        result['sex'] = row[3]
        result['telephone'] = row[4]
        result['class_id'] = row[5]
        result['entry_time'] = row[6]
        jsonCollege.append(result)
    print(jsonCollege[0]['class_id'])
    userInfo = database.userInfo(jsonCollege[0]['class_id'])
    for row in userInfo:
        a = {}
        a['class_name'] = row[0]
        a['major_name'] = row[1]
        a['college_name'] = row[2]
    js = [dict(jsonCollege[0], **a)]
    return jsonify(js)


# 修改个人信息
@app.route('/changeInfo', methods=["POST"])
def changeInfo():
    get_data = request.get_json()
    uid = get_data.get("id")
    telephone = get_data.get("telephone")
    if len(str(telephone)) == 11:
        database.changeInfo(telephone, uid)
        return jsonify(code=200, msg="修改成功")
    else:
        return jsonify(code=500, msg="电话格式不正确")


# 查看课程成绩
@app.route('/searchCourse', methods=["POST"])
def searchCourse():
    get_data = request.get_json()
    uid = get_data.get("id")
    year = int(get_data.get("year"))
    userData = database.login(uid)
    jsonCourse = []
    mark = []
    credit = []
    if (year < userData[0][6] or year > userData[0][6] + 4):
        return jsonify(code=500, msg="年份输入错误")
    else:
        userCourse = database.searchCourse(year, uid)
        for row in userCourse:
            result = {}
            result["course_date"] = row[0]
            result["course_mark"] = row[1]
            result["course_name"] = row[2]
            result["course_credit"] = row[3]
            jsonCourse.append(result)
            mark.append(row[1])
            credit.append(row[3])
        # 计算学生加权平均成绩
        total = round(sum([mark[i] * credit[i] for i in range(len(mark))]) / sum(credit), 1)
        return jsonify([jsonCourse, total])


# 查询奖惩事件
@app.route('/award', methods=["POST"])
def award():
    get_data = request.get_json()
    uid = get_data.get("id")
    year = int(get_data.get("year"))
    userData = database.login(uid)
    jsonAward = []
    if (year < userData[0][6] or year > userData[0][6] + 4):
        return jsonify(code=500, msg="年份输入错误")
    else:
        userAward = database.award(year, uid)
        print(userAward)
        for row in userAward:
            result = {}
            result["award_time"] = row[0].strftime("%Y-%m-%d")  # 处理时间转换格式
            result["award_name"] = row[1]
            if (row[2] == 0):
                result["mark"] = -row[3]
            else:
                result["mark"] = row[3]
            jsonAward.append(result)
        return jsonify(jsonAward)


@app.route('/apply', methods=["POST"])
def Apply():
    get_data = request.get_json()
    print(get_data)
    student_id = get_data.get("student_id")
    award_id = get_data.get("award_id")
    apply_id = get_data.get("apply_id")
    state = get_data.get("state")
    info = get_data.get("info")
    apply_time = get_data.get("apply_time")
    year = get_data.get("year")
    database.apply(student_id, award_id, apply_id, state, info, apply_time, year)
    return jsonify(code=200, msg="提交成功")


@app.route('/searchApply', methods=["GET"])
def searchApply():
    get_data = request.args['userid']
    award = database.searchApply(get_data)
    jsonApply = []
    for row in award:
        result = {}
        result["apply_time"] = row[0].strftime("%Y-%m-%d")  # 处理时间转换格式
        result["award_kind"] = row[1]
        result["info"] = row[2]
        if (row[3] == 0):
            result["state"] = "待审核"
        elif (row[3] == 1):
            result["state"] = "审核通过"
        elif (row[3] == 2):
            result["state"] = "审核未通过"
        jsonApply.append(result)
    print(jsonApply)
    return jsonify(jsonApply)


@app.route('/searchApplyAll', methods=["GET"])
def searchApplyAll():
    award = database.searchApplyAll()
    jsonApply = []
    for row in award:
        result = {}
        result["apply_time"] = row[0].strftime("%Y-%m-%d")  # 处理时间转换格式
        result["award_kind"] = row[1]
        result["info"] = row[2]
        if (row[3] == 0):
            result["state"] = "待审核"
        elif (row[3] == 1):
            result["state"] = "审核通过"
        elif (row[3] == 2):
            result["state"] = "审核未通过"
        result["apply_id"] = row[4]
        result["id"] = row[5]
        jsonApply.append(result)
    print(jsonApply)
    return jsonify(jsonApply)


@app.route('/searchApplyKind', methods=["GET"])
def searchApplyKind():
    data = database.searchApplyKind()
    jsonAwardKind = []
    for row in data:
        result = {}
        result["award_id"] = row[0]
        result["award_name"] = row[1]
        jsonAwardKind.append(result)
    return jsonify(jsonAwardKind)


@app.route('/teacherClass', methods=["GET"])
def teacherClass():
    get_data = request.args['userid']
    info = database.teacherClass(get_data)
    jsonClass = []
    for row in info:
        result = {}
        result["class_name"] = row[0]
        result["class_id"] = row[1]
        jsonClass.append(result)
    return jsonify(jsonClass)


@app.route('/teacherCourse', methods=["GET"])
def teacherCourse():
    teacher_id = request.args['userid']
    class_id = request.args['class_id']
    info = database.teacherCourse(teacher_id, class_id)
    jsonCourse = []
    for row in info:
        result = {}
        result["course_name"] = row[0]
        result["course_id"] = row[1]
        jsonCourse.append(result)
    return jsonify(jsonCourse)


@app.route('/teacherCourseMark', methods=["POST"])
def teacherCourseMark():
    get_data = request.get_json()
    year = get_data.get("year")
    teacher_id = get_data.get("teacher_id")
    class_id = get_data.get("class_id")
    course_id = get_data.get("course_id")
    info = database.teacherCourseMark(year, class_id, course_id, teacher_id)
    json = []
    for row in info:
        result = {}
        result["year"] = row[0]
        result["class_name"] = row[1]
        result["course_name"] = row[2]
        result["student_id"] = row[3]
        result["course_mark"] = row[4]
        json.append(result)
    return jsonify(json)


# 教师录入成绩
@app.route('/updateMark', methods=["POST"])
def updateMark():
    get_data = request.get_json()
    student_id = get_data.get("student_id")
    course_mark = get_data.get("course_mark")
    couser_id = get_data.get("course_id")
    database.updateMark(student_id, course_mark, couser_id)
    return jsonify(code=200, msg="成功")


# 修改申请奖惩状态
@app.route('/updateState', methods=["POST"])
def updateState():
    get_data = request.get_json()
    id = get_data.get("id")
    state = get_data.get("state")
    database.updateState(id, state)
    return jsonify(code=200, msg="成功")


app.run()
