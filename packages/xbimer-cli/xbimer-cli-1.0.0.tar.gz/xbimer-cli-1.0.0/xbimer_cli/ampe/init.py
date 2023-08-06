import PyInquirer
import click
import uuid
import json
import zipfile

from xml.etree import ElementTree as ET
from xml.dom import minidom
from os import path, getcwd, mkdir, unlink

__SupportedSdks__ = ['none', 'ac22', 'ac23']

__vcxprojFilters__ = [{
    'Include': 'Src',
    'UniqueIdentifier': '{de7d7a13-a071-41e4-8f04-7d1691f7ec83}',
    'Extensions': 'cpp;c;cxx'
}, {
    'Include': 'Headers',
    'UniqueIdentifier': '{b32da348-770f-41d8-85c9-903e1cc415c5}',
    'Extensions': 'h;hpp;hxx'
}, {
    'Include': 'Libraries',
    'UniqueIdentifier': '{42902bf0-12fb-4ecb-a6fa-d9d2cf0ceeb9}',
    'Extensions': 'lib'
}]

__vcxprojClcs__ = [{
    'Include': '$(ProjectName).cpp',
    'Filter': 'Src'
}, {
    'Include': R'src\dllmain.cpp',
    'Filter': 'Src'
}, {
    'Include': R'src\stdafx.cpp',
    'Filter': 'Src'
}]

__vcxprojClis__ = [{
    'Include': R'src\stdafx.h',
    'Filter': 'Headers'
}, {
    'Include': R'src\targetver.h',
    'Filter': 'Headers'
}]


def promptOptions():

    choices = []
    for sdk in __SupportedSdks__:
        choices.append({'name': sdk})

    ques = [{
        "type": "input",
        "message": "Project Name:",
        "name": "name",
        "validate": lambda val: len(val.replace(" ", "")) > 3
    }, {
        "type": "checkbox",
        "message": "Select Archicad SDK:",
        "name": "sdks",
        "choices": choices
    }]

    answers = PyInquirer.prompt(ques)

    return answers["name"].replace(" ", ""), answers["sdks"]


def readIncludesBySdk(sdk):
    file = path.join(path.dirname(__file__), f"includes_{sdk}.json")
    with open(file, 'r', encoding='utf-8') as f:
        return json.loads(f.read(), encoding='utf-8')


def readLibrariesBySdk(sdk):
    file = path.join(path.dirname(__file__), f"libraries_{sdk}.json")
    with open(file, 'r', encoding='utf-8') as f:
        return json.loads(f.read(), encoding='utf-8')


def appendElements(xmlRoot, eles, name, sdk=None):
    if sdk != None:
        ig = ET.SubElement(
            xmlRoot, 'ItemGroup',
            {'Condition': f"'$(Configuration)|$(Platform)'=='{sdk}|x64'"})
    else:
        ig = ET.SubElement(xmlRoot, 'ItemGroup')

    for ele in eles:
        flt = ET.SubElement(ig, name, {'Include': ele['Include']})

        if 'Filter' in ele:
            ET.SubElement(flt, 'Filter').text = ele['Filter']

        if 'UniqueIdentifier' in ele:
            ET.SubElement(flt,
                          'UniqueIdentifier').text = ele['UniqueIdentifier']

        if 'Extensions' in ele:
            ET.SubElement(flt, 'Extensions').text = ele['Extensions']


def savePrettyXml(xmlRoot,
                  fileName,
                  indent='\t',
                  newline='\n',
                  encoding='utf-8'):
    rawXmlText = ET.tostring(xmlRoot)
    dom = minidom.parseString(rawXmlText)
    with open(fileName, 'w') as doc:
        dom.writexml(doc, '', indent, newline, encoding)


def extractZip(srcPath, destPath):
    zFile = zipfile.ZipFile(f"{srcPath}.zip")
    zFile.extractall(destPath)


