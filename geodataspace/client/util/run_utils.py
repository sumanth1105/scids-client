import subprocess
import sys

def cmd_print_output(process):
    for line in iter(process.stdout.readline, ''):
        line = line.strip()
        print "   > ", line
    return 1


def run_command(args, processing_function=cmd_print_output):
    #print ("running:", args)
    try:
        process = subprocess.Popen(args,
                                   shell=True,
                                   bufsize=-1,
                                   stdout=subprocess.PIPE,
                                   stderr=None,
                                   universal_newlines=True)


        output = processing_function(process)

        process.communicate()
    except OSError:
        print "   > ", sys.exc_info()[1]

    return output

def is_geounit_selected(geounit):
    if geounit is None:
        print "please select a geounit"
        return False
    return geounit.is_active