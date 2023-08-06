from setuptools import setup
import sys

additional_requires=[] if sys.platform.startswith("hp-ux11") else ['psutil']

VERSION='3.2.2'

with open("m360/__init__.py","w") as f:
    f.write("__version__='"+VERSION+"'")

setup(
    name='m360-ptelegraf',
    version=VERSION,
    install_requires=[
        "backports.functools-lru-cache",
        "beautifulsoup4",
        "certifi",
        "cffi",
        "chardet",
        "configparser",
        "cryptography",
        "cx_Oracle<=7.3",
        "enum34",
        "idna",
        "ipaddress",
        "parse_apache_configs",
        "pycparser",
        "pyOpenSSL",
        "pyparsing",
        "python-dateutil",
        "pytz",
        "PyYAML",
        "requests",
        "six",
        "soupsieve",
        "urllib3"] + ["pystatgrab"] if sys.platform.startswith("hp-ux") else ['psutil']
    ,
    package_data={'m360.config': ['*.yaml',"*.sample","*.conf","*.ora"],
                  'm360.agents.weblogic.jmxmonitor': ['*.jar'],
                  'm360.agents.jboss.jmxmonitor': ['*.jar']
                  },
    packages=['m360',
              'm360.config',
              'm360.formatter',
              'm360.agents',
              'm360.agents.unix',
              'm360.agents.apache',
              'm360.agents.custom',
              'm360.agents.procstat',
              'm360.agents.jboss',
              'm360.agents.oracle',
              'm360.agents.oraclecloud',
              'm360.agents.jboss.jmxmonitor',
              'm360.agents.weblogic',
              'm360.agents.weblogic.jmxmonitor',
              'm360.agents.weblogic.lib',
              'm360.agents.tomcat',
              'm360.agents.internal',
              'm360.base',
              'm360.outputs',
              'm360.base.lib'],
    url='https://github.com/alerta/alerta-contrib',
    license='MIT',
    author='Enrique Pacheco Aragon',
    author_email='pacheco-aragon@dxc.com',
    description='Agentes python de M360 para Telegraf',
    py_modules=['m360.agents.tomcat.monitor','m360.agents.weblogic.monitor','m360.agents.internal.monitor',
                'm360.agents.jboss.monitor','m360.agents.unix.monitor','m360.agents.apache.monitor',
                'm360.agents.oracle.monitor','m360.agents.oraclecloud.monitor','m360.agents.custom.monitor',
                'm360.agents.procstat.monitor','m360.formatter.influx','m360.ptelegraf','m360.base.models'],
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.6',
    entry_points={
        'console_scripts': [
            'ptelegraf = m360.ptelegraf:main',
        ],
        'ptelegraf.monitors': [
            'jboss = m360.agents.jboss.monitor:Monitor',
            'weblogic = m360.agents.weblogic.monitor:Monitor',
            'unix = m360.agents.unix.monitor:Monitor',
            'apache = m360.agents.apache.monitor:Monitor',
            'tomcat = m360.agents.tomcat.monitor:Monitor',
            'oracle = m360.agents.oracle.monitor:Monitor',
            'custom = m360.agents.custom.monitor:Monitor',
            'procstat = m360.agents.procstat.monitor:Monitor',
            'oraclecloud = m360.agents.oraclecloud.monitor:Monitor',
            'internal = m360.agents.internal.monitor:Monitor',
        ]
    }
)
