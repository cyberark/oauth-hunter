

# oauth-hunter

[![GitHub release][release-img]][release]
[![License][license-img]][license] 
![Stars](https://img.shields.io/github/stars/cyberark/oauth-hunter)  


 <img align="right" src="https://github.com/user-attachments/assets/480aa00f-54d9-41fa-bb6b-e65f92fbc19e" alt="LibAFL logo" width="250" heigh="250">

oauth-hunter is a powerful tool designed for intercepting and analyzing OAuth requests using mitmproxy.   
It captures OAuth requests and performs comprehensive testing on the redirect_uri parameter, evaluating it against a variety of scenarios to identify potential vulnerabilities. 
This allows users to ensure the robustness of their OAuth implementations and safeguard against common security issues.  

In addition to its current capabilities, we are actively working on expanding the tool's functionality to include testing to the state parameter, among other enhancements.   
This ongoing development aims to provide a more thorough analysis of OAuth implementations, ensuring robust security and resilience against common vulnerabilities.  

--- 

## Table of Contents
- [Deployment](#deployment)
  - [Run from source](#run-from-source)
- [Usage](#usage)
  - [Burp Suite Integration](#burp-suite-integration)
  - [Menu](#menu)
- [Contributing](#contributing)
- [License](#license)
- [Share Your Thoughts and Feedback](#share-your-thoughts-and-feedback)

---

## Deployment  
You will need the following installed:
* python 3.x
* pip3

### Run from source
Clone the repository:
~~~
git clone https://github.com/cyberark/oauth-hunter.git
~~~

Install module dependencies. (You may prefer to do this within a [Virtual Environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/))
~~~
cd ./oauth-hunter
pip3 install -r requirements.txt
~~~

Run:
~~~
python3 main.py
~~~



## Usage  

The tool starts a proxy on the default port `1337`. Ensure you configure your system or tool to listen on this port to intercept and analyze network traffic.  

### Burp Suite Integration
For advanced usage, the tool can integrate with Burp Suite by specifying the `--burp-proxy` option followed by the port Burp Suite is configured to use.   
This allows the tool to send test requests through the Burp Suite proxy for enhanced analysis.


### Menu
```
usage: main.py [-h] [--create-excel [CREATE_EXCEL]] [--overwrite] [--proxy-port PROXY_PORT] [--burp-proxy [BURP_PROXY]] [--evil-domain EVIL_DOMAIN] [--yaml-scenarios YAML_SCENARIOS]

OAuth Proxy Tester

options:
  -h, --help            show this help message and exit
  --create-excel [CREATE_EXCEL]
                        Create an Excel file with the given name or use the default name.
  --overwrite           Overwrite the existing file if it exists.
  --proxy-port PROXY_PORT
                        Specify the proxy port.
  --burp-proxy [BURP_PROXY]
                        Specify the Burp proxy port. Defaults to 8080 if specified without a value.
  --evil-domain EVIL_DOMAIN
                        Specify the evil domain.
  --yaml-scenarios YAML_SCENARIOS
                        Path to YAML file with scenarios.
```

 


## Contributing

We welcome contributions of all kinds to this repository.  
For instructions on how to get started and descriptions
of our development workflows, please see our [contributing guide](https://github.com/cyberark/oauth-hunter/blob/main/CONTRIBUTING.md).

## License  
Copyright (c) 2024 CyberArk Software Ltd. All rights reserved  
This repository is licensed under  Apache-2.0 License - see [`LICENSE`](LICENSE) for more details.

## Share Your Thoughts And Feedback
For more comments, suggestions or questions, you can contact Eviatar Gerzi ([@g3rzi](https://twitter.com/g3rzi)) from CyberArk Labs.
You can find more projects developed by us in https://github.com/cyberark/.

[release-img]: https://img.shields.io/github/release/cyberark/oauth-hunter.svg
[release]: https://github.com/cyberark/oauth-hunter/releases

[license-img]: https://img.shields.io/github/license/cyberark/oauth-hunter.svg
[license]: https://github.com/cyberark/oauth-hunter/blob/master/LICENSE
