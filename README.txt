About
=====
This is a blogging engine based on Tipfy http://www.tipfy.org/ and Bloggart http://github.com/Arachnid/bloggart

Installation
---------------------------
@git clone git@github.com:mikkolehtinen/bloggart-tipfy.git@
@git submodule init && git submodule update@

- In your project folder run:
    python bootstrap.py --distribute
    bin/buildout

- Start the development server calling bin/dev_appserver. It will use the
  application from /app by default:

    bin/dev_appserver

- Open a browser and test the URLs:

    http://localhost:8080/
    http://localhost:8080/
