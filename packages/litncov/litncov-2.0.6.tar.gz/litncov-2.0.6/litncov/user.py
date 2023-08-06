#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests
import json

from litncov import endpoints
from litncov import util


class litUesr:
    """lit uesr object"""

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = util.get_sha256(password)

        self.__headers = {
            "Connection": "keep-alive",
            "Content-Type": "application/json",
        }

        # login the acconut
        try:
            self.login = self.__login()
        except:
            self.info = None

        # get the user info
        try:
            self.info = self.login["data"]
        except:
            self.info = None

        # update some values
        try:
            self.__headers["token"] = self.info["token"]
            self.is_logged = True
        except:
            self.is_logged = False

        # init last record info
        self.last_record = None

    def __login(self):
        data = {"cardNo": self.username, "password": self.password}

        # login func
        try:
            response = requests.post(
                url=endpoints["login"], data=json.dumps(data), headers=self.__headers
            )
        except:
            return None

        res = response.json()

        return res

    def get_last_record(self):
        data = {"teamId": self.info["teamId"], "userId": self.info["userId"]}

        try:
            response = requests.get(
                url=endpoints["lastRecord"], params=data, headers=self.__headers
            )
        except:
            return None

        res = response.json()

        return res

    def fetch_last_record(self):
        if self.last_record == None or util.is_outdate_last_record(self.last_record):
            self.last_record = self.get_last_record()["data"]

        return self.last_record

    def is_record_today(self, rtime=1):
        last_record = self.fetch_last_record()

        if last_record["createTime"][0:10] == util.get_today_time():

            if rtime == 1:
                return True
            elif (rtime == 2) & (self.last_record["temperatureTwo"] != ""):
                return True
            elif (rtime == 3) & (self.last_record["temperatureThree"] != ""):
                return True
        else:
            return False

    def get_instructor(self):
        data = {
            "teamId": self.info["teamId"],
            "organizationName": self.info["organizationName"],
            "userOrganizationId": self.info["userOrganizationId"],
        }

        try:
            response = requests.get(
                url=endpoints["getInstructor"], params=data, headers=self.__headers
            )
        except:
            return None

        res = response.json()

        return res

    def get_familys(self):
        data = {
            "userId": self.info["userId"],
        }

        try:
            response = requests.get(
                url=endpoints["getFamilys"], params=data, headers=self.__headers
            )
        except:
            return None

        res = response.json()

        return res

    def get_important_city(self):
        try:
            response = requests.get(
                url=endpoints["getImportantCity"], headers=self.__headers
            )
        except:
            return None

        res = response.json()
        return res

    def get_trips(self):
        data = {
            "userId": self.info["userId"],
            "teamId": self.info["teamId"],
        }

        try:
            response = requests.get(
                url=endpoints["getTrips"], params=data, headers=self.__headers
            )
        except:
            return None

        res = response.json()

        return res

    def query_record(self, st=util.get_today_time, et=util.get_today_time):
        data = {
            "pageNum": 1,
            "pageSize": 20,
            "userId": self.info["userId"],
            "teamId": self.info["teamId"],
            "startTime": st,
            "endTime": et,
        }

        try:
            response = requests.get(
                url=endpoints["queryRecord"], params=data, headers=self.__headers
            )
        except:
            return None

        res = response.json()

        return res

    def first_record(
        self,
        mode="last",
        rtimes=1,
        temperature=36.1,
        temperatureTwo=36.2,
        temperatureThree=36.3,
    ):
        """
        the 'normal' will not record the temperatureTwo and temperatureThree values from last record
        and you can use the 'manual' for use your values, 'random' use random values
        """

        # get the last record info
        last_record = self.fetch_last_record()

        data = {
            "mobile": self.info["mobile"],
            "nativePlaceProvince": self.info["nativePlaceProvince"],
            "nativePlaceCity": self.info["nativePlaceCity"],
            "nativePlaceDistrict": self.info["nativePlaceDistrict"],
            "nativePlaceAddress": self.info["nativePlaceAddress"],
            "localAddress": self.info["localAddress"],
            "currentProvince": last_record["currentProvince"],
            "currentCity": last_record["currentCity"],
            "currentDistrict": last_record["currentDistrict"],
            "currentLocation": util.current_location(
                last_record["currentDistrict"], last_record["currentCity"]
            ),
            "currentAddress": last_record["currentAddress"],
            "villageIsCase": last_record["villageIsCase"],
            "caseAddress": last_record["caseAddress"],
            "peerIsCase": last_record["peerIsCase"],
            "peerAddress": last_record["peerAddress"],
            "isInTeamCity": last_record["isInTeamCity"],
            "temperatureNormal": last_record["temperatureNormal"],
            "temperature": last_record["temperature"],
            "selfHealthy": last_record["selfHealthy"],
            "selfHealthyInfo": last_record["selfHealthyInfo"],
            "selfHealthyTime": last_record["selfHealthyTime"],
            "friendHealthy": last_record["friendHealthy"],
            "isolation": last_record["isolation"],
            "currentStatus": last_record["currentStatus"],
            "diagnosisTime": last_record["diagnosisTime"],
            "treatmentHospitalAddress": last_record["treatmentHospitalAddress"],
            "cureTime": last_record["cureTime"],
            "travelPatient": last_record["travelPatient"],
            "goHuBeiCity": last_record["goHuBeiCity"],
            "goHuBeiTime": last_record["goHuBeiTime"],
            "contactPatient": last_record["contactPatient"],
            "contactTime": last_record["contactTime"],
            "contactProvince": last_record["contactProvince"],
            "contactCity": last_record["contactCity"],
            "contactDistrict": last_record["contactDistrict"],
            "contactLocation": "",  # temporary emtpy
            "contactAddress": last_record["contactAddress"],
            "isAbroad": last_record["isAbroad"],
            "abroadInfo": last_record["abroadInfo"],
            "seekMedical": last_record["seekMedical"],
            "seekMedicalInfo": last_record["seekMedicalInfo"],
            "exceptionalCase": last_record["exceptionalCase"],
            "exceptionalCaseInfo": last_record["exceptionalCaseInfo"],
            "isTrip": last_record["isAbroad"],  # temporary use
            "userId": self.info["userId"],
            "teamId": self.info["teamId"],
            "healthyStatus": last_record["healthyStatus"],
            "temperatureTwo": "",
            "temperatureThree": "",
            "reportDate": util.get_today_time(),
        }

        if mode == "last":
            if rtimes >= 2:
                data["temperatureTwo"] = last_record["temperatureTwo"]
            if rtimes == 3:
                data["temperatureThree"] = last_record["temperatureThree"]
        elif mode == "random":
            data["temperature"] = util.random_temp()
            if rtimes >= 2:
                data["temperatureTwo"] = util.random_temp()
            if rtimes == 3:
                data["temperatureThree"] = util.random_temp()
        elif mode == "manual":
            data["temperature"] = temperature
            if rtimes >= 2:
                data["temperatureTwo"] = temperatureTwo
            if rtimes == 3:
                data["temperatureThree"] = temperatureThree
        else:
            return None

        try:
            response = requests.post(
                url=endpoints["firstRecord"],
                data=json.dumps(data),
                headers=self.__headers,
            )
            # res['data']['temperature'] = data['temperature']
            # res['data']['temperatureTwo'] = data['temperatureTwo']
            # res['data']['temperatureThree'] = data['temperatureThree']
            # {"success":true,"code":200,"msg":"请求成功","data":""}
        except:
            return None

        res = response.json()

        res["data"] = {"temperature": data["temperature"]}
        if rtimes >= 2:
            res["data"]["temperatureTwo"] = data["temperatureTwo"]
        if rtimes == 3:
            res["data"]["temperatureThree"] = data["temperatureThree"]

        return res

    def second_record(self, mode="last", temperature=36.6):
        """
        mode: 'last', 'random' and 'manual'
        """

        # get the last record info
        last_record = self.fetch_last_record()

        data = {
            "healthyRecordId": last_record["id"],
            "temperature": last_record["temperatureTwo"],
            "temperatureNormal": last_record["temperatureNormal"],
        }

        if mode == "last":
            pass
        elif mode == "random":
            data["temperature"] = util.random_temp()
        elif mode == "manual":
            data["temperature"] = temperature
        else:
            return None

        try:
            response = requests.put(
                url=endpoints["secondRecord"], params=data, headers=self.__headers
            )
        except:
            return None

        res = response.json()
        res["data"] = {"temperature": data["temperature"]}

        return res

    def third_record(self, mode="last", temperature=36.6):
        """
        mode: 'last', 'random' and 'manual'
        """

        # get the last record info
        last_record = self.fetch_last_record()

        data = {
            "healthyRecordId": last_record["id"],
            "temperature": last_record["temperatureThree"],
            "temperatureNormal": last_record["temperatureNormal"],
        }

        if mode == "last":
            pass
        elif mode == "random":
            data["temperature"] = util.random_temp()
        elif mode == "manual":
            data["temperature"] = temperature
        else:
            return None

        try:
            response = requests.put(
                url=endpoints["thirdRecord"], params=data, headers=self.__headers
            )
        except:
            return None

        res = response.json()
        res["data"] = {"temperature": data["temperature"]}

        return res

    def change_password(self, psw: str):
        """
        for changes your password
        """
        data = {"password": util.get_sha256(psw)}

        try:
            response = requests.put(
                url=endpoints["password"], params=data, headers=self.__headers
            )
        except:
            return None

        res = response.json()

        return res
