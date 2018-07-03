import redis
import threading



class RedisManager:

    def __init__(self, command):
        """
        Initialize the database
        """
        self.r = redis.Redis()
        self.lock = threading.RLock()


    def add_data(self, job_id, job_units):
        """
        Save the job to the database
        :param job_id: id of the job to be saved
        :param job_units: list of job units that will be saved to the database
        :return:
        """
        with self.lock:
            self.r.set(job_id, job_units)

    def get_job_units(self, job_id):
        """
        Get the job units from the database
        :param job_id: id of the job to get from the database
        :return: the list of job units
        """
        return self.r.get(job_id)

    def delete_all(self):
        """
        Delete everything from the database
        """
        self.r.flushall()

    def delete_job(self, job_id):
        """
        Delete a specific item from the database
        :param job_id: id of the job to be deleted
        """
        self.r.delete(job_id)

    def get_job_id_list(self):
        """
        Get a list of the all the job ids in the database
        :return: the list of job ids
        """
        return self.r.keys()

