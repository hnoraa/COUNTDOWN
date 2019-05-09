from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

# globals
endDate = None
startDate = datetime.now()
dateDiff = 0
localMode = True
port = 9091
host = '0.0.0.0'

# date formats
fullDate = '%m/%d/%Y %H:%M:%S'
smallDate = '%Y-%m-%d'

# instantiate Flask framework
app = Flask(__name__)

# index url
@app.route('/')
def index():
    # call globals
    global startDate
    global endDate
    global dateDiff

    # update globals and format things
    start = startDate.strftime(fullDate)
    end = endDate
    diff = dateDiff

    if endDate is not None:
        # if the date is not null, user has clicked submit with non-empty date
        # update the startDate to now and update dateDiff
        startDate = datetime.now()
        dateDiff = endDate - startDate
        end = endDate.strftime(fullDate)

    if dateDiff == 0:
        # countdown has reached end
        diff = 'END!!!'
        endDate = None
        startDate = datetime.now()
    
    # render template
    return render_template('index.html', start=start, end=end, diff=diff)

# get-date-range POST url
@app.route('/get-date-range', methods=['POST'])
def getDateRange():
    # call globals
    global startDate
    global endDate
    global dateDiff

    # update start date
    startDate = datetime.now()

    # update end date, if date time is not set in post body
    if request.form['end-date'] is not '' and request.form['end-date'] is not None and len(request.form['end-date']) > 0:
        endDate = datetime.strptime(request.form['end-date'], smallDate)
        endDate.replace(minute=0, hour=0, second=0, microsecond=0)
        endDate = endDate + timedelta(hours=7)

    # get time difference
    dateDiff = endDate - startDate

    # redirect
    return redirect(url_for('index'))

if __name__ == '__main__':
    # RUN!!!!!
    if localMode == False:
        # allow others to connect
        print('COUNTDOWN Running from Server...')
        app.run(host=host, port=port)
    else:
        # run on localhost
        print('COUNTDOWN Running on Localhost for DEV!')
        app.run(port=port)