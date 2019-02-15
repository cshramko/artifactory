#!/usr/bin/env python

###
### external import
###

import os
import sys
import json
import re
import getpass
import textwrap
import argparse
import urlparse
from pprint import pprint

###
### internal import
###

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import artifactoryAPI
from tools import log

###
### local functions for API calls
###
### to allow any needed parameter/value manipulation

def artifactory_get_information():
    return artifactoryAPI.artifactory_get_information()
        
def artifactory_get_health():
    return artifactoryAPI.artifactory_get_health()
        
def artifactory_get_configuration():
    return artifactoryAPI.artifactory_get_configuration()
        
def license_information():
    return artifactoryAPI.license_information()
        
def license_install(licenseData):
    return artifactoryAPI.license_install(licenseData)
        
def users_list():
    return artifactoryAPI.users_list()
        
def users_detail(username):
    return artifactoryAPI.users_detail(username)
        
def users_create(username, userData):
    return artifactoryAPI.users_create(username, userData)
        
def users_update(username, userData):
    return artifactoryAPI.users_update(username, userData)
        
def users_delete(username):
    return artifactoryAPI.users_delete(username)

def groups_list():
    return artifactoryAPI.groups_list()
        
def groups_detail(groupname):
    return artifactoryAPI.groups_detail(groupname)
        
def groups_create(groupname, groupData):
    return artifactoryAPI.groups_create(groupname, groupData)
        
def groups_update(groupname,groupData):
    return artifactoryAPI.groups_update(groupname, groupData)
        
def groups_delete(groupname):
    return artifactoryAPI.groups_delete(groupname)

def repos_list(repotype):
    return artifactoryAPI.repositories_list(repotype)
        
def repos_detail(repokey):
    return artifactoryAPI.repositories_detail(repokey)

def repos_create(repokey, repoData):
    return artifactoryAPI.repositories_create(repokey, repoData)

def repos_update(repokey, repoData):
    return artifactoryAPI.repositories_update(repokey, repoData)

def repos_delete(repokey):
    return artifactoryAPI.repositories_delete(repokey)

def permissions_list():
    return artifactoryAPI.permissions_list()
        
def permissions_detail(permissionname):
    return artifactoryAPI.permissions_detail(permissionname)
        
def permissions_create(permissionname, permissionData):
    return artifactoryAPI.permissions_create(permissionname, permissionData)
        
def permissions_delete(permissionname):
    return artifactoryAPI.permissions_delete(permissionname)

###
### parameter parsing/promptrint commands
###

# prompt user for input, using proper function for Python major version
def user_input(prompt):
    if sys.version_info[0] > 2: 
        return input(prompt)
    else:
        return raw_input(prompt)
    
# build Artifactory API Base URL
def get_artifactory_baseURL():
    # use value from command-line, if present
    if arguments.targetServer:
        valueProvided = arguments.targetServer

    # else use value from configuration file, if present
    elif 'artifactory' in config:
        if 'baseURL' in config['artifactory']:
            valueProvided = config['artifactory']['baseURL']
        elif 'hostname' in config['artifactory']:
            valueProvided = config['artifactory']['hostname']
        elif 'targetServer' in config['artifactory']:
            valueProvided = config['artifactory']['targetServer']

    # else prompt for value
    else:
        valueProvided = user_input('targetServer: ')

    # parse provided value and build full baseURL, as necessary
    valueParsed = urlparse.urlsplit(valueProvided)
    hostname = valueParsed.hostname # if full baseURL provided
    # note: serverPublicContextPath = valueParsed.path[1:] if full baseURL provided
    if not hostname:
        hostname = valueProvided
        if 'serverPublicContextPath' in config:
            serverPublicContextPath = config['serverPublicContextPath']
        else:
            serverPublicContextPath = 'artifactory'
        baseURL = 'http://' + hostname + '/' + serverPublicContextPath
    else:
        baseURL = valueProvided
        
    return baseURL

def get_artifactory_username():
    # use value from command-line, if present
    if arguments.username:
        username = arguments.username

    # else use value from configuration file, if present
    elif 'artifactory' in config:
        if 'username' in config['artifactory']:
            username = config['artifactory']['username']

    # else prompt for value
    else:
        username = user_input('username: ')

    return username

def get_artifactory_password():
    # use value from command-line, if present,
    if arguments.password:
        password = arguments.password

    # else use value from configuration file, if present,
    elif 'artifactory' in config:
        if 'password' in config['artifactory']:
            password = config['artifactory']['password']

    # else prompt for value
    else:
        password = getpass.getpass('password: ')

    return password

