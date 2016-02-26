# Bootstrap

Script to quickly switch between source code branches or ramp-up a new development environment, resulting in a live functioning application workstation. (Best used with a centralized vcs (svn) versus distributed versions (i.e., git or mercurial) that already provide quick branch management functionality)

## Prerequisites

1. Installed Developer IDE.
1. Installed application servers. 
1. Installed source code control client (i.e., svn)

## Bootstrap process

Single command:

1. Fetch latest source code per configured branch (Usually HEAD development)
1. Update configuration files for application servers based upon target environment: Dev, Test, etc.
1. Build the source.
1. Test the deliverables. 
1. Deploy locally the application(s).
1. Start servers. 
