# coding: utf-8
import os
import sys
import time
import loggus
import inspect
import colorama
import importlib

from threading import RLock

__author__ = "https://github.com/CzaOrz"
__version__ = "0.0.1"


# collect & count all samples.
class Collector:
    start = time.monotonic()

    allSample = 0
    passSample = 0
    failSample = 0
    lock = RLock()

    def addSample(self):
        with self.lock:
            self.allSample += 1

    def addPassSample(self):
        with self.lock:
            self.passSample += 1
            self.addSample()

    def addFailSample(self):
        with self.lock:
            self.failSample += 1
            self.addSample()

    def show(self, other: str = ""):
        print(f"""
CodeCoverage: {int(other)}%
TotalCases: {self.allSample}
Pass: {self.passSample}
Fail: {self.failSample}
Cost: {time.monotonic() - self.start:.3f} s
""")
        if self.failSample:
            print(colorama.Fore.RED + f"Test Failed")
            print(colorama.Style.RESET_ALL)
            sys.exit(loggus.PANIC)
        else:
            print(colorama.Fore.GREEN + f"Test Pass")
            print(colorama.Style.RESET_ALL)
            sys.exit(0)


collector = Collector()


# hook for info.
class CollectorPassHook(loggus.IHook):

    def GetLevels(self):
        return [loggus.INFO]

    def ProcessMsg(self, msg):
        collector.addPassSample()


# hook for error.
class CollectorFailHook(loggus.IHook):

    def GetLevels(self):
        return [loggus.ERROR]

    def ProcessMsg(self, msg):
        collector.addFailSample()


# new logger, it is safe for loggus.
logger = loggus.NewLogger()
logger.AddHook(CollectorPassHook())
logger.AddHook(CollectorFailHook())
# bind this logger for entry.
entry = loggus.NewEntry(logger)


def find_unittest_yaml(path=".", last=None):
    if path == last:
        return None
    path = os.path.abspath(path)
    last = path
    if os.path.exists(os.path.join(path, "unittest.yaml")):
        os.chdir(path)
        return path
    path = os.path.dirname(path)
    return find_unittest_yaml(path, last)


# init a unittest.yaml for project
def init():
    unittest_yaml = find_unittest_yaml()
    if unittest_yaml:
        loggus. \
            withField("UnitTestYamlPath", unittest_yaml, loggus.ERROR_COLOR). \
            panic(f"project had already init!")
    projectName = os.path.basename(os.path.abspath("."))
    with open("unittest.yaml", "w", encoding="utf-8") as f:
        f.write(f"""version: beta
kind: unittest
metadata:
  project:
    name: {projectName}
""")
    loggus.withField("UnitTestYamlPath", unittest_yaml).info("init success!")


# create a py test file.
def create(pyfile: str):
    currentPath = os.path.abspath(".")
    if not find_unittest_yaml():
        loggus.panic("init project first")
    os.chdir(currentPath)
    sys.path.append(currentPath)

    if not os.path.isfile(pyfile):
        loggus.panic(f"not exist file: <{pyfile}>.")
    dirName = os.path.dirname(pyfile)
    if dirName:
        sys.path.append(dirName)

    pyfile = pyfile. \
        replace(".\\", ""). \
        replace("\\", "."). \
        replace("/", "."). \
        replace(".py", ""). \
        strip("./")

    try:
        module = importlib.import_module(pyfile)
    except:
        loggus.withTraceback().panic("ImportModuleErr")
        return
    template = f"""# coding: utf-8
import loggus

try:
    from .{pyfile} import *
except:
    from {pyfile} import *

"""
    for attr in dir(module):
        if attr.startswith(("_", "UnitTest")):
            continue
        attrIns = getattr(module, attr)
        if not inspect.isfunction(attrIns):
            loggus.debug(f"ignore self attr<{attr}>")
            continue
        if hasattr(attrIns, "__module__") and attrIns.__module__ != pyfile:
            loggus.withField("module", attrIns.__module__).warning(f"ignore other module attr<{attr}>")
            continue
        loggus.debug(f"found {attr}, generate UnitTest_{attr}")
        sig = inspect.signature(attrIns)
        parameters = []
        argsKeys = []
        argsValues = []
        for k, v in sig.parameters.items():
            argsKeys.append(k)
            if v.kind == v.POSITIONAL_ONLY:
                argsValues.append(k)
            elif v.kind == v.POSITIONAL_OR_KEYWORD:
                argsValues.append(k)
            elif v.kind == v.VAR_POSITIONAL:
                argsValues.append(f"*{k}")
            elif v.kind == v.KEYWORD_ONLY:
                argsValues.append(f"**{k}")
            elif v.kind == v.VAR_KEYWORD:
                argsValues.append(f"**{k}")
            if v.annotation is sig.empty:
                parameters.append(
                    "                {},".format(
                        {k: {"kind": v.kind.__str__()}}))
            else:
                parameters.append(
                    "                {},".format(
                        {k: {"kind": v.kind.__str__(), "type": f"{v.annotation}"}}))
        argsKeys = ", ".join(argsKeys)
        if argsKeys:
            argsKeys += ","
            argsKeys += " = sample[\"parameters\"]"
        argsValues = ", ".join(argsValues)
        parameters = "\n".join(parameters)
        loggus.WithFields({
            "argsKeys": argsKeys,
            "argsValues": argsValues,
            "parameters": parameters,
        }).debug("generate successful")
        template += f"""
def UnitTest_{attr}(entry: loggus.Entry) -> None:
    entry = entry.withField("funcName", "{attr}")
    # test cases.
    samples = [
        {{
            "name": str,
            "parameters": [
{parameters}
            ],
            "want": None,
            "wantErr": bool,
        }},
    ]
    # perform validation.
    for sample in samples[1:]:
        log = entry.withField("sampleName", sample["name"])
        try:
            {argsKeys}
            want = {attr}({argsValues})
        except:
            log.info("pass") if sample["wantErr"] else log.withTraceback().error("ExceptionErr")
        else:
            if sample["wantErr"]:
                log.error("Want Err But Pass")
            elif want != sample["want"]:
                log.withFields({{"want": sample["want"], "actual": want}}).error("EqualErr")
            else:
                log.info("pass")\n
"""
        loggus.info(f"add attr<{attr}> successful")

    def ensureUnique(src: str) -> None:
        if os.path.exists(src):
            while True:
                dst = f"{src}.{int(time.time())}.bak"
                if os.path.exists(dst):
                    continue
                os.rename(src, dst)
                break

    ensureUnique(f"{pyfile}_test.py")
    with open(f"{pyfile}_test.py", "w", encoding="utf-8") as f:
        f.write(template)
    sys.path.remove(currentPath)
    loggus.info("create unit test file successful~")