# get value of destructive flag
# if True, creates over-write existing objects with the same identifier and type
def get_destructive_flag():
    # use value from command-line, if flag was specified
    flagValue = arguments.destructive

    # else use value from configuration file, if present
    if not flagValue:
        if 'destructive' in config:
            flagValue = config['destructive']

    # else default to safe (non-destructive) mode
    # (provided by argparse default=)
    
    # safe flag from anywhere overrides
    if arguments.safe:
        flagValue = False
    if 'safe' in config:
        if config['safe']:
            flagValue = False
        
    return flagValue

###
### functions to process Artifactory section of configuration file
###

def process_artifactory_section():
    if 'health' in config['artifactory']:
        process_artifactory_health()
    if 'information' in config['artifactory']:
        process_artifactory_information()
    if 'configuration' in config['artifactory']:
        process_artifactory_configuration()
    return

def process_artifactory_health():
    if  config['artifactory']['health']:
        print('\nHealth Status: '+ artifactory_get_health())
    return

def process_artifactory_information():
    if  config['artifactory']['info']:
        print('\nArtifactory Instance Information:')
        print(artifactory_get_information())
    return

def process_artifactory_configuration():
    if  config['artifactory']['configuration']:
        print('\nArtifactory Instance Configuration:')
        print(artifactory_get_configuration())
    return

###
### functions to process License section of configuration file
###

def process_license_section():
    if 'information' in config['license']:
        process_license_information()
    if 'install' in config['license']:
        process_license_install()
    return
   
def process_license_information():
    if  config['license']['information']:
        print('\nLicense information:')
        print(str(license_information()))
    return

def process_license_install():
    licenseData = ''
    if 'licenseFile' in config['license']['install']:
        with open(config['license']['install']['licenseFile'], 'r') as license_file:
            licenseData = license_file.read()
    if 'license' in config['license']['install']:
        licenseData = config['license']['install']
    print('\nLicense installation results:')
    print(str(license_install(licenseData)))
    return

###
### functions to process Users section of configuration file
###

def process_users_section():
    if 'list' in config['users']:
        process_users_list()
    if 'detail' in config['users']:
        process_users_detail()
    if 'delete' in config['users']:
        process_users_delete()
    if 'create' in config['users']:
        process_users_create()
    if 'createFromFile' in config['users']:
        process_users_createFromFile()
    if 'update' in config['users']:
        process_users_update()
    if 'updateFromFile' in config['users']:
        process_users_updateFromFile()
    return

def process_users_list():
    print('\nList of Users:')
    print(str(users_list()))
    return

def process_users_detail():
    for username in config['users']['detail']:
        print('\nDetails for User "' + username + '":')
        print(str(users_detail(username)))
    return

def process_users_delete():
    for username in config['users']['delete']:
        print('\nDeleting User "' + username + '"')
        print('Results: ' + str(users_delete(username)))
    return

def process_users_create():
    for username in config['users']['create']:
        userData = config['users']['create'][username]
        print('\nCreating User "' + username + '" with data:')
        print(str(userData))
        print('\nResults:\n' +str(users_create(username,userData)))
    return

def process_users_createFromFile():
    for userFileName in config['users']['createFromFile']:
        with open(userFileName, 'r') as user_file:
            username = os.path.splitext(user_file)[0]
            userData = user_file.read()
            print('\nCreating User "' + username + '" with data:')
            print(str(userData))
            print('\nResults:\n' +str(users_create(username,userData)))
    return

def process_users_update():
    for username in config['users']['update']:
        userData = config['users']['update'][username]
        print('\nUpdating User "' + username + '" with data:')
        print(str(userData))
        print('\nResults:\n' +str(users_update(username,userData)))
    return

def process_users_update():
    for userFileName in config['users']['updateFromFile']:
        with open(userFileName, 'r') as user_file:
            username = os.path.splitext(user_file)[0]
            userData = user_file.read()
            print('\nUpdating User "' + username + '" with data:')
            print(str(userData))
            print('\nResults:\n' +str(users_update(username,userData)))
    return

###
### functions to process Groups section of configuration file
###

# identify and process subsections
def process_groups_section():
    if 'list' in config['groups']:
        process_groups_list()
    if 'detail' in config['groups']:
        process_groups_detail()
    if 'delete' in config['groups']:
        process_groups_delete()
    if 'create' in config['groups']:
        process_groups_create()
    if 'createFromFile' in config['groups']:
        process_groups_createFromFile()
    if 'update' in config['groups']:
        process_groups_update()
    if 'updateFromFile' in config['groups']:
        process_groups_updateFromFile()
    return

# display a list of all Artifactory Instance Groups
def process_groups_list():
    print('\nList of Groups:')
    print(str(groups_list()))
    return

# display details for listed Artifactory Instance Groups
def process_groups_detail():
    for groupname in config['groups']['detail']:
        print('\nDetails for Group "' + groupname + '":')
        print(str(groups_detail(groupname)))
    return

