#!/usr/bin/env python
# -*- coding: utf-8 -*-

import  os, sys, tempfile, traceback, shutil, re, logging, subprocess

# bootstrap - NWL Developer Application initialization script
# 1. fetch source
# 2. update configuration
# 3. compile
# 4. link jboss server

# dynamic config imports, loaded by command line argument
cfg = {}
new_dir = ""
build_dir = "conf/local"

def usage():
    print ("""bootstrap - Developer Application initialization script
Fetches, configures, and builds NWL applications\n
Usage: bootstrap [OPTIONS] <config_file>
    Override Options:
    -a appname      -a ls-tools
    -b branch       -b PRODUCTION-SUPPORT-1
    -d directory    -d .
    -f fetch        -f force fetch
    -v verbose

    e.g.:   bootstrap ls-tools
            where config file is named "ls-tools.py"\n""")

def fetch_source():
    #global new_dir
    #new_dir = "%s/%s/%s" % (
    #    cfg.checkout_dir,
    #    cfg.svn['svn.branch'],
    #    cfg.svn['svn.app'])

    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

        params = dict(
            checkout_dir = cfg.checkout_dir,
            server = cfg.svn['svn.server'],
            branch = cfg.svn['svn.branch'],
            app = cfg.svn['svn.app'],
        )

        tmpl = "svn checkout $server/$branch/$app $checkout_dir/$branch/$app"
        process = Template(tmpl).substitute(params)
        logging.info(" [FETCH] %s" % process)
        os.system(process)
    else:
        logging.info(" [FETCH] Skipping fetch. Check-out directory exists.")

def update_config():
    for eachfile in cfg.files.keys():
        edits = cfg.files[eachfile]

        params = dict(
            checkout_dir = cfg.checkout_dir,
            branch = cfg.svn['svn.branch'],
            app = cfg.svn['svn.app'],
            build_dir = cfg.build_dir,
            each_file = eachfile)

        tmpl = "$checkout_dir/$branch/$app/$build_dir/$each_file"
        filename = Template(tmpl).substitute(params)
        logging.info("[CONFIG] Updating %s" % eachfile)
        update_file(filename, eachfile, edits)

def update_file(filename, eachfile, edits):
    #Create temp file
    fh, abspath = tempfile.mkstemp()
    newfile = open(abspath,'w')
    oldfile = open(filename)

    for line in oldfile:
        tmpline = line
        for eachedit in edits:
            tmpl = Template(eachedit['pattern'])
            ptn = tmpl.substitute(value=cfg.regex[eachfile])
            val = tmpl.substitute(value=eachedit['value'])
            tmpln = re.sub(ptn, val, tmpline)
            tmpline = tmpln
        newfile.write(tmpln)
        #string replace

    #close temp file
    newfile.close()
    os.close(fh)
    oldfile.close()
    #Remove original file
    os.remove(filename)
    #Move new file
    shutil.move(abspath, filename)

def build_source():
    build_dir = new_dir.join("/conf/local")
    logging.info(" [BUILD] Build directory: %s" % build_dir)
    if os.path.exists(build_dir):
        os.chdir(new_dir + "/conf/local")
        if os.path.exists("build.xml"):
            logging.info(" [BUILD] Compiling...")
            retcode = run_process("ant -q")
            #logging.info(" [BUILD] Result: " + str(retcode))
            if retcode > 0: raise Exception("Compiling failed")
        else:
            logging.info(" [BUILD] Build script (build.xml) not found")
    else:
        logging.info(" [BUILD] Build directory not found" %
            build_dir)

def run_process(args, **kwds):
    kwds.setdefault("stdout", subprocess.PIPE)
    kwds.setdefault("stderr", subprocess.STDOUT)
    retcode = subprocess.call(args.split())
    return retcode

def link_server():
    #"$deploy_dir"
    if not os.path.exists("/jboss-5/server/tools/deploy/ls-tools.war"):
        logging.info("[LINK] Linking war")
        #delete link
        #print
        #os.makedirs(new_dir)
        process = "junction /jboss-5/server/tools/deploy/%s %s/%s/%s/defaultroot" % (
            cfg.svn['svn.app'] + ".war",
            cfg.checkout_dir,
            cfg.svn['svn.branch'],
            cfg.svn['svn.app'])
        os.system(process)

def success():
    logging.info("  [PASS] Success!")

def failure(msg):
    logging.error("  [FAIL] *** %s" % msg)

def load_config(config_file):
    global cfg
    cfg = __import__(config_file, fromlist='*')

def scrub_config():
    # Location of build.xml
    global build_dir
    if True: #core_ver == 4
        build_dir = "conf/local"
    cfg.svn['svn.server'] = trim(cfg.svn['svn.server'])
    cfg.svn['svn.branch'] = trim(cfg.svn['svn.branch'])
    cfg.checkout_dir = trim(cfg.checkout_dir)

def trim(str):
    return str.rstrip("/\\").lstrip("/\\")

def init_logging():
    logging.basicConfig(level=logging.DEBUG,
                        format="[%(asctime)s] %(message)s",
                        datefmt="%m-%d %H:%M",
                        filename="bootstrap.log",
                        filemode="w")
    console = logging.StreamHandler()
    formatter = logging.Formatter("%(message)s")
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

if __name__ == "__main__":
    init_logging()
    try:
        if len(sys.argv) < 2 or sys.argv[1] == 'help':
            usage()
            sys.exit(1)

        config_file = sys.argv[1]

        if (not sys.argv[1].endswith(".py")):
            config_file += ".py"

        if not os.path.exists(config_file):
            print >>sys.stderr, "Configuration $config_file file not found"
            sys.exit(2)

        load_config(config_file)
        scrub_config()
        logging.info("*** Bootstrapping %s ***" % cfg.svn['svn_app'])
        logging.info("   [CMD] ".join(sys.argv))
        fetch_source()

        update_config()
        build_source()
        link_server()
        success()

    except Exception, msg:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stderr)
        print '-'*60

        #failure("%s" % sys.exc_info()[1])
        #for err in sys.exc_info(): sys.stderr.write(err)
        #print sys.exc_info()

        #logging.info("[CONFIG] Updating JBoss server.xml")
        #logging.info("[CONFIG] Updating JBoss .keystore")
        #copy default server to server name if not present
        #server.xml
        #keystore

"""
def __init__(self):
    self.states = {}
    self.state = None
    self.dbg = None

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
             raise Usage(msg)
        # more code, unchanged
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())
"""
