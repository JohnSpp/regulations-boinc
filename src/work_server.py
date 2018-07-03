from flask import Flask, request, Response
import redis
import json
import random
import string
import os
from redis_manager import RedisManager


app = Flask(__name__)

work_key = os.environ['WORK_SERVER_KEY']

r = RedisManager(redis.Redis())


@app.route('/')
def default():
    """
    Default endpoint
    :return: returns empty json
    """
    return json.dumps({})


@app.route('/add_work', methods=['POST'])
def add_work():
    """
    Given a key, job_id, and job_units as parameters in the url, this will add work to the database
    Raises a post exception if the key is incorrect, the job_id is not properly formatted, or if the job_unit is not a list
    :return: ok to say it was successful
    """
    try:
        job_id = request.form['job_id']
        job_units = request.form['job_units']
        received_key = request.form['key']
    except:
        raise PostException
    if received_key != work_key:
        raise PostException
    if len(job_id) != 16:
        raise PostException
    if isinstance(job_units, list):
        raise PostException
    r.add_data(job_id, job_units)
    return 'Ok'


@app.route('/get_data')
def get_data():
    """
    Given a job_id in the url this will loop through the database and find the id that matches the given id
    Raises get exception if there are no parameters or if the job_id is not properly formatted
    :return: the list of urls for the specific job
    """
    if len(request.args) != 1:
        raise GetException
    job_id = request.args.get('job_id')
    if len(job_id) != 16:
        raise GetException
    urls = []
    keys = r.get_job_id_list()
    for id in keys:
        if job_id == id:
            urls = r.get_job_units(id).decode("utf-8")
    return json.dumps(urls)


@app.route('/work_done', methods=['POST'])
def work_done():
    """
    Will delete the work from the database given the job_id and the correct key
    Raises post exception if there are incorrect parameters, incorrect key, or the job_id is formatted incorrectly
    :return: ok if the call was successful
    """
    try:
        job_id = request.form['job_id']
        received_key = request.form['key']
    except:
        raise PostException
    if received_key != work_key:
        raise PostException
    if len(job_id) != 16:
        raise PostException
    r.delete_job(job_id)
    return 'Ok'

# Throw exception of there is an error making a post call
class PostException(Exception):
    print("Bad Request")

# Throw exception if there is an error making the get call
class GetException(Exception):
    print("Bad Request")


if __name__ == '__main__':
    app.run('0.0.0.0',port=5000)