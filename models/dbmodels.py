__author__ = "Enku Wendwosen<enku@singularitynet.io>"

import os


class Session:
    """
    A class that represents a single run of the MOSES analysis
    """

    def __init__(self, id, mnemonic, annotations, genes):
        self.id = id
        self.status = 0
        self.message = ""
        self.start_time = 0
        self.end_time = 0
        self.mnemonic = mnemonic
        self.annotations = annotations
        self.genes = genes
        self.result = None
        self.result_file = None
        self.csv_file = None
        self.expired = False

    def save(self, db):
        """
        Save the session into a database
        :param db: The database to insert the session into
        :return:
        """
        data = self.__dict__
        db["sessions"].insert_one(data)

    def delete_session(self, db):
        db["sessions"].delete_one({"id": self.id})


    def update_session(self, db):
        data = self.__dict__
        db["sessions"].update_one({
            "id": self.id
        }, {
            "$set": data
        })

    @staticmethod
    def get_session(db, session_id=None, mnemonic=None):
        """
        Get a session using its id or mnemonic from a database
        :param db: the db in which the session is found
        :param session_id: the id of the session
        :param mnemonic: the mnemonic value for the session derived from its uuid
        :return: A session object
        """
        result = None
        if session_id:
            result = db["sessions"].find_one({
                "id": session_id
            })

        elif mnemonic:
            result = db["sessions"].find_one({
                "mnemonic": mnemonic
            })

        if result:
            session = Session(result["id"],result["mnemonic"],result["annotations"],result["genes"])
            session.status = result["status"]
            session.message = result["message"]
            session.start_time = result["start_time"]
            session.end_time = result["end_time"]
            session.result = result["result"]
            session.result_file = result["result_file"]
            session.csv_file = result["csv_file"]
            session.expired = result["expired"]
            session.annotations = result['annotations']
            session.genes = result['genes']

            return session

        return result
