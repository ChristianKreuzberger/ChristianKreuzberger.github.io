---
title: "Adding a new dynamic library to waf / wscript"
alias: "adding-a-new-dynamic-library-to-waf-wscript"
tags:
  - "Informatics"
  - "Linux"
weight: 0
created_at: "2015-02-24T00:00:00Z"
updated_at: "2015-02-24T00:00:00Z"
---

When using waf / wscript for compiling a project, you might come across the problem of adding another library, e.g., a shared object, to the compile and run process of waf. The task is trivial, but tutorials on that matter seem to be rare.

In my specific example, the task at hand was to add an external library, which I built from source, to an existing complex project. For now, we call this library libExternalStuff.\
I assume that libExternalStuff has been built externally with whatever tools it was required to built, and it generated the following:\
$SOMEDIR/libExternalStuff/includes/\*.h (in particular, we are going to use externalStuff.h)\
$SOMEDIR/libExternalStuff/bin/libExternalStuff.so\
Where $SOMEDIR could be anywhere, e.g., in your home directory.

If you would "install" the library to your includes and library paths on Linux, you would probably be able to skip the following steps. Though if you don't want to mess with your Linux distributions configuration, or if you want to have a custom version of a certain library, this should be helpful.

Open the wscript file of your project (or subproject). Find the part where it says\
`def configure(conf):`

Within this method, add the following:\
`\
test_code = '''\
#include "externalStuff.h"`

int main()\
{\
return 0;\
}\
'''

conf.env.append\_value('INCLUDES', os.path.abspath(os.path.join("$SOMEDIR/libExternalStuff/includes/", ".")))

conf.check(args=["--cflags", "--libs"], fragment=test\_code, package='libExternalStuff', lib='ExternalStuff', mandatory=True, define\_name='EXTERNAL\_STUFF',\
uselib\_store='EXTERNAL\_STUFF',libpath=os.path.abspath(os.path.join("$SOMEDIR/libExternalStuff/bin/", ".")))

conf.env.append\_value('PROJECT\_MODULE\_PATH',os.path.abspath(os.path.join("$SOMEDIR/libExternalStuff/bin/", ".")))

This should get you going when you call:\
`./waf configure`

What are those lines doing? First of all, we are creating a test code, which tries including one of the generated/provided header files. This can be adapted to anything you would like, and is mainly a sanity check. Second, we are adding the includes directory to the global INCLUDES path. This is important, else the compiler wouldn't know where to find the include script. Then we are creating a configuration entry for libdash. I'm not an expert with waf/wscript, but this line seems to have worked fine for me. Most importantly, make sure to have the lib parameter set properly (e.g., if your shared object is called libExternalStuff.so, then the lib parameter reflects the -l parameter of gcc, and needs to be set to ExternalStuff). libpath is used for the linker to determine where to find the .so file.\
The last line\
 `conf.env.append_value('PROJECT_MODULE_PATH',os.path.abspath(os.path.join("$SOMEDIR/libExternalStuff/bin/", ".")))`\
is something specific to your project and you would have to figure out how the global variable is called in your project. This is the path where the project will look for the shared object file when using ./waf --run.

If your projct also has a --run method, then you will have to add the library to the run-configuration.\
Find out where dynamic libraries are specified in your wscript, and add it to the line, e.g.:\
`module.uselib = 'LIB1 LIB2 EXTERNAL_STUFF'`

I'm not an expert with waf/wscript, but those lines should get you going. However, based on the used project, some lines might have to be added, modified or deleted.