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

###
### local functions for API calls
###
### to allow any needed parameter/value manipulation

def artifactory_health():
    return artifactoryAPI.artifactory_health()
        
def artifactory_information():
    return artifactoryAPI.artifactory_information()
        
def artifactory_configuration():
    return artifactoryAPI.artifactory_configuration()
        
def license_information():
    return artifactoryAPI.license_information()
        
def license_install():
    with open(options.keyFile, 'r') as data_file:
        data = data_file.read()
    return artifactoryAPI.license_install(data)
        
def users_list():
    return artifactoryAPI.users_list()
        
def users_detail():
    return artifactoryAPI.users_detail(options.name)
        
def users_create():
    name = os.path.splitext(options.userFile)[0]
    with open(options.userFile, 'r') as data_file:
        data = data_file.read()    
    return artifactoryAPI.users_create(name,data)
        
def users_update():
    name = os.path.splitext(options.userFile)[0]
    with open(options.userFile, 'r') as data_file:
        data = data_file.read()
    return artifactoryAPI.users_update(name,data)
        
def users_delete():
    return artifactoryAPI.users_delete(options.name)

def groups_list():
    return artifactoryAPI.groups_list()
        
def groups_detail():
    return artifactoryAPI.groups_detail(options.name)
        
def groups_create():
    name = os.path.splitext(options.groupFile)[0]
    with open(options.groupFile, 'r') as data_file:
        data = data_file.read()
    return artifactoryAPI.groups_create(name,data)
        
def groups_update():
    name = os.path.splitext(options.groupFile)[0]
    with open(options.groupFile, 'r') as data_file:
        data = data_file.read()
    return artifactoryAPI.groups_update(name,data)
        
def groups_delete():
    return artifactoryAPI.groups_delete(options.name)

def repositories_list():
    return artifactoryAPI.repositories_list(options.type)
        
def repositories_detail():
    return artifactoryAPI.repositories_detail(options.key)

def repositories_create():
    name = os.path.splitext(options.repositoryFile)[0]
    with open(options.repositoryFile, 'r') as data_file:
        data = data_file.read()
    return artifactoryAPI.repositories_create(name,data)

def repositories_update():
    name = os.path.splitext(options.repositoryFile)[0]
    with open(options.repositoryFile, 'r') as data_file:
        data = data_file.read()
    return artifactoryAPI.repositories_update(name,data)

def repositories_delete():
    return artifactoryAPI.repositories_delete(options.key)

def permissions_list():
    return artifactoryAPI.permissions_list()
        
def permissions_detail():
    return artifactoryAPI.permissions_detail(options.name)
        
def permissions_create():
    name = os.path.splitext(options.permissionFile)[0]
    with open(options.permissionFile, 'r') as data_file:
        data = data_file.read()
    return artifactoryAPI.permissions_create(name,data)
        
def permissions_delete():
    return artifactoryAPI.permissions_delete(options.name)

###
### parameter parsing/promptrint commands
###

# prompt user for input, using proper function for Python major version
def user_input(prompt):
    if sys.version_info[0] > 2: 
        return input(prompt)
    else:
        return raw_input(prompt)
    
##################################
# main program
##################################

