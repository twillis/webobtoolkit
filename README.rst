===============
 Webob Toolkit
===============

This was written as an experiment to explore how much effort it takes
to use the webob library on the client side.

I'm considering the experiment as success because though, I have been
using the lethal combination of webob.Request.get_response +
paste.proxy.TransparentProxy for many years, I did not know all the
things that were possible.

If I had to predict the future right now, I would say that this
library will contain code for sending HTTP requests, and handling
responses in a a way so easy you could use it interactively in the
console. 

BUT, it will also be flexible, in that all the pieces that make up the
happy path are simple enough to be composed into anything your heart
desires or that would meet your needs as far as communicating via
HTTP. 

And finally, it won't hide anything from you. HTTP is how our programs
communicate in todays world. There's no sense in trying to abstract
that away. We would all be better off when we all know what's going
on in that layer rather than pretending that layer doesn't exist.

So yeah, 

   #. easy
   #. flexible
   #. transparent 

It's not there yet because I just started, cut me some slack. :)
