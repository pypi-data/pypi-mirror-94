# FAME-Protobuf
Google Protocol Buffer (protobuf) definitions define the structure of binary input and output files for FAME applications.
Please visit the [Wiki for FAME](https://gitlab.com/fame-framework/wiki/-/wikis/home) to get an explanation of FAME and its components.

FAME-Protobuf connects FAME-Io to applications based on FAME-Core. Thus, both depend on FAME-Protobuf.

## Repository
The repository is split into three source code parts:
* protobuf definitions reside in `src/main/resources`,
* derived Python classes for FAME-Io reside in `src/main/python`.
* derived Java classes for FAME-Core reside in `target/generated-java-sources`, and

## Installation instructions
### Compile
The .pom-xml is configured to allow automated compilation of the protobuf definitions to Python and Java classes. 
#### With Eclipse
To compile just build the project by hitting Alt-F5.

### Usage with FAME-Core
#### Package and install
As long as the repository is not integrated with Maven-central, the Java source files should to be packaged into a library file and installed to local Maven repository.
##### With Eclipse
Run the provided launcher "InstallFamePBLocally.launch" by selecting "Run" -> "Run Configuration" -> "Maven Build" -> "InstallFamePBLocally" and clicking on "Run"

##### Linux Console
In the cloned repository of fame-protobuf:
Compile, package and install fame-protobuf to your local Maven repository: 

```
mvn install
```

#### Dependency of FAME-Core
**Only in case that the protobuf definitions have been updated:** Please update the Maven dependency in FAME-Core also. 

Currently, FAME-Core should use the following Maven dependency to refer to FAME-Protobuf

```
<dependency>
  <groupId>de.dlr.fame</groupId>
  <artifactId>protobuffers</artifactId>
  <version>0.3.3</version>
</dependency>
```

### Package to PyPI
FAME-Protobuf is packaged to PyPI. Use the provided `setup.py` to automatically 
* create Python package "fameprotobuf"
* fix broken Python imports
* setup the package
