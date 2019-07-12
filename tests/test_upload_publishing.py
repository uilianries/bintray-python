# -*- coding: utf-8 -*-

import tempfile

from bintray.bintray import Bintray


def test_upload_content():
    bintray = Bintray()
    _, temp_path = tempfile.mkstemp()
    response = bintray.upload_content("uilianries", "generic", "statistics", "test", "test.txt",
                                      temp_path, override=True)
    assert {'error': False, 'message': 'success', 'statusCode': 201} == response


def test_bad_credentials_for_upload_content():
    bintray = Bintray("foobar", "85abc6aece02515e8bd87b9754a18af697527d88")
    error_message = ""
    try:
        _, temp_path = tempfile.mkstemp()
        bintray.upload_content("uilianries", "generic", "statistics", "test", "test.txt", temp_path)
    except Exception as error:
        error_message = str(error)
    assert "Could not PUT (401): 401 Client Error: Unauthorized for url: " \
           "https://api.bintray.com/content/uilianries/generic/statistics/test/test.txt?" \
           "publish=1&override=0&explode=0" == error_message


def test_maven_upload():
    bintray = Bintray()
    _, temp_path = tempfile.mkstemp(suffix=".xml")
    with open(temp_path, 'w') as fd:
        fd.write("""<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
<modelVersion>4.0.0</modelVersion>

<groupId>com.mycompany.app</groupId>
<artifactId>my-app</artifactId>
<version>1.0.0</version>

<properties>
<maven.compiler.source>1.7</maven.compiler.source>
<maven.compiler.target>1.7</maven.compiler.target>
</properties>

<dependencies>
<dependency>
  <groupId>junit</groupId>
  <artifactId>junit</artifactId>
  <version>4.12</version>
  <scope>test</scope>
</dependency>
</dependencies>
</project>
""")
    response = bintray.maven_upload("uilianries", "maven", "test", "pom.xml", temp_path,
                                    publish=True)
    assert {'error': False, 'message': 'success', 'statusCode': 201} == response
