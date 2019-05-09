from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

# globals
endDate = None
startDate = datetime.now()
dateDiff = 0
localMode = False

# instantiate Flask framework
app = Flask(__name__)

@app.route('/')
def index():
    # call globals
    global startDate
    global endDate
    global dateDiff

    # set params and format things
    start = startDate.strftime('%m/%d/%Y %H:%M:%S')
    end = endDate
    diff = dateDiff

    if endDate is not None:
        startDate = datetime.now()
        dateDiff = endDate - startDate
        end = endDate.strftime('%m/%d/%Y %H:%M:%S')
    
    # render template
    return render_template('index.html', start=start, end=end, diff=diff)

@app.route('/get-date-range', methods=['POST'])
def getDateRange():
    # call globals
    global startDate
    global endDate
    global dateDiff

    # start date
    startDate = datetime.now()

    # end date, if date time is not set in post body
    if request.form['end-date'] is not '' and request.form['end-date'] is not None and len(request.form['end-date']) > 0:
        endDate = datetime.strptime(request.form['end-date'], '%Y-%m-%d')
        endDate.replace(minute=0, hour=0, second=0, microsecond=0)
        endDate = endDate + timedelta(hours=7)

    # time difference
    dateDiff = endDate - startDate

    # redirect
    return redirect(url_for('index'))

if __name__ == '__main__':
    # RUN!!!!!
    if localMode == False:
        # allow others to connect
        app.run(host='0.0.0.0', port=9090)
    else:
        # run on localhost
        app.run(port=9090)