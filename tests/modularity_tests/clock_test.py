import modules.clock as clock
import modules.module_loader as ml
import tools.sklearn_sims as sk

def tests(classes):
    get_test(classes)
    fail_test(classes)

def get_test(classes):
    sk.compare_command("what is the time right now", classes)

def fail_test(classes):
    sk.compare_command("bad input", classes)
