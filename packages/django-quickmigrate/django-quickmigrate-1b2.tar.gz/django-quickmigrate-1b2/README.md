Quick migrations via manage.py
=

When executed without arguments, it will search for the `QUICK_MIGRATE` setting in settings.py,
make migrations for every app in it and apply them.

Otherwise, it will do the same only upon apps given as arguments.

Prompt
`py manage.py quickmigrate -h`
for more specific details on arguments _or_ read the docs below.

Quickstart
=

Installation
--

1. Open your Django project and activate _virtual environment_.

2. After activating virtual environment install the package using 
`pip install django-quickmigrate`

3. Open your settings.py and add `'quickmigrate'` to your `INSTALLED_APPS`

4. Add additional list `QUICK_MIGRATE` into your settings. It should look pretty much
like `INSTALLED_APPS`, except you fill it only with apps you want to be migrated when you
call `py manage.py quickmigrate` without arguments.

5. And that's it. Now you can use `quickmigrate` in your project!

Additional arguments
--

Quickmigrate allows you to choose a variety of apps to migrate during one call.

You can manipulate this using additional arguments listed below:
1. `-i`, `--inst` — command will look at your `INSTALLED_APPS` instead of `QUICK_MIGRATE`.
In its turn, this flag takes one optional argument: either `base` or `all` (defaults to `all`).
    + `base` will just call
    `makemigrations` and `migrate` commands. As the result, only basic apps such as `admin` will be migrated.
    + `all` will make and apply migrations for all `INSTALLED_APPS` which support migrations.

2. `-a`, `--apps` — command will look for specific apps. It can take any amount of arguments
starting from 1.   
**e.g.** `py manage.py quickmigrate --apps myapp1 myapp2 admin auth`

With no arguments provided, the command will look in your `QUICK_MIGRATE` setting.
