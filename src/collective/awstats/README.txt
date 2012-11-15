BlueAwstats
===========

BlueAwstats is a products for displaying Awstats generated statistice inside
a plone site.

Version:
========

  * 1.5

Requirements
============

  * Plone 2.5
  * Zope 2.9
  * bda.awstatsparser
  * BlueAwstatsManagementTool

Installation:
=============

  * Checkout and/or download the requirements
  
  * Start Zope
  
  * Go to the ZMI and add a BlueAwstatsManagementTool. On further information
    about the Management Tool see README.txt of this product.
  
  * Install the BlueAwstats Product with portal quickinstaller

Changes:
========

  * Awstats object is not a tool any longer
  
  * Statistic Parts can be enabled and disabled
  
  * Custom Parts can be added

Awstats object:
===============

  An awstats object can be placed anywhere in the portal. You have to be
  Manager to do that.
  
  The ability to create more than one awstats objects gives you beyond the
  features of the BlueAwstatsManagementTool makes the permission management
  more fine-grained.
  
  On Each Awstats object you can specify which parts are displayed and each one
  has its own custom parts.

Custom Parts:
=============

  Custom Parts can be used to get specific information out of the SIDER section
  of the awstats file.

  At the moment there is not really a gui implemented to configure the Custom
  parts.
  
  For a part you have to define the calculation epoch. it is either annual or
  monthly.
  
  Then you have to set a flag wether a graph should be generated or not.
  The graph is always drawn next to the title if flag is set to true.
  
  The listing configuration is primary done by a simple text field.
  
  The available informations in the SIDER section are:
    * Pages - How many times an URL has been accessed
    * Bandwidth - The used bandwith for this URL
    * Entry - How often this URL was the entry point
    * Exit - How often this URL was the exit point
  
  The syntax for the statistic configuration is as follows:
  
  * In the first line you define the information to display, seperated by pipes.
    For Example:
    
        Pages (Downloads) | Bandwith | Entry | Exit
   
    There must be at least one requested information. The term in parethesis
    can be set optional and is then used as the information identifyer.
  
  * The following lines are the URL's to chart, and optional a title to use
    for this URL, f.e.:
    
        /foo/bar (Newsletter 1)
        /bar/baz (Newsletter 2)

TODO:
=====

  * cleanup the logic in browser/stats.py for displaying the single parts
  
  * improve the styles for the part chooser
  
  * make graph generation not beeing macros any longer
  
  * extend custom parts (atm only SIDER section supported)
  
  * general more refactoring (much later)

Credits:
========

  * This Product was written by Robert Niederreiter <rnix@squarewave.at>
  
  * The dependent bda.awstatsparser was written by
    Jens Klein <jens@bluedynamics.com>