# delete listed Artifactory Instance Groups
def process_groups_delete():
    for groupname in config['groups']['delete']:
        print('\nDeleting Group "' + groupname + '"')
        print('Results: ' + str(groups_delete(groupname)))
    return

def process_groups_create():
    for groupname in config['groups']['create']:
        groupData = config['groups']['create'][groupname]
        print('\nCreating Group "' + groupname + '" with data:')
        print(str(groupData))
        print('\nResults:\n' +str(groups_create(groupname,groupData)))
    return

def process_groups_createFromFile():
    for groupname in config['groups']['create']:
        with open(groupFileName, 'r') as group_file:
            groupname = os.path.splitext(group_file)[0]
            groupData = group_file.read()
            print('\nCreating Group "' + groupname + '" with data:')
            print(str(groupData))
            print('\nResults:\n' +str(groups_create(groupname,groupData)))
    return

def process_groups_update():
    for groupname in config['groups']['update']:
        groupData = config['groups']['update'][groupname]
        print('\nUpdating Group "' + groupname + '" with data:')
        print(str(groupData))
        print('\nResults:\n' +str(groups_update(groupname,groupData)))
    return

def process_groups_update():
    for groupFileName in config['groups']['updateFromFile']:
        with open(groupFileName, 'r') as group_file:
            groupname = os.path.splitext(group_file)[0]
            groupData = group_file.read()
            print('\nUpdating Group "' + groupname + '" with data:')
            print(str(groupData))
            print('\nResults:\n' +str(groups_update(groupname,groupData)))
    return

###
### functions to process Repositories section of configuration file
###

def process_repos_section():
    if 'list' in config['repositories']:
        process_repos_list()
    if 'detail' in config['repositories']:
        process_repos_detail()
    if 'delete' in config['repositories']:
        process_repos_delete()
    if 'create' in config['repositories']:
        process_repos_create()
    if 'createFromFile' in config['repositories']:
        process_repositories_createFromFile()
    if 'update' in config['repositories']:
        process_repos_update()
    if 'updateFromFile' in config['repositories']:
        process_repos_updateFromFile()
    return

# display a list of all Artifactory Instance Repositories
# or all Repositories of listed Types
def process_repos_list():
    if type(config['repositories']['list']) is list:
         for repoType in config['repositories']['list']:
            print('\nList of Repositories of Type "' + repoType + '":')
            print(str(repos_list(repoType)))
    else:
        print('\nList of Repositories:')
        print(str(repos_list('')))
    return

def process_repos_detail():
    for reponame in config['repositories']['detail']:
        print('\nDetails for Repository "' + reponame + '":')
        print(str(repos_detail(reponame)))
    return

def process_repos_delete():
    for repoKey in config['repositories']['delete']:
        print('\nDeleting Repository "' + repoKey + '"')
        print('Results: ' + str(repos_delete(repoKey)))
    return

def process_repos_create():
    for repoKey in config['repositories']['create']:
        repoData = config['repositories']['create'][repoKey]
        print('\nCreating Repository "' + repoKey + '" with data:')
        print(str(repoData))
        print('\nResults:\n' +str(repos_create(repoKey,repoData)))
    return

def process_repos_createFromFile():
    for repoFileName in config['repositories']['create']:
        with open(repoFileName, 'r') as repo_file:
            repoKey = os.path.splitext(repo_file)[0]
            repoData = repo_file.read()
            print('\nCreating Repository "' + repoKey + '" with data:')
            print(str(repoData))
            print('\nResults:\n' +str(repos_create(repoKey,repoData)))
    return

def process_repos_update():
    for repoKey in config['repositories']['update']:
        repoData = config['repositories']['update'][repoKey]
        print('\nUpdating Repository "' + repoKey + '" with data:')
        print(str(repoData))
        print('\nResults:\n' +str(repos_update(repoKey,repoData)))
    return

def process_repos_updateFromFile():
    for repoFileName in config['repositories']['updateFromFile']:
        with open(repoFileName, 'r') as repo_file:
            repoKey = os.path.splitext(repo_file)[0]
            repoData = repo_file.read()
            print('\nUpdating Repository "' + repoKey + '" with data:')
            print(str(repoData))
            print('\nResults:\n' +str(repos_update(repoKey,repoData)))
    return

###
### functions to process Permissions section of configuration file
###

def process_permissions_section():
    if 'list' in config['permissions']:
        process_permissions_list()
    if 'detail' in config['permissions']:
        process_permissions_detail()
    if 'delete' in config['permissions']:
        process_permissions_delete()
    if 'create' in config['permissions']:
        process_permissions_create()
    if 'createFromFile' in config['permissions']:
        process_permissions_createFromFile()
    return

def process_permissions_list():
    print('\nList of Permissions:')
    print(str(permissions_list()))
    return

def process_permissions_detail():
    for permissionname in config['permissions']['detail']:
        print('\nDetails for Permission "' + permissionname + '":')
        print(str(permissions_detail(permissionname)))
    return

