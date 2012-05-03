#!/usr/bin/python

# Core4 Configuration File

# Local check-out location
checkout_dir = "C:/Dev/workspace" #${branch}/${app}"

# JBoss deployment directory
deploy_dir = "C:/Dev/Apps/JBoss/JBoss-5/server/tools/deploy"

# Application name and directory
#app_name = "ls-tools"

# Location of build.xml
#build_dir = "conf/local"

# Repository location
svn = {
    "svn.server"      : "https://server/svn/branches",
    "svn.branch"      : "LSHL-PRODUCTION-SUPPORT-2011-05-03",
    "svn.app"         : "ls-tools",
    "svn.core.ver"    : 4
}

# Configuration files
files = {
    "application.properties":
        [{
            "pattern": "application.shared.content.directory=${value}",
            "value": "C:/Dev/workspace/LSHL-PRODUCTION-SUPPORT-2011-05-03/ls-content/content/tools"
        },{
            "pattern": "application.shared.directory=${value}",
            "value": "C:/Dev/workspace/LSHL-PRODUCTION-SUPPORT-2011-05-03/ls-content"
        },{
            "pattern": "application.deployed.locale=${value}",
            "value": "en_CA"
        },{
            "pattern": "global.encryption.enabled=${value}",
            "value": "false"
        }],

    "build.properties":
        [{
            "pattern": "target.server=${value};",
            "value": "jboss"
        },{
            "pattern": "jboss.dir=${value}",
            "value": "C:/Dev/apps/jboss/jboss-5"
        },{
            "pattern": "tomcat.dir=${value}",
            "value": ""
        },{
            "pattern": "jboss.server.config=${value}",
            "value": "tools"
        }],

    "jboss/ls-ds.xml":
        [{
            # Username
            "pattern": "<user-name>${value}</user-name>",
            "value": ""
        },{
            "pattern": "user=${value};",
            "value": ""
        },{
            # Password
            "pattern": "<password>${value}</password>",
            "value": ""
        },{
            "pattern": "password=${value};",
            "value": ""
        }],

    "../ehcache.xml":
        [{
            "pattern": "<diskStore path=\"${value}\"/>",
            "value": "c:/temp"
        }]
}

# Symbolic File links
links = {
    "ls-tools5.war" :
        [{
            "directory": "",
            "target": "${branch_dir}/ls-content"
        }],

    "sharedfiles" :
        [{
            "directory": "",
            "target": "${branch_dir}/ls-content"
        }]
}

# Search pattern for configuration key
regex = {
    #todo: error if regex is not found for a given config file
    "application.properties": "(.*)",
    "build.properties": "(.*)",
    "jboss/ls-ds.xml": "(.*?)",
    "../ehcache.xml": "(.*?)"
}






# Variables:

# ${checkout_dir} = local check out directory
# ${deploy_dir} = jboss project deployment directory
# ${branch} =
# ${app} =

# Specify a relative location:
# "value": "${project_dir}/ls-content/content/tools"
#
# Or specify an absolute location
# "value": "c:/dev/ls-content/content/tools"

