collective.awstats
==================

collective.awstats is a products for displaying Awstats generated statistice
inside a plone site.


Installation
============

- Install and configure awstats. For Ubuntu based systems see
  https://help.ubuntu.com/community/AWStats

- Depend product in your buildout

- Install via GenericSetup or Quick Installer


Awstats object
==============

An awstats object can be placed anywhere in the portal. You have to be
Manager to do that.

On Each Awstats object you can specify which parts are displayed and each one
has its own custom parts.


Custom Parts
============

Custom Parts can be used to get specific information out of the SIDER section
of the awstats file. They are located as children inside an Awstats object.

You have to set a flag wether a graph should be generated or not.
The graph is always drawn next to the title if flag is set to true.

The listing configuration is primary done by a simple text field.

The available informations in the SIDER section are:

- pages - How many times an URL has been accessed
- bandwidth - The used bandwith for this URL
- entry - How often this URL was the entry point
- exit - How often this URL was the exit point

The syntax for the statistic configuration is as follows:

- In the first line you define the information to display, seperated by pipes.
  For Example:
  
    pages (Downloads) | bandwidth | entry | exit
  
  There must be at least one requested information. The term in parethesis
  can be set optional and is used as the information identifyer if given.

- The following lines are the URL's to chart, and optional a title to use
  for this URL, f.e.:
  
    /foo/bar (Newsletter 1)
    /bar/baz (Newsletter 2)


Awstats Extender
================

An Archetypes schemaextender is available for enabling per-object-based
statistics via a separate tab. The schema extender must be enabled explicitely,
e.g.::

    <adapter
      for="Products.Archetypes.BaseObject.BaseObject"
      name="collective.awstats"
      factory="collective.awstats.at.extender.AwstatsExtender" />


Contributors
============

- Robert Niederreiter <rnix [at] squarewave [dot] at>

- Jens Klein <jens [at] bluedynamics [dot] com>