def generateVcxproj(root, name, sdks):
    xmlRoot = ET.Element(
        'Project', {
            'DefaultTargets': 'Build',
            'ToolsVersion': '15.0',
            'xmlns': 'http://schemas.microsoft.com/developer/msbuild/2003'
        })

    # ProjectConfigurations
    ig = ET.SubElement(xmlRoot, 'ItemGroup',
                       {'Label': 'ProjectConfigurations'})
    for sdk in sdks:
        pc = ET.SubElement(ig, 'ProjectConfiguration',
                           {'Include': f'{sdk}|x64'})
        ET.SubElement(pc, 'Configuration').text = sdk
        ET.SubElement(pc, 'Platform').text = 'x64'

    # Globals
    ig = ET.SubElement(xmlRoot, 'PropertyGroup', {'Label': 'Globals'})
    ET.SubElement(ig, 'VCProjectVersion').text = '15.0'
    ET.SubElement(ig, 'ProjectGuid').text = f'{uuid.uuid4()}'
    ET.SubElement(ig, 'Keyword').text = 'Win32Proj'
    ET.SubElement(ig, 'RootNamespace').text = name
    ET.SubElement(ig, 'WindowsTargetPlatformVersion').text = '10.0.17763.0'

    # Import
    ET.SubElement(xmlRoot, 'Import',
                  {'Project': R'$(VCTargetsPath)\Microsoft.Cpp.Default.props'})

    # Configuration
    for sdk in sdks:
        ig = ET.SubElement(
            xmlRoot, 'PropertyGroup', {
                'Condition': f"'$(Configuration)|$(Platform)'=='{sdk}|x64'",
                'Label': 'Configuration'
            })
        ET.SubElement(ig, 'ConfigurationType').text = 'DynamicLibrary'
        ET.SubElement(ig, 'UseDebugLibraries').text = 'false'
        ET.SubElement(ig, 'PlatformToolset').text = 'v141'
        ET.SubElement(ig, 'WholeProgramOptimization').text = 'true'
        ET.SubElement(ig, 'CharacterSet').text = 'Unicode'

    # Import
    ET.SubElement(xmlRoot, 'Import',
                  {'Project': R'$(VCTargetsPath)\Microsoft.Cpp.props'})

    # ExtensionSettings
    ET.SubElement(xmlRoot, 'ImportGroup', {'Label': 'ExtensionSettings'})

    # Shared
    ET.SubElement(xmlRoot, 'ImportGroup', {'Label': 'Shared'})

    # PropertySheets
    for sdk in sdks:
        ig = ET.SubElement(
            xmlRoot, 'ImportGroup', {
                'Label': 'PropertySheets',
                'Condition': f"'$(Configuration)|$(Platform)'=='{sdk}|x64'"
            })
        ET.SubElement(
            ig, 'Import', {
                'Project':
                R'$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props',
                'Condition':
                R"exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')",
                'Label': 'LocalAppDataPlatform'
            })

    # UserMacros
    ET.SubElement(xmlRoot, 'PropertyGroup', {'Label': 'UserMacros'})

    # LinkIncremental
    for sdk in sdks:
        ig = ET.SubElement(
            xmlRoot, 'PropertyGroup',
            {'Condition': f"'$(Configuration)|$(Platform)'=='{sdk}|x64'"})
        ET.SubElement(ig, 'LinkIncremental').text = 'false'
        ET.SubElement(ig, 'TargetExt').text = '.pyd'

        if sdk == "none":
            outSuffix = "modules"
        else:
            outSuffix = f'{sdk}_modules'

        ET.SubElement(ig, 'OutDir').text = f'$(SolutionDir){outSuffix}\\'

    # ItemDefinitionGroup
    for sdk in sdks:
        ig = ET.SubElement(
            xmlRoot, 'ItemDefinitionGroup',
            {'Condition': f"'$(Configuration)|$(Platform)'=='{sdk}|x64'"})
        clc = ET.SubElement(ig, 'ClCompile')
        ET.SubElement(clc, 'PrecompiledHeader').text = 'Use'
        ET.SubElement(clc, 'WarningLevel').text = 'Level3'
        ET.SubElement(clc, 'Optimization').text = 'MaxSpeed'
        ET.SubElement(clc, 'FunctionLevelLinking').text = 'true'
        ET.SubElement(clc, 'IntrinsicFunctions').text = 'true'
        ET.SubElement(clc, 'SDLCheck').text = 'true'
        ET.SubElement(
            clc, 'PreprocessorDefinitions'
        ).text = f'NDEBUG;{name.upper()}_EXPORTS;_WINDOWS;_USRDLL;NOMINMAX;PROJECTNAME="{name}";ARCHICAD_{sdk.upper()}=1;%(PreprocessorDefinitions)'
        ET.SubElement(clc, 'ConformanceMode').text = 'true'

        dirs = readIncludesBySdk(sdk)

        ET.SubElement(clc,
                      'AdditionalIncludeDirectories').text = ';'.join(dirs)

        lk = ET.SubElement(ig, 'Link')
        ET.SubElement(lk, 'SubSystem').text = 'Windows'
        ET.SubElement(lk, 'EnableCOMDATFolding').text = 'true'
        ET.SubElement(lk, 'OptimizeReferences').text = 'true'
        ET.SubElement(lk, 'GenerateDebugInformation').text = 'true'
        ET.SubElement(
            lk, 'LinkTimeCodeGeneration').text = 'UseLinkTimeCodeGeneration'

    # ClInclude
    ig = ET.SubElement(xmlRoot, 'ItemGroup')
    ET.SubElement(ig, 'ClInclude', {'Include': R'src\stdafx.h'})
    ET.SubElement(ig, 'ClInclude', {'Include': R'src\targetver.h'})

    ig = ET.SubElement(xmlRoot, 'ItemGroup')
    ET.SubElement(ig, 'ClCompile', {'Include': R'src\dllmain.cpp'})
    ET.SubElement(ig, 'ClCompile', {'Include': f'src\\{name}.cpp'})
    std = ET.SubElement(ig, 'ClCompile', {'Include': R'src\stdafx.cpp'})

    for sdk in sdks:
        ET.SubElement(
            std, 'PrecompiledHeader', {
                'Condition': f"'$(Configuration)|$(Platform)'=='{sdk}|x64'"
            }).text = 'Create'

    # Library
    for sdk in sdks:
        libs = readLibrariesBySdk(sdk)
        appendElements(xmlRoot, libs, 'Library', sdk)

    ET.SubElement(xmlRoot, 'Import',
                  {'Project': R'$(VCTargetsPath)\Microsoft.Cpp.targets'})

    ET.SubElement(xmlRoot, 'ImportGroup', {'Label': 'ExtensionTargets'})

    fileName = f'{name}.vcxproj'
    savePrettyXml(xmlRoot, path.join(root, fileName))


