0.11.1 (2021-02-13)
-------------------

* Release for testing publishing of self-contained binaries built via pyinstaller

0.11.0 (2021-01-18)
-------------------

* aws-gate now has basic support for running on Windows platforms. However, **aws-gate bootstrap** is not yet working and session-manager-plugin has to be installed by the user separately (contribution by [@mbp](https://github.com/mbp))
* **aws-gate ssh** now supports local port forwarding (contribution by [@iainelder](https://github.com/iainelder))
* **aws-gate ssh** now supports remote port forwarding
* **aws-gate ssh** now supports dynamic (SOCKS5) port forwarding

0.10.1 (2021-01-07)
-------------------

* Refactor `cli.py` argument parsing, so it is easier to integrate with (contribution by [@awiddersheim](https://github.com/awiddersheim))

0.10.0 (2021-01-04)
-------------------

* Add support for SSM managed instances. These instances are prefixed by `mi-` (contribution by [@awiddersheim](https://github.com/awiddersheim))
* Error messages that are raised when AWS API querying fails are now visible (contribution by [@awiddersheim](https://github.com/awiddersheim))
* Minor performance improvements ([#691](https://github.com/xen0l/aws-gate/pull/691), [#693](https://github.com/xen0l/aws-gate/pull/693)) (contribution by [@awiddersheim](https://github.com/awiddersheim))

0.9.3 (2020-12-23)
------------------

* Add new AWS regions

0.9.2 (2020-10-17)
------------------

* Fix regression introduced in #572, which resulted in not being to find bootstrapped plugin
* Plugin version comparison is using more robust mechanism to determine newer plugin version

0.9.1 (2020-10-06)
------------------

* Add bash completion for **exec**(contribution by [@kit494way](https://github.com/kit494way))
* Fix ls to show instances without Name tag (contribution by [@kit494way](https://github.com/kit494way))
* Pass environment on to subprocess and support running behind a proxy (contribution by [@DanSipola](https://github.com/DanSipola))

0.9.0 (2020-05-03)
------------------

* Add **exec** command to be able to execute interactive commands over SSM. Idea by [@nc-furstenauw](https://github.com/nc-furstenauw)  

0.8.8 (2020-04-21)
------------------

* Default profile and region are now used if hosts profile and region are not defined. This allows to have much leaner config files, especially in situations when multiple hosts are sharing the same profile and region. Contributed by [@svalentino](https://github.com/svalentino)
* AWS sessions will look for cached credentials in ~/.aws/cli/cache. Contributed by [@becrsh](https://github.com/becrsh)
* Fix Python 3.6 compatibility issue in `subprocess.run`. Tested by [@larryon](https://github.com/larryon)

0.8.7 (2020-02-12)
------------------

* Improve instance listing performance in cases when there are many instances connecged to AWS Systems Manager 

0.8.6 (2020-01-17)
------------------

* Extend user agent with aws-gate version information, so it can be easier tracked in CloudTrail

0.8.5 (2020-01-14)
------------------

* Provide more debug output when fetching host information from config files. 

0.8.4 (2019-12-24)
------------------

* Version 0.8.3 introduced a bug into querying instance by autoscaling group, where the name would not be properly parsed. This is now fixed.

0.8.3 (2019-12-23)
------------------

* aws-gate now supports querying instances via **asg** identifier
* Querying instances by autoscaling group tag is now fixed

0.8.2 (2019-12-11)
------------------

* aws-gate now ships with Bash completion

0.8.1 (2019-12-10)
------------------

* _plugin\_required_ decorator now also checks for the presence of system-installed session-manager-plugin (contribution by [@kit494way](https://github.com/kit494way))
 
0.8.0 (2019-12-03)
------------------

* **list** subcommand is able to return output in multiple formats: JSON, TSV, CSV and human
* aws-gate now ships with ZSH completion

0.7.2 (2019-11-30)
------------------

* Docker container is now available
* Tests have been refactored to use pytest
* aws-gate now uses Github Actions

0.7.1 (2019-11-11)
------------------

* Turn off SSH host key verification in **aws-gate ssh**

0.7.0 (2019-11-09)
------------------

* Add **ssh** command to be able to directly connect to instances via SSH

0.6.1 (2019-10-29)
------------------

* aws-gate will now use AWS profile from AWS_VAULT environment variable when called from aws-vault

0.6.0 (2019-10-11)
------------------

* Add support for Linux in **bootstrap**
* Black coding style is now used
* pre-commit hooks are available for easier development

0.5.0 (2019-10-04)
------------------

* Add **ssh-proxy** command to be able to use ssh over Session Manager session
* Add **ssh-config** command to generate _~/.ssh/config_ configuration for easier integration with _ssh_
* AWS profile_name and region_name validation happens now on all commands

0.4.3 (2019-09-26)
------------------

* Fix problem with uncaptured command output
* bootstrap not working when ~/.aws-gate is missing

0.4.2 (2019-08-21)
------------------

* Use default region and profile in list command
* Always use own version of session-manager-plugin if available
* Improve tests coverage

0.4.1 (2019-08-12)
------------------

* Homebrew package is now available

0.4.0 (2019-08-11)
------------------

* Add **bootstrap**, which downloads session-manager-plugin on macOS
* aws-gate now queries only for running instances
* aws-gate functions using session-manager-plugin are now safeguarded by plugin_required and plugin_version decorators

0.3.0 (2019-05-26)
------------------

* Add support for aws-vault (portions contributed by [@danmx](https://github.com/danmx))
* Option to query by name
* Improve performance of queries by tag
* Add configuration file support


0.2.0 (2019-01-12)
------------------

* Allow opening session via tag identifier (contribution by [@openbankGit](https://github.com/openbankGit))
* Add list subcommand (contribution by [@openbankGit](https://github.com/openbankGit))

0.1.0 (2018-11-18)
-------------------

* Initial release
