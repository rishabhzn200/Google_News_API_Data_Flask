# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# "Project Name"        :   "NewsData"                                  #
# "File Name"           :   "flaskmain"                                 #
# "Author"              :   "rishabhzn200"                              #
# "Date of Creation"    :   "Jan-07-2019"                               #
# "Time of Creation"    :   "21:08"                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from flask import Flask, render_template, request, Response, jsonify
from mainfile import *
app = Flask(__name__)


def stream_template(template_name, **context):
    """

    :param template_name: name of the template to stream
    :param context: context
    :return:
    """
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    return rv



@app.route('/')
@app.route('/index')
def index():
    """

    :return: result of render_template
    """
    if request.method == 'POST':
        result = request.form
        print(result)
    companies = ['Facebook', 'Okta', 'Xactly', 'WeWork', '8 x 8', 'SynapseFI', 'Apptemize', 'Uber', 'Gusto', 'HelloSign']
    return render_template('index.html', companies=companies)


@app.route('/result',methods = ['POST', 'GET'])
def result():
    """

    :return: result of render_template
    """
    query_string = None
    if request.method == 'POST':
        result = request.form
        for key, value in result.items():
            if key == 'companies':
                query_string = value

    elif request.method == 'GET':
        query_string = request.args.get('companies', '')
    else:
        return render_template("result.html",result = ['Empty Query String'])

    return Response(stream_template('result.html', result=main(query_string)))


if __name__ == '__main__':
    app.run(debug = True)