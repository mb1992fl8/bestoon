# Bestoon project by mamad

A simple expense and income system.

## How to run

To run Bestoon in development mode; Just use steps bellow:

1. Install `python2`, `pip`, `virtualenv` in your system.
2. Clone the project `https://github.com/jadijadi/bestoon`.
3. Make development environment ready using commands bellow;

  ```bash
  git clone https://github.com/jadijadi/bestoon
  virtualenv -p python2 build  # Create virtualenv named env
  source build/bin/activate
  pip install -r requirements.txt
  python manage.py migrate  # Create database tables
  ```

4. Run `Bestoon` using `python manage.py runserver`
5. Go to [http://localhost:8000](http://localhost:8000) to see your Bestoon version.

## Run tests

To run tests in Bestoon simply use `python manage.py test`.

If you want more verbosity you can use `-v` option with `0, 1, 2, or 3.`; e.g. `python manage.py test -v2`

## More Clients

[Ruby Console Clients API bestoon]("http://github.com/shayanzare007/ruby-bestoon-api")

## TODO
- [ ] login webservice (user/pass -> token)
- [x] a restful login service. user will give user pass and will get her token
- [x] local storage for ionic app. will store token and will using it when calling anything
- [ ] create and submit the APK!
- [ ] expand the error message on the server side. client should understand that token was not valid and refer user to login page.