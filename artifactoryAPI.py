#!/usr/bin/env python

import os
import json
import requests
import logging

# uncomment the following line, if needed, to avoid SSL missing certificate warnings
# logging.getLogger("urllib3").setLevel(logging.ERROR)

class ArtifactoryAPI:
    
    def __init__(self, serverBase, username, password):
        self.ARTIFACTORY_MGMT_URI = serverBase + "/api/"
        self.USER = username
        self.PASSWORD = password
    
    def artifactory_information(self):
        r = requests.get(
            self.ARTIFACTORY_MGMT_URI + "system",
            verify=False,  # do not check certificate
            auth=(self.USER, self.PASSWORD))
        return r.text

    def artifactory_health(self):
        r = requests.get(
            self.ARTIFACTORY_MGMT_URI + "system/ping",
            verify=False,  # do not check certificate
            auth=(self.USER, self.PASSWORD))
        return r.text

    def artifactory_configuration(self):
        r = requests.get(
            self.ARTIFACTORY_MGMT_URI + "system/configuration",
            verify=False,  # do not check certificate
            auth=(self.USER, self.PASSWORD))
        return r.text

    def license_information(self):
        r = requests.get(
            self.ARTIFACTORY_MGMT_URI + "system/license",
            verify=False,  # do not check certificate
            auth=(self.USER, self.PASSWORD))
        return r.json()
        
    def license_install(self, licenseData):
        requestHeaders = {'Content-Type': 'application/json'}
        r = requests.put(
                self.ARTIFACTORY_MGMT_URI + "system/license",
                headers=requestHeaders,
                data=licenseData,
                verify=False,  # do not check certificate
                auth=(self.USER, self.PASSWORD))
        return r.json()
    
    def repositories_list(self, repoType):
        query = (("?type=" + repoType) if repoType else "")
        print('repoType:'+str(repoType))
        print('query:'+str(query))
        r = requests.get(
                self.ARTIFACTORY_MGMT_URI + "repositories" + query,
                verify=False,  # do not check certificate
                auth=(self.USER, self.PASSWORD))
        return r.json()
    
    def repositories_detail(self, key):
        r = requests.get(
                self.ARTIFACTORY_MGMT_URI + "repositories/" + key,
                verify=False,  # do not check certificate
                auth=(self.USER, self.PASSWORD))
        return r.json()
    
    def repositories_create(self, key, payload):
        requestHeaders = {'Content-Type': 'application/json'}
        r = requests.put(
                self.ARTIFACTORY_MGMT_URI + "repositories/" + key,
                headers=requestHeaders,
                data=json.dumps(payload),
                verify=False,  # do not check certificate
                auth=(self.USER, self.PASSWORD))
        return r.status_code

    def repositories_update(self, key, payload):
        requestHeaders = {'Content-Type': 'application/json'}
        r = requests.post(
                self.ARTIFACTORY_MGMT_URI + "repositories/" + key,
                headers=requestHeaders,
                data=json.dumps(payload),
                verify=False,  # do not check certificate
                auth=(self.USER, self.PASSWORD))
        return r.status_code

    def repositories_delete(self, key):
        r = requests.delete(
            self.ARTIFACTORY_MGMT_URI + "repositories/" + key,
            verify=False,  # do not check certificate
            auth=(self.USER, self.PASSWORD))
        return r.status_code

    def users_list(self):
        r = requests.get(
            self.ARTIFACTORY_MGMT_URI + "security/users",
            verify=False,  # do not check certificate
            auth=(self.USER, self.PASSWORD))
        return r.json()

    def users_detail(self, name):
        r = requests.get(
            self.ARTIFACTORY_MGMT_URI + "security/users/" + name,
            verify=False,  # do not check certificate
            auth=(self.USER, self.PASSWORD))
        return r.json()

    def users_create(self, name, payload):
        requestHeaders = {'Content-Type': 'application/json'}
        requestParameters = {'username': name}
        r = requests.put(
                self.ARTIFACTORY_MGMT_URI + "security/users/" + name,
                headers=requestHeaders,
                params=requestParameters,
                data=json.dumps(payload),
                verify=False,  # do not check certificate
                auth=(self.USER, self.PASSWORD))
        return r.status_code
    
    def users_update(self, name, payload):
        requestHeaders = {'Content-Type': 'application/json'}
        requestParameters = {'username': name}
        r = requests.post(
                self.ARTIFACTORY_MGMT_URI + "security/users/" + name,
                headers=requestHeaders,
                params=requestParameters,
                data=json.dumps(payload),
                verify=False,  # do not check certificate
                auth=(self.USER, self.PASSWORD))
        return r.status_code
    
    def users_delete(self, name):
        r = requests.delete(
            self.ARTIFACTORY_MGMT_URI + "security/users/" + name,
            verify=False,  # do not check certificate
            auth=(self.USER, self.PASSWORD))
        return r.status_code

    def groups_list(self):
        r = requests.get(
            self.ARTIFACTORY_MGMT_URI + "security/groups",
            verify=False,  # do not check certificate
            auth=(self.USER, self.PASSWORD))
        return r.json()

    def groups_detail(self, name):
        r = requests.get(
            self.ARTIFACTORY_MGMT_URI + "security/groups/" + name,
            verify=False,  # do not check certificate
            auth=(self.USER, self.PASSWORD))
        return r.json()

    def groups_create(self, name, payload):
        requestHeaders = {'Content-Type': 'application/json'}
        requestParameters = {'groupname': name}
        r = requests.put(
                self.ARTIFACTORY_MGMT_URI + "security/groups/" + name,
                headers=requestHeaders,
                params=requestParameters,
                data=json.dumps(payload),
                verify=False,  # do not check certificate
                auth=(self.USER, self.PASSWORD))
        return r.status_code
    
    def groups_update(self, name, payload):
        requestHeaders = {'Content-Type': 'application/json'}
        requestParameters = {'groupname': name}
        r = requests.post(
                self.ARTIFACTORY_MGMT_URI + "security/groups/" + name,
                headers=requestHeaders,
                params=requestParameters,
                data=json.dumps(payload),
                verify=False,  # do not check certificate
                auth=(self.USER, self.PASSWORD))
        return r.status_code
    
    def groups_delete(self, name):
        r = requests.delete(
            self.ARTIFACTORY_MGMT_URI + "security/groups/" + name,
            verify=False,  # do not check certificate
            auth=(self.USER, self.PASSWORD))
        return r.status_code

    def permissions_list(self):
        r = requests.get(
            self.ARTIFACTORY_MGMT_URI + "security/permissions",
            verify=False,  # do not check certificate
            auth=(self.USER, self.PASSWORD))
        return r.json()

    def permissions_detail(self, name):
        r = requests.get(
            self.ARTIFACTORY_MGMT_URI + "security/permissions/" + name,
            verify=False,  # do not check certificate
            auth=(self.USER, self.PASSWORD))
        return r.json()

    def permissions_create(self, name, payload):
        requestHeaders = {'Content-Type': 'application/json'}
        requestParameters = {'permissionname': name}
        r = requests.put(
                self.ARTIFACTORY_MGMT_URI + "security/permissions/" + name,
                headers=requestHeaders,
                params=requestParameters,
                data=json.dumps(payload),
                verify=False,  # do not check certificate
                auth=(self.USER, self.PASSWORD))
        return r.status_code
    
    def permissions_delete(self, name):
        r = requests.delete(
            self.ARTIFACTORY_MGMT_URI + "security/permissions/" + name,
            verify=False,  # do not check certificate
            auth=(self.USER, self.PASSWORD))
        return r.status_code