if __name__ == "__main__":

    ###
    ### setup argument parser
    ###

    main_parser = argparse.ArgumentParser(
                      description='Command-line interface to the Artifactory REST API.',
                      formatter_class=argparse.RawDescriptionHelpFormatter,
                      epilog=textwrap.dedent('''\
                        Examples:
                          %(prog)s -s -u admin -p password artifactoryHostname repos list 
                          %(prog)s -user admin --server artifactory.company.com:5000/artifactory repos list
                          
                        See '%(prog)s <object> --help' to read about a specific subcommand.
                      '''))  
    
    main_parser.add_argument('-s', '--server', required=True, help='target server or base Artifactory URL')
                                                                                                                  
    main_parser.add_argument('-u', '--username', required=False, default='admin', help='username for Artifactory authentication')
                                                                                                                  
    main_parser.add_argument('-p', '--password', required=False, help='password for Artifactory authentication')
                                                                                                                  
    object_subparsers = main_parser.add_subparsers(title="object", dest="object")                                                                                                              
       
    ###
    ### parser for the "artifactory" object
    ###
    object_parser_artifactory = object_subparsers.add_parser(
                                "artifactory",
                                help="manuipulate an Artifactory Instance: {health,information,configuration}")

    object_action_subparser_artifactory = object_parser_artifactory.add_subparsers(title="action", dest="action")                                                                                                               

    parser_artifactory_info = object_action_subparser_artifactory.add_parser(
                          "health",
                          help="get Health Status",
                          description="Retrieve Health Status of the Artifactory Installation.",
                          formatter_class=argparse.RawDescriptionHelpFormatter,
                          epilog=textwrap.dedent('''\
                            Examples:
                              %(prog)s  
                          '''))  

    parser_artifactory_install = object_action_subparser_artifactory.add_parser(
                          "information",
                          help="get Information",
                          description="Retrieve Information of the Artifactory Installation.",
                          formatter_class=argparse.RawDescriptionHelpFormatter,
                          epilog=textwrap.dedent('''\
                            Examples:
                              %(prog)s   
                          '''))  
    
    parser_artifactory_install = object_action_subparser_artifactory.add_parser(
                          "configuration",
                          help="get Configuration",
                          description="Retrieve Configuration of the Artifactory Installation.",
                          formatter_class=argparse.RawDescriptionHelpFormatter,
                          epilog=textwrap.dedent('''\
                            Examples:
                              %(prog)s   
                          '''))  
    
    ###
    ### parser for the "license" object
    ###
    
    object_parser_license = object_subparsers.add_parser(
                                "license",
                                help="manuipulate a License: {information,install}")

    object_action_subparser_license = object_parser_license.add_subparsers(title="action", dest="action")                                                                                                               

    parser_license_info = object_action_subparser_license.add_parser(
                          "information",
                          help="get License information",
                          description="Retrieve information about the current License.",
                          formatter_class=argparse.RawDescriptionHelpFormatter,
                          epilog=textwrap.dedent('''\
                            Examples:
                              %(prog)s  
                          '''))  

    parser_license_install = object_action_subparser_license.add_parser(
                          "install",
                          help="install a License Key",
                          description="Install License Key contained in a file.",
                          formatter_class=argparse.RawDescriptionHelpFormatter,
                          epilog=textwrap.dedent('''\
                            Examples:
                              %(prog)s --keyFile licenseKey.json  
                          '''))  

    parser_license_install.add_argument('--keyFile', required=True, help='File containing the License Key to install.')
    
    ###
    ### parser for the "users" object
    ###
    
    object_parser_users = object_subparsers.add_parser(
                             "users",
                             help="manuipulate Users: {list,detail,create,update,delete}",
                             epilog="See '%(prog)s <user_action> --help' to read about a specific User action.")
                                                                                            
    object_action_subparser_users = object_parser_users.add_subparsers(title="action", dest="action")                                                                                                               
    
    parser_users_list = object_action_subparser_users.add_parser(
                          "list",
                          help="list all Users",
                          description="List all Users.",
                          formatter_class=argparse.RawDescriptionHelpFormatter,
                          epilog=textwrap.dedent('''\
                            Examples:
                              %(prog)s  
                          '''))  

    parser_users_detail = object_action_subparser_users.add_parser(
                          "detail",
                          help="get the details of User",
                          description="Get the details of a User.",
                          formatter_class=argparse.RawDescriptionHelpFormatter,
                          epilog=textwrap.dedent('''\
                            Examples:
                              %(prog)s administrator  
                          '''))  

    parser_users_detail.add_argument('--name', required=True, help='Username to return the details of.')

    parser_users_create = object_action_subparser_users.add_parser(
                          "create",
                          help="create or replace a User",
                          description="Create a User from a JSON file. Any existing User with the same Username will be replaced.",
                          formatter_class=argparse.RawDescriptionHelpFormatter,
                          epilog=textwrap.dedent('''\
                            Examples:
                              %(prog)s testuser.json  
                          '''))  

    parser_users_create.add_argument('--userFile', required=True, help='JSON file with details of user to create. Base name of file without extension is used as Username.')

    parser_users_update = object_action_subparser_users.add_parser(
                          "update",
                          help="update an existing User",
                          description="Update an existing User from a JSON file.",
                          formatter_class=argparse.RawDescriptionHelpFormatter,
                          epilog=textwrap.dedent('''\
                            Examples:
                              %(prog)s testuser.json  
                          '''))  

    parser_users_update.add_argument('--userFile', required=True, help='JSON file with details of user to update. Base name of file without extension is used as Username.')

    parser_users_delete = object_action_subparser_users.add_parser(
                          "delete",
                          help="delete a user",
                          description="Delete a User.",
                          formatter_class=argparse.RawDescriptionHelpFormatter,
                          epilog=textwrap.dedent('''\
                            Examples:
                              %(prog)s testuser  
                          '''))  

    parser_users_delete.add_argument('--name', required=True, help='Username to delete.')

    ###
    ### parser for the "groups" object
    ###
    
    object_parser_groups = object_subparsers.add_parser(
                             "groups",
                             help="manuipulate Groups: {list,detail,create,update,delete}",
                             epilog="See '%(prog)s <group_action> --help' to read about a specific Group action.")
                                                                                            
    object_action_subparser_groups = object_parser_groups.add_subparsers(title="action", dest="action")                                                                                                               
    
    parser_groups_list = object_action_subparser_groups.add_parser(
                          "list",
                          help="list all Groups",
                          description="list all Groups.",
                          formatter_class=argparse.RawDescriptionHelpFormatter,
                          epilog=textwrap.dedent('''\
                            Examples:
                              %(prog)s  
                          '''))  

    parser_groups_detail = object_action_subparser_groups.add_parser(
                          "detail",
                          help="get the details of a Group",
                          description="Get the details of a Group.",
                          formatter_class=argparse.RawDescriptionHelpFormatter,
                          epilog=textwrap.dedent('''\
                            Examples:
                              %(prog)s admins  
                          '''))  

    parser_groups_detail.add_argument('--name', required=True, help='Groupname to return details of.')

    parser_groups_create = object_action_subparser_groups.add_parser(
                          "create",
                          help="create or replace a Group",
                          description="Create a Group from a JSON file. Any existing Group with the same Groupname will be replaced.",
                          formatter_class=argparse.RawDescriptionHelpFormatter,
                          epilog=textwrap.dedent('''\
                            Examples:
                              %(prog)s testgroup.json  
                          '''))  

    parser_groups_create.add_argument('--groupFile', required=True, help='JSON file with details of Group to create. Base name of file without extension is used as Groupname.')

    parser_groups_update = object_action_subparser_groups.add_parser(
                          "update",
                          help="update am existing Group",
                          description="Update an existing Group from a JSON file.",
                          formatter_class=argparse.RawDescriptionHelpFormatter,
                          epilog=textwrap.dedent('''\
                            Examples:
                              %(prog)s testgroup.json  
                          '''))  

    parser_groups_update.add_argument('--groupFile', required=True, help='JSON file with details of Group to update. Base name of file without extension is used as Groupname.')

    parser_groups_delete = object_action_subparser_groups.add_parser(
                          "delete",
                          help="delete a group",
                          description="Delete a Group.",
                          formatter_class=argparse.RawDescriptionHelpFormatter,
                          epilog=textwrap.dedent('''\
                            Examples:
                              %(prog)s testgroup  
                          '''))  

    parser_groups_delete.add_argument('--name', required=True, help='Groupname to delete.')

    ###
    ### parser for the "repositories" object
    ###
    
    object_parser_repos = object_subparsers.add_parser(
                             "repositories",
                             help="manuipulate Repositories: {list,detail,create,update,delete}",
                             epilog="See '%(prog)s <repository_action> --help' to read about a specific Repository action.")
                                                                                            
    object_action_subparser_repos = object_parser_repos.add_subparsers(title="action", dest="action")                                                                                                               
    
    parser_repos_list = object_action_subparser_repos.add_parser(
                          "list",
                          help="list all Repositories or all Repositories of a specific Type",
                          description="List all Repositories or Repositories of a specific Type.",
                          formatter_class=argparse.RawDescriptionHelpFormatter,
                          epilog=textwrap.dedent('''\
                            Examples:
                              %(prog)s  
                              %(prog)s local
                          '''))  
    
    parser_repos_list.add_argument('--type', required=False, nargs='?', default="", choices=['local', 'remote', 'virtual'], help='Type of Respositories to return. If not specified, will return all Types.')
    
    parser_repos_detail = object_action_subparser_repos.add_parser(
                          "detail",
                          help="get the details of a Repository",
                          description="Get the details of a Repository.",
                          formatter_class=argparse.RawDescriptionHelpFormatter,
                          epilog=textwrap.dedent('''\
                            Examples:
                              %(prog)s testrepo  
                          '''))  

    parser_repos_detail.add_argument('--key', required=True, help='Key of Respository to return the configuration of.')

    parser_repos_create = object_action_subparser_repos.add_parser(
                          "create",
                          help="create or replace a Repository",
                          description="Create a Repository from a JSON file. Any existing Repository with the same Key will be replaced.",
                          formatter_class=argparse.RawDescriptionHelpFormatter,
                          epilog=textwrap.dedent('''\
                            Examples:
                              %(prog)s testrepo.json  
                          '''))  

    parser_repos_create.add_argument('--repositoryFile', required=True, help='JSON file with details of Repository to create. Base name of file without extension is used as Key.')

    parser_repos_update = object_action_subparser_repos.add_parser(
                          "update",
                          help="update an existing Repository",
                          description="Update an existing Repository from a JSON file.",
                          formatter_class=argparse.RawDescriptionHelpFormatter,
                          epilog=textwrap.dedent('''\
                            Examples:
                              %(prog)s testrepo.json  
                          '''))  

    parser_repos_update.add_argument('--repositoryFile', required=True, help='JSON file with details of Repository to update. Base name of file without extension is used as Key.')

    parser_repos_delete = object_action_subparser_repos.add_parser(
                          "delete",
                          help="delete a Repository",
                          description="Delete an Repository.",
                          formatter_class=argparse.RawDescriptionHelpFormatter,
                          epilog=textwrap.dedent('''\
                            Examples:
                              %(prog)s testuser  
                          '''))  

    parser_repos_delete.add_argument('--key', help='Key of Respository to delete.')

    ###
    ### parser for the "permissions" object
    ###
    
    object_parser_permissions = object_subparsers.add_parser(
                             "permissions",
                             help="manuipulate Permissions: {list,detail,create,delete}",
                             epilog="See '%(prog)s <permission_action> --help' to read about a specific Permission action.")
                                                                                            
    object_action_subparser_permissions = object_parser_permissions.add_subparsers(title="action", dest="action")                                                                                                               
    
    parser_permissions_list = object_action_subparser_permissions.add_parser(
                          "list",
                          help="list all Permissions",
                          description="List all Permissions.",
                          formatter_class=argparse.RawDescriptionHelpFormatter,
                          epilog=textwrap.dedent('''\
                            Examples:
                              %(prog)s  
                          '''))  

    parser_permissions_detail = object_action_subparser_permissions.add_parser(
                          "detail",
                          help="get the details of Permission",
                          description="Get the details of a Permission.",
                          formatter_class=argparse.RawDescriptionHelpFormatter,
                          epilog=textwrap.dedent('''\
                            Examples:
                              %(prog)s administrator  
                          '''))  

    parser_permissions_detail.add_argument('--name', required=True, help='Permission to return details of.')

    parser_permissions_create = object_action_subparser_permissions.add_parser(
                          "create",
                          help="create a permission",
                          description="Create a permission from a JSON file.",
                          formatter_class=argparse.RawDescriptionHelpFormatter,
                          epilog=textwrap.dedent('''\
                            Examples:
                              %(prog)s testpermission.json  
                          '''))  

    parser_permissions_create.add_argument('--permissionFile', required=True, help='JSON file with details of Permission to create. Base name of file without extension is used as Permissionname.')

    parser_permissions_delete = object_action_subparser_permissions.add_parser(
                          "delete",
                          help="delete a permission",
                          description="Delete an Artifactory permission.",
                          formatter_class=argparse.RawDescriptionHelpFormatter,
                          epilog=textwrap.dedent('''\
                            Examples:
                              %(prog)s testpermission  
                          '''))  

    parser_permissions_delete.add_argument('--name', required=True, help='Permissionname to delete.')

    ###
    ### parse command-line arguments
    ###
    
    options = main_parser.parse_args()  
    
    ###
    ### command-line parsable; start work
    ###

    ###
    ### setup API
    ###
    
    # build baseURL from passed baseURL, hostname, or hostname/PublicContextPath
    serverPassed = options.server
    serverParsed = urlparse.urlsplit(serverPassed)
    serverHostname = serverParsed.hostname # will not contain a value unless a URL was passed
    if not serverHostname: # passed value was not a URL, build one
        serverHostname = serverPassed
        serverPublicContextPath = 'artifactory' # should be updated to skip this if "/" already present, indicating empty PublicContextPath
        baseURL = 'http://' + serverHostname + '/' + serverPublicContextPath # should be updated to skip this if "/" already present, indicating empty PublicContextPath
    else: # passed value was a URL, just extract PublicContextPath (for possible future use)
        serverPublicContextPath = serverParsed.path[1:]
        baseURL = serverPassed

    if not options.password:
        options.password = getpass.getpass(prompt='Password for Artifactory user ' + artifactoryUsername +':')

    # setup API
    artifactoryAPI = artifactoryAPI.ArtifactoryAPI(baseURL, options.username, options.password)
    
    ###
    ### process command
    ###

    # call the local function named by the submitted object and action, then format, print, and return the result
    result = locals()[ options.object+'_'+options.action ]()
    pprint(result)
#    sys.exit(result)

    ###
    ### cleanup and exit
    ###

    # nothing to do

### EOF
