import os
from mmmint.registration_recognition.sdk import Status, Client
import time
import pytest


class Ressources():
    def __init__(self):
        self.APIKEY = os.environ.get("APIKEY", "")
        self.test_image_path = "sdk/mmmint/test_fahrzeugschein.jpeg"
        self.session_id = "2a9efbec7d93b47e99165f4401d58cfa840d417c7e47074b49a4d2f4d61487f5"
        self.session_created = "2020-12-16 13:44:03.666717"
        self.session_info = ""
        self.session_result = {
            "vorname": "",
            "nachname": "KREIS HETTMANN",
            "strasse": "DUSSELDORFER STRABE 26",
            "stadt": "40822 METTMANN",
            "kennzeichen": "ME-KV-1200",
            "identifizierungsnummer": "",
            "hu_jahr": "",
            "hu_monat": "",
            "erstzulassung_tag": "28",
            "erstzulassung_monat": "01",
            "erstzulassung_jahr": "2016",
            "codehersteller": "0009",
            "codetyp": ""
        }
        self.session_id_corrected = "0e5ec912c19cf8108733c51b2e46164bd297487b4908bd1c103f80720c9115d6"


def test_client_get_sessions_integration():
    ressources = Ressources()

    client = Client(ressources.APIKEY)
    sessions = client.get_sessions()

    for session in sessions:
        if session["session_id"] == ressources.session_id:
            test_session = session

    # found session?
    assert test_session["session_id"] == ressources.session_id
    # found status and is finished?
    assert test_session["status"] == Status.FINISHED.value
    # found creation date?
    assert test_session["created"] == ressources.session_created
    # found info?
    assert test_session["info"] == ressources.session_info

def test_client_get_fahrzeugschein_integration():
    ressources = Ressources()

    client = Client(ressources.APIKEY)

    client.session = ressources.session_id
    clientResult = client.get_fahrzeugschein()

    for key in ressources.session_result.keys():
        assert ressources.session_result[key] == clientResult[key]

def test_new_fahrzeugschein_integration():
    ressources = Ressources()

    # Session started sucessfully?
    client = Client(ressources.APIKEY)
    client.new_fahrzeugschein(ressources.test_image_path)
    assert client.status == Status.STARTED.value

    #Get resulsts or Timeout?
    resultTimeout = Timeout()
    while client.status == Status.STARTED.value and resultTimeout.timeout == False:
        client.get_fahrzeugschein_status()
        resultTimeout.update()
    assert resultTimeout.timeout == False


    #found Fahrzeugschein?
    client.get_fahrzeugschein()
    assert client.status == Status.FINISHED.value
    for key in ressources.session_result.keys():
        if key not in client.fahrzeugschein.keys():
            assert client.fahrzeugschein[key]

class Timeout():

    def __init__(self):
        self.limit = 30
        self.t0 = time.process_time()
        self.t1 = 0
        self.elapsedTime = 0
        self.timeout = False
    
    def update(self):
        time.sleep(2)
        self.t1 = self.t1 + time.process_time()
        self.elapsedTime = self.t1 - self.t0
        if self.elapsedTime > self.limit:
            self.timeout = True

    
