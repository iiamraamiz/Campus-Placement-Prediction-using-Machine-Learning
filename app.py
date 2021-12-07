from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)
salary = pickle.load(open('Package.pkl', 'rb'))
placed = pickle.load(open('Placement.pkl', 'rb'))

@app.route('/',methods=['GET','POST'])
def homePage():
    return render_template('base.html')

@app.route('/output', methods=['GET', 'POST'])
def compute():
    global cols, salary, placed
    if request.method == 'POST':
        try:
            age = int(request.form['Age'])
            cgpa = int(request.form['CGPA'])
            coding = int(request.form['Coding'])
            comms = int(request.form['comms'])
            intern = int(request.form['intern'])
            backsStr = request.form['backs']
            branches = request.form['branch']
            genderName = request.form['gender']
            if backsStr == 'Yes':
                backs = 1
            elif backsStr == 'No':
                backs = 0
            if branches == 'CSE':
                branch = [1, 0, 0, 0, 0]
            elif branches == 'EEE':
                branch = [0, 1, 0, 0, 0]
            elif branches == 'ECE':
                branch = [0, 0, 1, 0, 0]
            elif branches == 'IT':
                branch = [0, 0, 0, 1, 0]
            elif branches == 'ME':
                branch = [0, 0, 0, 0, 1]
            elif branches == 'CE':
                branch = [0, 0, 0, 0, 0]
            if genderName == 'Male':
                gender = 1
            elif genderName == 'Female':
                gender = 0
            inp = [age, gender, cgpa, coding, comms, intern, backs]
            inp.extend(branch)
            inpData = pd.DataFrame(columns=cols)
            inpData.loc[0] = inp
            prediction = placed.predict(inpData)[0]
            if prediction == 1:
                prediction = 'Will Be Placed'
                salaryPred = f'{int(salary.predict(inpData)[0])} LPA'
                prediction = f'{prediction} With Package {salaryPred}'
            else:
                prediction = 'Will Not Be Placed'
                salaryPred = 'None'
        except:
            prediction = 'Invalid Input'
            age = 0
            gender = 'none'
            branches = 'none'
    return render_template('finalOutput.html',
            prediction=prediction,
            age=age,
            branch=branches,
            gender=genderName,
            cgpa=cgpa,
            coding=coding,
            comms=comms,
            intern=intern,
            back=backsStr)

if __name__ == '__main__':
    cols = ['Age', 'Gender', 'CGPA', 'Coding Skills', 'Communication Skills',
                'Internships', 'HistoryOfBacklogs', 'Computer Science', 'Electrical',
                'Electronics And Communication', 'Information Technology',
                'Mechanical']
    app.run(debug=True)