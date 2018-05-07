## How to contribute to Nagbot

### Coding standards

All code needs to be in git. If your code is not in git then it could or likely will be deleted when 
the app is re-installed for testing.

#### Which branch should I use?

1. master is the branch used for live or production code and shouldn't contain untested code.
2. testing is branched from develop and is used for testing. 
3. develop is where we should be making changes

Note: If you are not comfortable making changes in develop then you can create a branch for your personal use and merge 
that into develop once you are happy with your changes.

**Documentation usually don't affect the runnning of code and therefore I will update documentation in master
since it is easy to find**

#### Security

Please don't put API keys or credentials into source control - it is a security risk and could get our API key disabled 
which will make troubleshooting our app difficult.


#### Where to get help

If you need help or don't understand please ask in our slack channel. www.git-scm.org has a great tutorial on git if you 
are unfamiliar with git branching and merging. 