# scan all test module in current dir.
def scan(save: bool = False, xml: bool = False, html: bool = False) -> None:
    import coverage

    unittest_yaml = find_unittest_yaml()
    if not unittest_yaml:
        loggus.panic("not found unittest.yaml, please `init` for your project.")
    sys.path.append(unittest_yaml)
    cov = coverage.Coverage(None, include=["./*"], omit=["*/*_test.py"])
    cov.start()
    for path, dirs, files in os.walk("."):
        for file in files:
            if not file.endswith("_test.py"):
                continue
            actual = os.path.join(path, file)
            print(f">>> found unittest file {actual}:")
            modulePath = os.path.abspath(os.path.dirname(actual))
            sys.path.append(modulePath)
            loggus.debug(f"add module path: {modulePath}")
            module = actual. \
                replace(".\\", ""). \
                replace("\\", "."). \
                replace("/", "."). \
                replace(".py", ""). \
                strip("./")
            log = entry.withField("module", module)
            try:
                module = importlib.import_module(module)
                for attr in dir(module):
                    loggus.debug(f"found attr<{attr}>")
                    if attr.startswith("UnitTest_"):
                        getattr(module, attr)(log)
            except:
                log.withTraceback().panic("TestErr")
            sys.path.remove(modulePath)
            loggus.debug(f"remove module path: {modulePath}")
    sys.path.remove(unittest_yaml)
    cov.stop()
    if save:
        cov.xml_report() if xml else None
        cov.html_report() if html else None
    print("\n  --------------------------- ")
    print("  ------ UnitTest Over ------ ")
    print("  --------------------------- \n")
    try:
        collector.show(cov.report())
    except coverage.CoverageException:
        loggus.withFields({
            "ProjectPath": unittest_yaml,
        }).error("Not Found Test Files.")


def delete():
    unittest_yaml = find_unittest_yaml()
    if not unittest_yaml:
        loggus.panic("not found unittest.yaml, please `init` for your project.")
    for path, dirs, files in os.walk("."):
        for file in files:
            if not file.endswith("_test.py"):
                continue
            actual = os.path.join(path, file)
            try:
                os.remove(actual)
            except:
                loggus.withField("file", actual).error("remove failure!")
            else:
                loggus.withField("file", actual).info("remove success!")


def execute():
    import argparse

    parser = argparse.ArgumentParser(
        prog="pytestorz",
        description="This is a unittest tools like go test.",
    )
    parser.add_argument("-i", "--init", action="store_true", help="init a unittest.yaml for project.")
    parser.add_argument("-c", "--create", type=str, help="create a unit test file for a py-file.")
    parser.add_argument("-t", "--test", action="store_true", help="start a unit test.")
    parser.add_argument("-s", "--save", action="store_true", help="save reports when start a unit test.")
    parser.add_argument("--xml", action="store_true", help="if `-s`, then generate a xml report after unit test.")
    parser.add_argument("--html", action="store_true", help="if `-s`, then generate a html report after unit test.")
    parser.add_argument("--delete", action="store_true",
                        help="delete all test files, use it when you packages such like Dockerfile.")

    args = parser.parse_args()

    if args.init:
        init()
    elif args.create:
        create(args.create)
    elif args.test:
        scan(args.save, args.xml, args.html)
    elif args.delete:
        delete()
    else:
        parser.print_help()
