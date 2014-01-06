================
 Change History
================

0.2.2
=====

  - merge pull request to address issue #8 https://github.com/twillis/webobtoolkit/issues/8

0.2.1
=====


  - check for content_type before attempting to set charset because
    some webservers behave badly

0.2
===

   - documentation updates
   - file uploads syntax sugar
   - changed client to not rely on a global pipeline app


0.1.3.3
=======

   - breakout stringify dict method as it may be useful

0.1.3.2
=======

   - client handles multidict to querystring better

0.1.3.1
=======

   - option for enabling auto redirect in test client


0.1.3
=====

   - added sugar for the HTTP OPTIONS method


0.1.2
=====

   - added preconfigured test client that is similar to webtest

0.1.1
=====

   - added file upload support
   - changed handling of query_string to look at the url if it is not
     passed in as a separate param.


0.1
===

initial release because I need this in my day job

0.0
===

first pass at a client, and first pass at docs.