def process_permissions_delete():
    for permissionname in config['permissions']['delete']:
        print('\nDeleting Permission "' + permissionname + '"')
        print('Results: ' + str(permissions_delete(permissionname)))
    return

def process_permissions_create():
    for permissionname in config['permissions']['create']:
        permissionData = config['permissions']['create'][permissionname]
        print('\nCreating Permission "' + permissionname + '" with data:')
        print(str(permissionData))
        print('\nResults:\n' +str(permissions_create(permissionname,permissionData)))
    return

def process_permissions_createFromFile():
    for permissionname in config['permissions']['create']:
        with open(permissionFileName, 'r') as permission_file:
            permissionname = os.path.splitext(permission_file)[0]
            permissionData = permission_file.read()
            print('\nCreating Permission "' + permissionname + '" with data:')
            print(str(permissionData))
            print('\nResults:\n' +str(permissions_create(permissionname,permissionData)))
    return

###
### help and documentation functions
###

def display_config_file_syntax(configFile):
    sys.exit("ConfigFile: '" +configFile + "' not found. Display of configFile syntax is not yet implemented.")
    return

##################################
# main program
##################################

if __name__ == "__main__":

    ###
    ### setup argument parser
    ###

    main_parser = argparse.ArgumentParser(
                      description='Configure an Artifactory instance on targetServer from a declarative configuration file.',
                      formatter_class=argparse.RawDescriptionHelpFormatter,
                      epilog=textwrap.dedent('''\
                        If configFile is not found, the configFile syntax will be displayed.
                        
                        The arguments targetServer, username, and password may be specified in configFile.
                        %(prog)s will prompt any of these arguments which are not supplied.
                        
                        Examples:
                          %(prog)s artConfig.json 
                          %(prog)s artCongif.json hostname.company.com --safe
                          %(prog)s artCongif.json -u admin hostname.company.com
                          %(prog)s artCongif.json https://hostname.company.com:5000/ServerPublicContext
                          %(prog)s artConfig.json --configFile artConfig.json -D
                      '''))  
    
    main_parser.add_argument('-c', '--configFile', required=False, help='configuration JSON file')

    main_parser.add_argument('-t', '--targetServer', required=False, help='target server or base Artifactory URL')
                                                                                                                  
    main_parser.add_argument('-u', '--username', required=False, help='username for Artifactory authentication')
                                                                                                                  
    main_parser.add_argument('-p', '--password', required=False, help='password for Artifactory authentication')
                                                                                                                  
    main_parser.add_argument('-D', '--destructive', required=False, action='store_true', default=False, help='flag to allow destruction and replacement of any conficting resources')

    main_parser.add_argument('-S', '--safe', required=False, action='store_true', default=False, help='flag to prevent destruction and replacement of any conficting resources; overrides destructive flag')

    main_parser.add_argument('--debug', required=False, action='store_true', default=False, help='flag include debug information in output')


    ###
    ### parse command-line arguments
    ###

    arguments = main_parser.parse_args()  

    ###
    ### command-line parsable; start work
    ###

    print('\n' + os.path.basename(sys.argv[0]) + ' started.')
    debug = arguments.debug
    if debug:
        print('\n=== arguments:')
        print(arguments)

    ###
    ### process configuration file
    ###
        
    if arguments.configFile:
        configFile = arguments.configFile
    else:
        configFile = ''
    if not (os.path.isfile(configFile) and os.access(configFile, os.R_OK)):
        display_config_file_syntax(configFile)

    with open(configFile) as config_file:
        config = json.load(config_file)

    if debug:
        print('\n=== config-file:')
        print(config)

    ###
    ### setup API & program modes
    ###
        
    artifactory_baseURL = get_artifactory_baseURL()
    artifactory_username = get_artifactory_username()
    artifactory_password = get_artifactory_password()

    artifactoryAPI = artifactoryAPI.ArtifactoryAPI(artifactory_baseURL, artifactory_username, artifactory_password)

    # get value of destructive flag
    # if True, creates over-write existing objects with the same identifier and type
    destructive = get_destructive_flag()
    if destructive:
        print('\n!!! DESTRUCTIVE flag is set; any creates will replace existing entities. !!!')

    ###
    ### process command
    ###

    print('\nTarget Artifactory Instance: ' + artifactory_baseURL)
    
    if 'artifactory' in config:
        process_artifactory_section()

    if 'license' in config:
        process_license_section()

    if 'users' in config:
        process_users_section()

    if 'groups' in config:
        process_groups_section()

    if 'repositories' in config:
        process_repos_section()

    if 'permissions' in config:
        process_permissions_section()

    ###
    ### cleanup and exit
    ###

    print('\n' + os.path.basename(sys.argv[0]) + ' complete.\n')

### EOF
