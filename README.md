# Checkmarx Professional Services Power Hacks

This is a curated set of hacks maintained by the Checkmarx Professional Services and made available for public consumption.  This is a collection of scripts, tutorials, source code, and anything else that may be useful for use in the field by Checkmarx employees or customers.

## The List

Project | Description
--------|------------
[JenkinsDemoInstance](JenkinsDemoInstance) | Using Docker desktop, create an instance of Jenkins running under selected versions of the JDK.  Standalone and master/agent configurations are supported.  Settings are persisted in a local directory so that configurations are not lost when the Docker container is stopped.
[WindowsNoRDP](WindowsNoRDP) | A script that will configured the ability to log into a server's desktop using VNC over HTTP.  Primarily made to facilitate access to Checkmarx training VMs, this is useful in situations where RDP port 3389 access to a training instance may be blocked by a corporate firewall.