def generateVcxprojUser(root, name, sdks):
    xmlRoot = ET.Element(
        'Project', {
            'ToolsVersion': '15.0',
            'xmlns': 'http://schemas.microsoft.com/developer/msbuild/2003'
        })

    for sdk in sdks:
        if sdk == 'none':
            continue

        ac = sdk.replace("ac", "")
        proGroup = ET.SubElement(
            xmlRoot, 'PropertyGroup',
            {'Condition': f"'$(Configuration)|$(Platform)'=='{sdk}|x64'"})

        ET.SubElement(
            proGroup, 'LocalDebuggerCommand'
        ).text = f'C:\\Program Files\\GRAPHISOFT\\ARCHICAD {ac}\\ARCHICAD.exe'
        ET.SubElement(proGroup, 'DebuggerFlavor').text = 'WindowsLocalDebugger'

    fileName = f'{name}.vcxproj.user'
    savePrettyXml(xmlRoot, path.join(root, fileName))


def generateVcxprojFilters(root, name, sdks):
    xmlRoot = ET.Element(
        'Project', {
            'ToolsVersion': '4.0',
            'xmlns': 'http://schemas.microsoft.com/developer/msbuild/2003'
        })

    # ItemGroup Filter
    appendElements(xmlRoot, __vcxprojFilters__, "Filter")
    appendElements(xmlRoot, __vcxprojClcs__, "ClCompile")
    appendElements(xmlRoot, __vcxprojClis__, "ClInclude")
    for sdk in sdks:
        libs = readLibrariesBySdk(sdk)
        appendElements(xmlRoot, libs, 'Library', sdk)

    fileName = f'{name}.vcxproj.filters'
    savePrettyXml(xmlRoot, path.join(root, fileName))


def extractLibraries(cRoot, pRoot, sdks):
    # extract archicad sdk
    for sdk in sdks:
        if sdk != 'none':
            extractZip(path.join(cRoot, 'zips', sdk), pRoot)

    # extract libraries
    extractZip(path.join(cRoot, 'zips', 'cast'), pRoot)
    extractZip(path.join(cRoot, 'zips', 'pybind11'), pRoot)
    extractZip(path.join(cRoot, 'zips', 'Python37'), pRoot)


def extractEntry(cRoot, pRoot, name):
    extractZip(path.join(cRoot, 'zips', 'entry'), pRoot)

    eFile = path.join(pRoot, 'src', '__entry__.cpp')
    with open(eFile, 'r', encoding='utf-8') as f:
        context = f.read()
        context = context.replace("__entry__", name)

    unlink(eFile)

    pFile = path.join(pRoot, 'src', f"{name}.cpp")
    with open(pFile, 'w', encoding='utf-8') as f:
        f.write(context)


@click.command()
def main():
    pName, acSdks = promptOptions()

    pRoot = path.join(getcwd(), pName)
    cRoot = path.dirname(__file__)

    if path.exists(pRoot) and path.isdir(pRoot):
        raise click.ClickException("folder already exists...")

    mkdir(pRoot)

    # generate visual studio c++ project guide files
    generateVcxproj(pRoot, pName, acSdks)
    generateVcxprojUser(pRoot, pName, acSdks)
    generateVcxprojFilters(pRoot, pName, acSdks)

    extractLibraries(cRoot, pRoot, acSdks)
    extractEntry(cRoot, pRoot, pName)
