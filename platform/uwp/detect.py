import os
import sys
from typing import TYPE_CHECKING

from methods import print_error
from platform_methods import detect_arch, validate_arch
from platform.windows import detect as windows_detect

if TYPE_CHECKING:
    from SCons.Script.SConscript import SConsEnvironment

STACK_SIZE = windows_detect.STACK_SIZE
STACK_SIZE_SANITIZERS = windows_detect.STACK_SIZE_SANITIZERS

SUPPORTED_ARCHES = ["x86_64", "arm64"]


def get_name():
    return "Windows UWP"


def can_build():
    # UWP builds rely on the Desktop MSVC or clang-cl toolchains which are
    # only available on Windows hosts.
    return os.name == "nt" and windows_detect.can_build()


def get_doc_classes():
    return ["EditorExportPlatformUWP"]


def get_doc_path():
    return "doc_classes"


def get_tools(env: "SConsEnvironment"):
    tools = windows_detect.get_tools(env)
    if "mingw" in tools:
        print_error("UWP builds require an MSVC or clang-cl toolchain. Please re-run from a MSVC prompt.")
        sys.exit(255)
    return tools


def get_opts():
    from SCons.Variables import BoolVariable, EnumVariable

    detected_arch = windows_detect.detect_build_env_arch() or detect_arch()
    if detected_arch not in SUPPORTED_ARCHES:
        detected_arch = "x86_64"

    return [
        EnumVariable(
            "arch",
            "Target CPU architecture",
            detected_arch,
            SUPPORTED_ARCHES,
            ignorecase=2,
        ),
        BoolVariable("use_llvm", "Use the clang-cl toolchain", False),
        BoolVariable("uwp_enable_cppwinrt", "Enable C++/WinRT projection support (/ZW)", False),
        BoolVariable("uwp_force_bigobj", "Force /bigobj for large translation units", True),
    ]


def get_flags():
    arch = windows_detect.detect_build_env_arch() or detect_arch()
    if arch not in SUPPORTED_ARCHES:
        arch = "x86_64"

    return {
        "arch": arch,
        "supported": ["library"],
    }


def configure(env: "SConsEnvironment"):
    validate_arch(env["arch"], get_name(), SUPPORTED_ARCHES)

    env.Prepend(CPPPATH=["#platform/windows", "#platform/uwp"])

    env.setdefault("windows_subsystem", "gui")

    env.msvc = True
    windows_detect.configure_msvc(env)

    env.AppendUnique(CPPDEFINES=["UWP_ENABLED"])
    env.AppendUnique(CPPDEFINES=[("WINAPI_FAMILY", "WINAPI_FAMILY_APP")])

    if env.get("uwp_force_bigobj", True):
        if "/bigobj" not in env["CCFLAGS"]:
            env.AppendUnique(CCFLAGS=["/bigobj"])
    else:
        env["CCFLAGS"] = [flag for flag in env["CCFLAGS"] if flag != "/bigobj"]

    if env.get("uwp_enable_cppwinrt"):
        env.AppendUnique(CCFLAGS=["/ZW"])
    else:
        env["CCFLAGS"] = [flag for flag in env["CCFLAGS"] if flag != "/ZW"]

    env.AppendUnique(LINKFLAGS=["/APPCONTAINER", "/WINMD"])
