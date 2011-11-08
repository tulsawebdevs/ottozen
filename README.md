Welcome to the ottozen code repository.

This document is written in 
[Markdown](http://daringfireball.net/projects/markdown/)
(or more specifically,
[MultiMarkdown](http://fletcherpenney.net/multimarkdown/)).
The original is README.md, and the generated is README.html - make changes to
the original, and John Whitlock can regenerate the HTML version.

GETTING STARTED
===============
1. Contact Luke Crouch to get your credentials added to the sourcehold account
2. git clone git@sourcehold.com:groovecoder/ottozen.git
3. Install:
  * [Python](http://www.python.org/getit/) - Tested with Python 2.6.7
  * [setuptools](http://pypi.python.org/pypi/setuptools) - for `easy_install`
  * [virtualenv](http://www.virtualenv.org/en/latest/index.html) - use
    `sudo easy_install virtualenv` or system package
  * [virtualenvwrapper][vew] - use `sudo easy_install virtualenvwrapper` or
    system package
  * [Ruby](http://www.ruby-lang.org/en/downloads/) - Tested with Ruby 1.8.7
  * [RubyGems](http://rubygems.org/) - Tested with RubyGems 1.3.6
4. Follow the [virtualenvwrapper docs][vewd] to update your environment, and
   make a new virtual environment with `mkvirtualenv ottozen`.  You should
   automatically enter the environment, change into the ottozen directory.
5. Leave the virtualenv by running `deactivate`
6. Following the instructions on [this site][bruno], edit the postactivate 
   script in your virtualenv folder to add:

        export GEM_HOME="$VIRTUAL_ENV/gems"
        export GEM_PATH=""
        export PATH=$PATH:$GEM_HOME/

7. Run `workon ottozen` to enter the virtual environment, then run:

        pip install -r requirements.txt
        gem install bundler
        bundle install

[bruno]: http://bruno.im/2011/sep/29/streamline-your-django-workflow/
[vew]: http://www.doughellmann.com/projects/virtualenvwrapper/
[vewd]: http://www.doughellmann.com/docs/virtualenvwrapper/